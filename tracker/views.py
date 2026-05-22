# tracker/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.db import models
from .models import FoodLog, DietPlan, WorkoutPlan
from accounts.models import UserProfile
import sys, os, json, pathlib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Model2_FitnessAI.fitness_engine import calculate_bmr, calculate_tdee, get_calorie_target, get_macro_targets
from Model2_FitnessAI.diet_plan import generate_diet_plan
from Model2_FitnessAI.workout_plan import generate_workout_plan


def get_greeting():
    h = timezone.now().hour
    if h < 12: return 'morning'
    if h < 17: return 'afternoon'
    return 'evening'


@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    today = timezone.now().date()

    recent_logs = FoodLog.objects.filter(user=request.user, logged_at__date=today).order_by('-logged_at')[:5]
    eaten_today = sum(l.total_kcal for l in FoodLog.objects.filter(user=request.user, logged_at__date=today))

    bmr      = calculate_bmr(profile.weight_kg, profile.height_cm, profile.age, profile.gender)
    tdee     = calculate_tdee(bmr, profile.activity_days)
    target   = int(get_calorie_target(tdee, profile.goal))
    remaining= max(0, target - eaten_today)
    progress = min(100, int((eaten_today / target * 100) if target else 0))

    from datetime import timedelta
    import json as _json
    week_labels, week_eaten, week_target = [], [], []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_total = FoodLog.objects.filter(
            user=request.user, logged_at__date=day
        ).aggregate(total=models.Sum('total_kcal'))['total'] or 0
        week_labels.append(day.strftime('%a'))
        week_eaten.append(day_total)
        week_target.append(target)

    return render(request, 'tracker/dashboard.html', {
        'greeting':       get_greeting(),
        'calorie_target': target,
        'eaten_today':    eaten_today,
        'remaining':      remaining,
        'progress_pct':   progress,
        'bmi':            profile.bmi(),
        'bmi_category':   profile.bmi_category(),
        'recent_logs':    recent_logs,
        'week_labels':    _json.dumps(week_labels),
        'week_eaten':     _json.dumps(week_eaten),
        'week_target':    _json.dumps(week_target),
    })


@login_required
def food_log(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    logs = FoodLog.objects.filter(user=request.user).order_by('-logged_at')[:20]

    if request.method == 'POST' and request.FILES.get('image'):
        import uuid
        from django.core.files.storage import default_storage
        from Model1_FoodDetection.detect import detect_and_estimate

        img  = request.FILES['image']
        ext  = pathlib.Path(img.name).suffix.lower()  # e.g. .jpg
        uid  = str(uuid.uuid4())[:8]
        name = f'food_logs/{uid}{ext}'

        # Save original to media/food_logs/
        saved_path = default_storage.save(name, img)
        # Full absolute path for YOLO
        full_path  = pathlib.Path(settings.MEDIA_ROOT) / saved_path

        print(f"DEBUG saved original: {full_path}")

        # Run YOLO — returns annotated_path
        result = detect_and_estimate(
            str(full_path),
            model_path='Model1_FoodDetection/best.pt',
            save_image=True,
        )

        # Annotated image is saved as uid_detected.jpg in same folder
        annotated_full = pathlib.Path(result['annotated_path'])
        print(f"DEBUG annotated path: {annotated_full}")
        print(f"DEBUG annotated exists: {annotated_full.exists()}")

        # Relative path for DB — strip MEDIA_ROOT prefix
        if annotated_full.exists():
            image_rel = str(annotated_full.relative_to(settings.MEDIA_ROOT))
        else:
            image_rel = saved_path  # fallback to original

        # Normalise slashes for URLs
        image_rel = image_rel.replace('\\', '/')
        print(f"DEBUG image_rel stored in DB: {image_rel}")

        FoodLog.objects.create(
            user          = request.user,
            image         = image_rel,
            detected      = json.dumps(result['detected_foods']),
            total_kcal    = result['total_kcal'],
            total_protein = result['total_protein_g'],
            meal_type     = request.POST.get('meal_type', 'meal'),
        )
        return redirect('food_log')

    return render(request, 'tracker/food_log.html', {'logs': logs})


@login_required
def my_plan(request):
    from Model2_FitnessAI.recipes import get_recipe

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    bmr     = calculate_bmr(profile.weight_kg, profile.height_cm, profile.age, profile.gender)
    tdee    = calculate_tdee(bmr, profile.activity_days)
    target  = get_calorie_target(tdee, profile.goal)
    macros  = get_macro_targets(target, profile.goal)
    diet    = generate_diet_plan(profile.diet_pref, target, macros, profile.supplements)
    workout = generate_workout_plan(profile.goal, profile.location)

    meals_with_recipes = {}
    for meal_type, meal_data in diet['meals'].items():
        recipe = get_recipe(meal_data['name'])
        meals_with_recipes[meal_type] = {**meal_data, 'recipe': recipe}

    return render(request, 'tracker/my_plan.html', {
        'diet':               diet,
        'workout':            workout,
        'calorie_target':     int(target),
        'macros':             macros,
        'meals_with_recipes': meals_with_recipes,
    })