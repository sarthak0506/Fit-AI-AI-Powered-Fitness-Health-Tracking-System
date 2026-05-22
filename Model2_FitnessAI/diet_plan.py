import random

MEALS = {
    "veg": {
        "breakfast": [
            {"name": "Paneer paratha (2) + curd",        "kcal": 450, "protein": 22, "time": "7:30 AM"},
            {"name": "Moong dal chilla (3) + chutney",   "kcal": 350, "protein": 18, "time": "7:30 AM"},
            {"name": "Oats + milk + banana + nuts",      "kcal": 400, "protein": 15, "time": "7:30 AM"},
            {"name": "Besan chilla + green chutney",     "kcal": 320, "protein": 16, "time": "7:30 AM"},
        ],
        "lunch": [
            {"name": "Dal + roti (2) + sabzi + salad",   "kcal": 550, "protein": 24, "time": "1:00 PM"},
            {"name": "Rajma chawal + salad + raita",     "kcal": 600, "protein": 22, "time": "1:00 PM"},
            {"name": "Chole + rice + raita",             "kcal": 580, "protein": 20, "time": "1:00 PM"},
            {"name": "Palak paneer + roti (2) + salad",  "kcal": 520, "protein": 26, "time": "1:00 PM"},
        ],
        "snack": [
            {"name": "Sprouts chaat",                    "kcal": 180, "protein": 10, "time": "4:30 PM"},
            {"name": "Peanut butter + banana",           "kcal": 250, "protein":  8, "time": "4:30 PM"},
            {"name": "Greek yoghurt + mixed nuts",       "kcal": 200, "protein": 12, "time": "4:30 PM"},
            {"name": "Roasted chana (50g)",              "kcal": 190, "protein": 10, "time": "4:30 PM"},
        ],
        "dinner": [
            {"name": "Palak paneer + roti (2)",          "kcal": 500, "protein": 25, "time": "7:30 PM"},
            {"name": "Mixed veg curry + rice + dal",     "kcal": 480, "protein": 18, "time": "7:30 PM"},
            {"name": "Tofu stir fry + roti (2)",         "kcal": 420, "protein": 22, "time": "7:30 PM"},
            {"name": "Paneer bhurji + roti (2)",         "kcal": 510, "protein": 28, "time": "7:30 PM"},
        ],
    },
    "non-veg": {
        "breakfast": [
            {"name": "3 egg omelette + brown bread (2)", "kcal": 420, "protein": 30, "time": "7:30 AM"},
            {"name": "Boiled eggs (3) + oats + milk",    "kcal": 400, "protein": 28, "time": "7:30 AM"},
            {"name": "Chicken poha + green tea",         "kcal": 380, "protein": 25, "time": "7:30 AM"},
            {"name": "Egg paratha (2) + curd",           "kcal": 450, "protein": 26, "time": "7:30 AM"},
        ],
        "lunch": [
            {"name": "Chicken curry + roti (2) + salad", "kcal": 600, "protein": 42, "time": "1:00 PM"},
            {"name": "Grilled fish + rice + dal",        "kcal": 580, "protein": 40, "time": "1:00 PM"},
            {"name": "Egg biryani + raita",              "kcal": 620, "protein": 32, "time": "1:00 PM"},
            {"name": "Chicken rice bowl + salad",        "kcal": 560, "protein": 38, "time": "1:00 PM"},
        ],
        "snack": [
            {"name": "Boiled eggs (2) + nuts",           "kcal": 220, "protein": 16, "time": "4:30 PM"},
            {"name": "Chicken sandwich (brown bread)",   "kcal": 300, "protein": 22, "time": "4:30 PM"},
            {"name": "Tuna salad",                       "kcal": 180, "protein": 20, "time": "4:30 PM"},
            {"name": "Greek yoghurt + boiled egg",       "kcal": 200, "protein": 18, "time": "4:30 PM"},
        ],
        "dinner": [
            {"name": "Grilled chicken + sabzi + roti",   "kcal": 550, "protein": 44, "time": "7:30 PM"},
            {"name": "Fish curry + rice",                "kcal": 500, "protein": 36, "time": "7:30 PM"},
            {"name": "Chicken stir fry + roti (2)",      "kcal": 520, "protein": 40, "time": "7:30 PM"},
            {"name": "Baked fish + salad + roti",        "kcal": 480, "protein": 38, "time": "7:30 PM"},
        ],
    },
    "vegan": {
        "breakfast": [
            {"name": "Oats + almond milk + banana",      "kcal": 320, "protein": 10, "time": "7:30 AM"},
            {"name": "Tofu scramble + toast (2)",        "kcal": 380, "protein": 20, "time": "7:30 AM"},
            {"name": "Smoothie bowl + seeds + nuts",     "kcal": 350, "protein": 12, "time": "7:30 AM"},
        ],
        "lunch": [
            {"name": "Lentil soup + quinoa + salad",     "kcal": 500, "protein": 22, "time": "1:00 PM"},
            {"name": "Chole + rice + salad",             "kcal": 560, "protein": 20, "time": "1:00 PM"},
            {"name": "Tofu curry + roti (2)",            "kcal": 520, "protein": 24, "time": "1:00 PM"},
        ],
        "snack": [
            {"name": "Hummus + veggie sticks",           "kcal": 160, "protein":  6, "time": "4:30 PM"},
            {"name": "Mixed nuts + seeds (40g)",         "kcal": 220, "protein":  6, "time": "4:30 PM"},
            {"name": "Peanut butter + rice cake",        "kcal": 200, "protein":  6, "time": "4:30 PM"},
        ],
        "dinner": [
            {"name": "Dal + roti (2) + sabzi",           "kcal": 480, "protein": 18, "time": "7:30 PM"},
            {"name": "Chickpea stir fry + rice",         "kcal": 450, "protein": 16, "time": "7:30 PM"},
            {"name": "Lentil dal + quinoa + salad",      "kcal": 460, "protein": 20, "time": "7:30 PM"},
        ],
    },
}

def generate_diet_plan(diet_pref, calorie_target, macros, supplements=False):
    plan   = MEALS.get(diet_pref, MEALS["veg"])
    daily  = {}
    for meal in ["breakfast", "lunch", "snack", "dinner"]:
        daily[meal] = random.choice(plan[meal])

    if supplements:
        daily["post_workout"] = {
            "name": "Whey protein shake (1 scoop) + water",
            "kcal": 130, "protein": 25, "time": "Within 30 min after workout"
        }

    total_kcal = sum(m["kcal"]    for m in daily.values())
    total_prot = sum(m["protein"] for m in daily.values())

    return {
        "calorie_target": round(calorie_target),
        "macros":         macros,
        "meals":          daily,
        "actual_kcal":    total_kcal,
        "actual_protein": total_prot,
    }