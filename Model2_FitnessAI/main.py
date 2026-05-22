import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Model2_FitnessAI.fitness_engine import (
    calculate_bmr, calculate_tdee,
    get_calorie_target, get_macro_targets, get_bmi_category
)
from Model2_FitnessAI.diet_plan    import generate_diet_plan
from Model2_FitnessAI.workout_plan import generate_workout_plan

def run_model2(user):
    bmi      = round(user["weight_kg"] / (user["height_cm"] / 100) ** 2, 1)
    bmr      = calculate_bmr(user["weight_kg"], user["height_cm"], user["age"], user.get("gender","male"))
    tdee     = calculate_tdee(bmr, user["activity_days"])
    target   = get_calorie_target(tdee, user["goal"])
    macros   = get_macro_targets(target, user["goal"])
    diet     = generate_diet_plan(user["diet_pref"], target, macros, user.get("supplements", False))
    workout  = generate_workout_plan(user["goal"], user.get("location", "gym"))

    print("\n" + "="*50)
    print("👤  USER PROFILE")
    print("="*50)
    print(f"  BMI       : {bmi} ({get_bmi_category(bmi)})")
    print(f"  BMR       : {round(bmr)} kcal/day")
    print(f"  TDEE      : {round(tdee)} kcal/day")
    print(f"  Goal      : {user['goal'].upper()}")
    print(f"  Target    : {round(target)} kcal/day")
    print(f"  Protein   : {macros['protein_g']}g | Carbs: {macros['carbs_g']}g | Fat: {macros['fat_g']}g")

    print("\n" + "="*50)
    print("🥗  DAILY DIET PLAN")
    print("="*50)
    for meal, data in diet["meals"].items():
        print(f"  {meal.upper():<14} ({data['time']:<12}) → {data['name']}")
        print(f"  {'':14}   {data['kcal']} kcal | {data['protein']}g protein")
    print(f"\n  Total: {diet['actual_kcal']} kcal | {diet['actual_protein']}g protein")

    print("\n" + "="*50)
    print("🏋️   WEEKLY WORKOUT PLAN")
    print("="*50)
    for day, data in workout.items():
        if data["exercises"]:
            print(f"\n  {day} — {data['focus']}")
            for ex in data["exercises"]:
                print(f"    • {ex['name']:<22} {ex['sets']} sets × {ex['reps']}")
        else:
            print(f"\n  {day} — 🛌 Rest Day")

    return {"diet": diet, "workout": workout, "bmi": bmi}


if __name__ == "__main__":
    user = {
        "name":         "Sarthak",
        "age":          22,
        "weight_kg":    68,
        "height_cm":    172,
        "gender":       "male",
        "activity_days": 4,
        "goal":         "bulk",       # bulk / cut / maintain
        "diet_pref":    "non-veg",    # veg / non-veg / vegan
        "supplements":  True,
        "location":     "gym",        # gym / home
    }
    run_model2(user)