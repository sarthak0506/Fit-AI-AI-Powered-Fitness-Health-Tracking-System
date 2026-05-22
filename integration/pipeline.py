# integration/pipeline.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Model1_FoodDetection.detect import detect_and_estimate
from Model2_FitnessAI.fitness_engine import (
    calculate_bmr, calculate_tdee,
    get_calorie_target, get_macro_targets, get_bmi_category
)
from Model2_FitnessAI.diet_plan    import generate_diet_plan
from Model2_FitnessAI.workout_plan import generate_workout_plan


def get_user_input():
    """Manually collect user data from terminal"""
    print("\n" + "="*50)
    print("💪  AI FITNESS & HEALTH TRACKER")
    print("="*50)
    print("Enter your details below:\n")

    name     = input("Your name                        : ").strip()
    age      = int(input("Age (years)                      : "))
    weight   = float(input("Weight (kg)                      : "))
    height   = float(input("Height (cm)                      : "))
    gender   = input("Gender (male/female)             : ").strip().lower()

    print("\nActivity level:")
    print("  1 = Sedentary (desk job, no exercise)")
    print("  2 = Light     (1-2 days/week)")
    print("  3 = Moderate  (3 days/week)")
    print("  4 = Active    (4-5 days/week)")
    print("  5 = Very active (6-7 days/week)")
    activity = int(input("Activity level (1-5)             : "))

    print("\nGoal:")
    print("  1 = Bulk (gain muscle)")
    print("  2 = Cut  (lose fat)")
    print("  3 = Maintain")
    goal_map = {"1": "bulk", "2": "cut", "3": "maintain"}
    goal     = goal_map.get(input("Choose goal (1/2/3)              : ").strip(), "maintain")

    print("\nDiet preference:")
    print("  1 = Non-veg")
    print("  2 = Veg")
    print("  3 = Vegan")
    diet_map = {"1": "non-veg", "2": "veg", "3": "vegan"}
    diet     = diet_map.get(input("Choose diet (1/2/3)              : ").strip(), "veg")

    supp     = input("\nDo you use protein supplements? (y/n): ").strip().lower() == "y"

    print("\nWorkout location:")
    print("  1 = Gym")
    print("  2 = Home")
    loc_map  = {"1": "gym", "2": "home"}
    location = loc_map.get(input("Choose location (1/2)            : ").strip(), "gym")

    return {
        "name": name, "age": age, "weight_kg": weight,
        "height_cm": height, "gender": gender,
        "activity_days": activity, "goal": goal,
        "diet_pref": diet, "supplements": supp,
        "location": location,
    }


def run_pipeline(image_path=None, user=None):
    # ── Step 1: Get user input ────────────────────────────────────────────────
    if user is None:
        user = get_user_input()

    # ── Step 2: Calculate fitness metrics ────────────────────────────────────
    bmi    = round(user["weight_kg"] / (user["height_cm"] / 100) ** 2, 1)
    bmr    = calculate_bmr(user["weight_kg"], user["height_cm"],
                           user["age"], user.get("gender", "male"))
    tdee   = calculate_tdee(bmr, user["activity_days"])
    target = get_calorie_target(tdee, user["goal"])
    macros = get_macro_targets(target, user["goal"])
    diet   = generate_diet_plan(user["diet_pref"], target, macros,
                                user.get("supplements", False))
    workout = generate_workout_plan(user["goal"], user.get("location", "gym"))

    # ── Step 3: Food detection (if image provided) ────────────────────────────
    food_result   = None
    eaten_kcal    = 0
    remaining     = round(target)

    if image_path and os.path.exists(image_path):
        print(f"\n📸 Analysing food image: {image_path}")
        food_result = detect_and_estimate(
            image_path,
            model_path="Model1_FoodDetection/best.pt",
            save_image=True
        )
        eaten_kcal = food_result["total_kcal"]
        remaining  = round(target - eaten_kcal)

    # ── Step 4: Print full report ─────────────────────────────────────────────
    print("\n\n" + "="*55)
    print(f"  👤  REPORT FOR {user['name'].upper()}")
    print("="*55)

    print(f"\n  BMI      : {bmi}  ({get_bmi_category(bmi)})")
    print(f"  BMR      : {round(bmr)} kcal/day")
    print(f"  TDEE     : {round(tdee)} kcal/day")
    print(f"  Goal     : {user['goal'].upper()}")
    print(f"  Target   : {round(target)} kcal/day")
    print(f"  Macros   : Protein {macros['protein_g']}g | "
          f"Carbs {macros['carbs_g']}g | Fat {macros['fat_g']}g")

    if food_result:
        print("\n" + "-"*55)
        print("  🍽️  MEAL LOG (from image)")
        print("-"*55)
        for item in food_result["detected_foods"]:
            print(f"  • {item['food']:<20} {item['calories_kcal']} kcal "
                  f"| {item['protein_g']}g protein")
        print(f"\n  Eaten so far : {eaten_kcal} kcal")
        print(f"  Remaining    : {remaining} kcal  ", end="")
        if abs(remaining) < 150:
            print("✅ On track!")
        elif remaining > 0:
            print("⬇️  You need to eat more today")
        else:
            print("⬆️  You've exceeded your target")

    print("\n" + "-"*55)
    print("  🥗  TODAY'S DIET PLAN")
    print("-"*55)
    for meal, data in diet["meals"].items():
        print(f"  {meal.upper():<14} {data['time']:<14} → {data['name']}")
        print(f"  {'':14} {'':14}   {data['kcal']} kcal | {data['protein']}g protein")

    print(f"\n  Daily total  : {diet['actual_kcal']} kcal | "
          f"{diet['actual_protein']}g protein")

    print("\n" + "-"*55)
    print("  🏋️   WEEKLY WORKOUT PLAN")
    print("-"*55)
    for day, data in workout.items():
        if data["exercises"]:
            print(f"\n  {day} — {data['focus']}")
            for ex in data["exercises"]:
                print(f"    • {ex['name']:<24} {ex['sets']} sets × {ex['reps']}")
        else:
            print(f"\n  {day} — 🛌 Rest Day")

    print("\n" + "="*55)
    print("  ✅  Report complete! Stay consistent 💪")
    print("="*55 + "\n")

    return {
        "user":         user,
        "bmi":          bmi,
        "calorie_target": round(target),
        "macros":       macros,
        "diet_plan":    diet,
        "workout_plan": workout,
        "food_log":     food_result,
        "remaining_kcal": remaining,
    }


if __name__ == "__main__":
    # ── Option A: with food image ─────────────────────────────────────────────
    # user = get_user_input()
    # run_pipeline(image_path="test_meal1.jpg", user=user)

    # ── Option B: just fitness plan, no image ─────────────────────────────────
    run_pipeline(image_path="test_meal1.jpg")