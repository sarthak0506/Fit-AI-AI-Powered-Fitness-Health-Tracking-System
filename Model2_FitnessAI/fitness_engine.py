def calculate_bmr(weight_kg, height_cm, age, gender='male'):
    if gender == 'male':
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

ACTIVITY = {1: 1.2, 2: 1.375, 3: 1.465, 4: 1.55, 5: 1.725, 6: 1.9}

def calculate_tdee(bmr, activity_days):
    return bmr * ACTIVITY.get(activity_days, 1.375)

def get_calorie_target(tdee, goal):
    return tdee + 300 if goal == 'bulk' else tdee - 400 if goal == 'cut' else tdee

def get_macro_targets(calories, goal):
    if goal == 'bulk':
        p, c, f = 0.30, 0.45, 0.25
    elif goal == 'cut':
        p, c, f = 0.40, 0.35, 0.25
    else:
        p, c, f = 0.30, 0.40, 0.30
    return {
        "protein_g": round(calories * p / 4),
        "carbs_g":   round(calories * c / 4),
        "fat_g":     round(calories * f / 9),
    }

def get_bmi_category(bmi):
    if bmi < 18.5: return "Underweight"
    if bmi < 25:   return "Normal"
    if bmi < 30:   return "Overweight"
    return "Obese"