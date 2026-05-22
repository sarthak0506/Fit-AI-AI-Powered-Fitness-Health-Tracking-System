# chatbot/views.py
import sys
import os
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from tracker.models import ChatMessage, FoodLog
from accounts.models import UserProfile

try:
    from groq import Groq
except ImportError:
    Groq = None

@login_required
def chatbot(request):
    history = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:20]
    return render(request, 'chatbot/chatbot.html', {'history': list(reversed(history))})


@login_required
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    if Groq is None:
        return JsonResponse({'reply': 'Groq not installed. Run: uv pip install groq'})

    data    = json.loads(request.body)
    message = data.get('message', '').strip()
    if not message:
        return JsonResponse({'error': 'empty'}, status=400)

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # ── Today's food logs ─────────────────────────────────────────────────────
    today      = timezone.now().date()
    today_logs = FoodLog.objects.filter(user=request.user, logged_at__date=today)
    eaten_kcal = sum(l.total_kcal    for l in today_logs)
    eaten_prot = sum(l.total_protein for l in today_logs)

    # Build food log summary string
    food_log_lines = []
    for log in today_logs:
        items = json.loads(log.detected) if log.detected else []
        for item in items:
            food_log_lines.append(
                f"  - {item['food'].title()} | {item['portion_g']}g | "
                f"{item['calories_kcal']} kcal | {item['protein_g']}g protein"
            )
    food_log_str = '\n'.join(food_log_lines) if food_log_lines else '  Nothing logged yet today'

    # ── Calorie calculations ──────────────────────────────────────────────────
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from Model2_FitnessAI.fitness_engine import (
        calculate_bmr, calculate_tdee,
        get_calorie_target, get_macro_targets, get_bmi_category
    )
    bmr       = calculate_bmr(profile.weight_kg, profile.height_cm, profile.age, profile.gender)
    tdee      = calculate_tdee(bmr, profile.activity_days)
    target    = int(get_calorie_target(tdee, profile.goal))
    macros    = get_macro_targets(target, profile.goal)
    remaining = max(0, target - eaten_kcal)
    progress  = min(100, int((eaten_kcal / target * 100) if target else 0))

    # ── System prompt with full context ──────────────────────────────────────
    system_prompt = f"""You are FitAI, a smart personal fitness and nutrition assistant.

=== USER PROFILE ===
Name        : {request.user.username}
Age         : {profile.age} | Gender: {profile.gender}
Weight      : {profile.weight_kg}kg | Height: {profile.height_cm}cm
BMI         : {profile.bmi()} ({profile.bmi_category()})
Goal        : {profile.goal.upper()} | Diet: {profile.diet_pref}
Activity    : {profile.activity_days} days/week | Location: {profile.location}
Supplements : {'Yes' if profile.supplements else 'No'}

=== TODAY'S CALORIE TRACKER ===
Daily Target  : {target} kcal
Eaten So Far  : {eaten_kcal} kcal
Protein Eaten : {eaten_prot}g
Remaining     : {remaining} kcal
Progress      : {progress}%
Macro Targets : Protein {macros['protein_g']}g | Carbs {macros['carbs_g']}g | Fat {macros['fat_g']}g

=== TODAY'S FOOD LOG ===
{food_log_str}

=== YOUR RULES ===
- You KNOW all the above data — never ask the user for calories or profile info
- Always use the real numbers above when answering about calories, remaining, progress
- Give specific, practical, motivating advice
- If the user asks "how many calories remaining" → answer with {remaining} kcal
- If the user asks "what have I eaten" → list the food log above
- Keep responses concise, use bullet points for lists
- Always relate advice to their goal ({profile.goal}) and diet ({profile.diet_pref})
- If they've eaten over target, be supportive not negative
"""

    # ── Build message history ─────────────────────────────────────────────────
    history  = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:10]
    messages = [{'role': 'system', 'content': system_prompt}]
    for msg in reversed(history):
        messages.append({'role': msg.role, 'content': msg.content})
    messages.append({'role': 'user', 'content': message})

    try:
        client   = Groq(api_key=settings.GROQ_API_KEY)
        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=messages,
            max_tokens=600,
            temperature=0.7,
        )
        reply = response.choices[0].message.content

        ChatMessage.objects.create(user=request.user, role='user',      content=message)
        ChatMessage.objects.create(user=request.user, role='assistant', content=reply)

        return JsonResponse({'reply': reply})

    except Exception as e:
        return JsonResponse({'reply': f'Error: {str(e)}'})