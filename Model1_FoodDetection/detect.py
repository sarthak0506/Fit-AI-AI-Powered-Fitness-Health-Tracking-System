# Model1_FoodDetection/detect.py
# v2 — 107 classes with accurate calorie/macro data

from ultralytics import YOLO
import cv2, json, pathlib

# ─── Calorie DB (kcal per 100g) ──────────────────────────────────────────────
CALORIE_DB = {
    # Indian meals
    "aloo gobi":        97,   "aloo matar":       98,   "aloo methi":       95,
    "biryani":         200,   "butter chicken":  165,   "chicken curry":   150,
    "chicken tikka":   160,   "cholay":          164,   "chole":           164,
    "daal":            116,   "dal":             116,   "dal makhni":      135,
    "dosa":            133,   "idli":             58,   "kadhi pakora":    120,
    "kheer":           150,   "khichdi":         130,   "kulfi":           180,
    "lassi":            98,   "naan":            317,   "pakora":          280,
    "palak paneer":    180,   "palak_paneer":    180,   "paratha":         300,
    "poha":            130,   "raita":            60,   "rajma":           144,
    "roti":            297,   "samosa":          262,   "seekh kabab":     185,
    "shahipaneer":     220,   "shahi paneer":    220,   "tandoori chicken":160,
    "bhatura":         320,   "bhindimasala":     75,   "bhindi masala":    75,
    "dhokla":          160,   "gulab jamun":     387,   "gulab_jamun":     387,
    "jalebi":          370,   "modak":           350,   "rasgulla":        186,
    "chutney":          80,

    # Proteins / eggs
    "chicken":         165,   "chicken wings":   203,   "egg":             155,
    "fried egg":       196,   "boiled egg":      155,   "omelette":        154,

    # Healthy / vegetables
    "salad":            15,   "cucumber":        16,    "soup":             50,
    "red beans":       127,   "rice":            130,   "white rice":      130,

    # Fast food / international
    "apple":            52,   "bread":           265,   "burger":          295,
    "chai":             40,   "donuts":          452,   "dumplings":       220,
    "french fries":    312,   "french toast":    228,   "ice cream":       207,
    "lasagna":         166,   "mac and cheese":  164,   "nachos":          346,
    "onion rings":     301,   "pancakes":        227,   "pizza":           266,
    "potato cutlets":  173,   "sandwich":        250,   "spaghetti":       158,
    "spring rolls":    220,   "tacos":           226,   "waffles":         291,

    # McDonald's (map to generic equivalents)
    "mcdonalds_big_mac":                         295,
    "mcdonalds_caesar_spicy_crispy_chicken_salad": 80,
    "mcdonalds_chicken_mcnuggets":               296,
    "mcdonalds_corn_soup":                        60,
    "mcdonalds_crispy_chicken_leg_original":     250,
    "mcdonalds_double_oreo_mcfurry":             280,
    "mcdonalds_fries":                           312,
    "mcdonalds_hash_brown":                      326,
    "mcdonalds_honey_mustard_sauce":             260,
    "mcdonalds_ice_cream_cone":                  207,
    "mcdonalds_italian_grilled_chicken_salad":    80,
    "mcdonalds_ketchup":                         100,
    "mcdonalds_large_ice_cream_cone":            207,
    "mcdonalds_mcchicken":                       360,
    "mcdonalds_mcfurry":                         207,
    "mcdonalds_oreo_mcfurry":                    207,
    "mcdonalds_parmesan_chef_chicken_burger":    400,
    "mcdonalds_pork_and_egg_mcmuffin":           290,
    "mcdonalds_seasonal_salad":                   35,
    "mcdonalds_spicy_chicken_burger":            360,
    "mcdonalds_spicy_chicken_wings":             240,
    "mcdonalds_sweet_and_sour_sauce":            100,

    # FamilyMart items
    "famfamilymart_strawberry_double_filling_cheese_tartilymart_rice_ball_korean_seared_mayo_chicken": 180,
    "familymart_baked_tuna_sandwich":            220,
    "familymart_blow_wind_marinated_deli_shuangyue": 180,
    "familymart_chicken_white_soup_ramen":       350,
    "familymart_fresh_salmon_tuna_double_hand_roll": 200,
    "familymart_golden_curry_rich_spicy_curry_rice": 380,
    "familymart_kimchi_pork_bun":                280,
    "familymart_pepper_sesame_scallion_cold_noodles": 320,
    "familymart_rice_ball_gangwon-do_snow_crab_roe": 180,
    "familymart_rice_ball_kimchi_tuna":          180,
    "familymart_rice_ball_korean_grilled_beef":  190,
    "familymart_rice_ball_korean_seared_mayo_chicken": 200,
    "familymart_teppan_silky_egg_fried_pork_cutlet_don": 420,
}

# ─── Portion sizes (grams) ───────────────────────────────────────────────────
PORTION_G = {
    # Indian meals
    "aloo gobi":       150,  "aloo matar":      150,  "aloo methi":      150,
    "biryani":         300,  "butter chicken":  200,  "chicken curry":   200,
    "chicken tikka":   150,  "cholay":          150,  "chole":           150,
    "daal":            150,  "dal":             150,  "dal makhni":      150,
    "dosa":            150,  "idli":            120,  "kadhi pakora":    150,
    "kheer":           150,  "khichdi":         200,  "kulfi":            80,
    "lassi":           250,  "naan":            100,  "pakora":          100,
    "palak paneer":    200,  "palak_paneer":    200,  "paratha":         100,
    "poha":            150,  "raita":           100,  "rajma":           150,
    "roti":             80,  "samosa":           80,  "seekh kabab":     100,
    "shahipaneer":     200,  "shahi paneer":    200,  "tandoori chicken":200,
    "bhatura":         100,  "bhindimasala":    150,  "bhindi masala":   150,
    "dhokla":          100,  "gulab jamun":      80,  "gulab_jamun":      80,
    "jalebi":           80,  "modak":            50,  "rasgulla":         80,
    "chutney":          30,

    # Proteins / eggs
    "chicken":         150,  "chicken wings":   150,  "egg":              60,
    "fried egg":        60,  "boiled egg":       60,  "omelette":        100,

    # Healthy / vegetables
    "salad":           200,  "cucumber":        100,  "soup":            250,
    "red beans":       150,  "rice":            195,  "white rice":      195,

    # Fast food / international
    "apple":           182,  "bread":            60,  "burger":          200,
    "chai":            240,  "donuts":            75,  "dumplings":      150,
    "french fries":    150,  "french toast":    100,  "ice cream":       100,
    "lasagna":         300,  "mac and cheese":  200,  "nachos":          100,
    "onion rings":     100,  "pancakes":        150,  "pizza":           200,
    "potato cutlets":  100,  "sandwich":        150,  "spaghetti":       220,
    "spring rolls":    100,  "tacos":           150,  "waffles":         130,

    # McDonald's
    "mcdonalds_big_mac":                          200,
    "mcdonalds_caesar_spicy_crispy_chicken_salad": 250,
    "mcdonalds_chicken_mcnuggets":                150,
    "mcdonalds_corn_soup":                        250,
    "mcdonalds_crispy_chicken_leg_original":      150,
    "mcdonalds_double_oreo_mcfurry":              200,
    "mcdonalds_fries":                            150,
    "mcdonalds_hash_brown":                        60,
    "mcdonalds_honey_mustard_sauce":               30,
    "mcdonalds_ice_cream_cone":                   100,
    "mcdonalds_italian_grilled_chicken_salad":    250,
    "mcdonalds_ketchup":                           30,
    "mcdonalds_large_ice_cream_cone":             150,
    "mcdonalds_mcchicken":                        150,
    "mcdonalds_mcfurry":                          150,
    "mcdonalds_oreo_mcfurry":                     150,
    "mcdonalds_parmesan_chef_chicken_burger":     200,
    "mcdonalds_pork_and_egg_mcmuffin":            150,
    "mcdonalds_seasonal_salad":                   200,
    "mcdonalds_spicy_chicken_burger":             200,
    "mcdonalds_spicy_chicken_wings":              150,
    "mcdonalds_sweet_and_sour_sauce":              30,

    # FamilyMart
    "famfamilymart_strawberry_double_filling_cheese_tartilymart_rice_ball_korean_seared_mayo_chicken": 150,
    "familymart_baked_tuna_sandwich":             150,
    "familymart_blow_wind_marinated_deli_shuangyue": 150,
    "familymart_chicken_white_soup_ramen":        350,
    "familymart_fresh_salmon_tuna_double_hand_roll": 150,
    "familymart_golden_curry_rich_spicy_curry_rice": 300,
    "familymart_kimchi_pork_bun":                 100,
    "familymart_pepper_sesame_scallion_cold_noodles": 200,
    "familymart_rice_ball_gangwon-do_snow_crab_roe": 100,
    "familymart_rice_ball_kimchi_tuna":           100,
    "familymart_rice_ball_korean_grilled_beef":   100,
    "familymart_rice_ball_korean_seared_mayo_chicken": 100,
    "familymart_teppan_silky_egg_fried_pork_cutlet_don": 300,
}

# ─── Protein DB (g per 100g) ─────────────────────────────────────────────────
PROTEIN_DB = {
    # Indian meals
    "aloo gobi":    2,  "aloo matar":    3,  "aloo methi":    2,
    "biryani":      8,  "butter chicken":20, "chicken curry": 18,
    "chicken tikka":25, "cholay":        9,  "chole":          9,
    "daal":         9,  "dal":           9,  "dal makhni":     8,
    "dosa":         3,  "idli":          2,  "kadhi pakora":   5,
    "kheer":        4,  "khichdi":       5,  "kulfi":          3,
    "lassi":        3,  "naan":          9,  "pakora":         5,
    "palak paneer": 10, "palak_paneer": 10,  "paratha":        6,
    "poha":         3,  "raita":         3,  "rajma":          9,
    "roti":         7,  "samosa":        4,  "seekh kabab":   20,
    "shahipaneer":  10, "shahi paneer": 10,  "tandoori chicken":28,
    "bhatura":       6, "bhindimasala":  2,  "bhindi masala":  2,
    "dhokla":        5, "gulab jamun":   2,  "gulab_jamun":    2,
    "jalebi":        1, "modak":         2,  "rasgulla":       1,
    "chutney":       1,

    # Proteins / eggs
    "chicken":      25, "chicken wings": 18, "egg":           13,
    "fried egg":    13, "boiled egg":    13, "omelette":      11,

    # Healthy / vegetables
    "salad":         1, "cucumber":       1, "soup":           3,
    "red beans":     9, "rice":           3, "white rice":     3,

    # Fast food
    "apple":         0, "bread":          9, "burger":        13,
    "chai":          1, "donuts":         5, "dumplings":      8,
    "french fries":  4, "french toast":   7, "ice cream":      3,
    "lasagna":       8, "mac and cheese": 6, "nachos":         5,
    "onion rings":   4, "pancakes":       6, "pizza":         11,
    "potato cutlets":3, "sandwich":      10, "spaghetti":      6,
    "spring rolls":  5, "tacos":          8, "waffles":        7,

    # McDonald's
    "mcdonalds_big_mac":                          13,
    "mcdonalds_caesar_spicy_crispy_chicken_salad": 8,
    "mcdonalds_chicken_mcnuggets":                15,
    "mcdonalds_corn_soup":                         3,
    "mcdonalds_crispy_chicken_leg_original":      18,
    "mcdonalds_double_oreo_mcfurry":               4,
    "mcdonalds_fries":                             4,
    "mcdonalds_hash_brown":                        3,
    "mcdonalds_honey_mustard_sauce":               1,
    "mcdonalds_ice_cream_cone":                    3,
    "mcdonalds_italian_grilled_chicken_salad":    10,
    "mcdonalds_ketchup":                           1,
    "mcdonalds_large_ice_cream_cone":              3,
    "mcdonalds_mcchicken":                        14,
    "mcdonalds_mcfurry":                           4,
    "mcdonalds_oreo_mcfurry":                      4,
    "mcdonalds_parmesan_chef_chicken_burger":     18,
    "mcdonalds_pork_and_egg_mcmuffin":            14,
    "mcdonalds_seasonal_salad":                    2,
    "mcdonalds_spicy_chicken_burger":             16,
    "mcdonalds_spicy_chicken_wings":              18,
    "mcdonalds_sweet_and_sour_sauce":              1,

    # FamilyMart
    "famfamilymart_strawberry_double_filling_cheese_tartilymart_rice_ball_korean_seared_mayo_chicken": 8,
    "familymart_baked_tuna_sandwich":             12,
    "familymart_blow_wind_marinated_deli_shuangyue": 10,
    "familymart_chicken_white_soup_ramen":        15,
    "familymart_fresh_salmon_tuna_double_hand_roll": 12,
    "familymart_golden_curry_rich_spicy_curry_rice": 10,
    "familymart_kimchi_pork_bun":                 10,
    "familymart_pepper_sesame_scallion_cold_noodles": 8,
    "familymart_rice_ball_gangwon-do_snow_crab_roe": 6,
    "familymart_rice_ball_kimchi_tuna":            8,
    "familymart_rice_ball_korean_grilled_beef":    8,
    "familymart_rice_ball_korean_seared_mayo_chicken": 8,
    "familymart_teppan_silky_egg_fried_pork_cutlet_don": 18,
}

# ─── Fat DB (g per 100g) ─────────────────────────────────────────────────────
FAT_DB = {
    "butter chicken": 10, "chicken tikka":  8, "samosa":        17,
    "pakora":         18, "paratha":        12, "biryani":        8,
    "gulab jamun":    12, "gulab_jamun":    12, "jalebi":         8,
    "burger":         17, "pizza":          11, "french fries":  15,
    "mcdonalds_fries":15, "mcdonalds_big_mac":17, "donuts":      25,
    "waffles":        12, "pancakes":        7, "ice cream":     11,
    "egg":            11, "boiled egg":     11, "fried egg":     14,
    "omelette":       12, "naan":           10, "paratha":       12,
    "chicken wings":  14, "chicken":         9, "seekh kabab":   12,
    "lasagna":         8, "mac and cheese":  9, "spring rolls":  10,
}

# ─── Carb DB (g per 100g) ────────────────────────────────────────────────────
CARB_DB = {
    "rice":        28,  "white rice":  28,  "roti":        52,
    "naan":        57,  "paratha":     42,  "biryani":     30,
    "idli":        12,  "dosa":        25,  "poha":        28,
    "khichdi":     25,  "bread":       49,  "burger":      24,
    "pizza":       33,  "french fries":41,  "pancakes":    28,
    "waffles":     37,  "donuts":      51,  "pasta":       25,
    "spaghetti":   25,  "lasagna":     17,  "nachos":      46,
    "tacos":       22,  "samosa":      30,  "jalebi":      65,
    "gulab jamun": 50,  "gulab_jamun": 50,  "rasgulla":    45,
    "modak":       55,  "kheer":       20,  "halwa":       45,
    "apple":       14,  "chai":         4,  "lassi":       12,
    "soup":         5,  "salad":        3,  "cucumber":     4,
    "mcdonalds_fries":  41,
    "mcdonalds_big_mac": 24,
    "mcdonalds_chicken_mcnuggets": 16,
}


def detect_and_estimate(image_path, model_path="Model1_FoodDetection/best.pt",
                        conf=0.4, save_image=True):
    model   = YOLO(model_path)
    results = model(image_path, conf=conf)

    detected   = []
    total_kcal = 0
    total_prot = 0
    total_fat  = 0
    total_carb = 0

    p        = pathlib.Path(image_path)
    out_path = p.parent / (p.stem + '_detected' + p.suffix)

    for r in results:
        if save_image:
            annotated = r.plot()
            cv2.imwrite(str(out_path), annotated)
            print(f"📸 Annotated image saved: {out_path}")

        for box in r.boxes:
            food      = model.names[int(box.cls)].lower()
            confidence= float(box.conf)
            portion   = PORTION_G.get(food, 100)
            kcal_100g = CALORIE_DB.get(food, 100)
            prot_100g = PROTEIN_DB.get(food, 5)
            fat_100g  = FAT_DB.get(food, 5)
            carb_100g = CARB_DB.get(food, 15)

            kcal = round((kcal_100g * portion) / 100)
            prot = round((prot_100g  * portion) / 100)
            fat  = round((fat_100g   * portion) / 100)
            carb = round((carb_100g  * portion) / 100)

            detected.append({
                "food":          food,
                "confidence":    round(confidence, 2),
                "portion_g":     portion,
                "calories_kcal": kcal,
                "protein_g":     prot,
                "fat_g":         fat,
                "carbs_g":       carb,
            })
            total_kcal += kcal
            total_prot += prot
            total_fat  += fat
            total_carb += carb

    print("\n" + "="*55)
    print("🍽️  FOOD DETECTION RESULTS v2")
    print("="*55)
    if not detected:
        print("❌ No food detected. Try a clearer image.")
    for item in detected:
        print(f"  ✅ {item['food']:<30} "
              f"| {item['portion_g']}g "
              f"| {item['calories_kcal']} kcal "
              f"| P:{item['protein_g']}g "
              f"| F:{item['fat_g']}g "
              f"| C:{item['carbs_g']}g "
              f"| conf:{item['confidence']}")
    print("-"*55)
    print(f"  🔥 Calories : {total_kcal} kcal")
    print(f"  💪 Protein  : {total_prot}g")
    print(f"  🧈 Fat      : {total_fat}g")
    print(f"  🌾 Carbs    : {total_carb}g")
    print("="*55)

    return {
        "detected_foods":  detected,
        "total_kcal":      total_kcal,
        "total_protein_g": total_prot,
        "total_fat_g":     total_fat,
        "total_carbs_g":   total_carb,
        "item_count":      len(detected),
        "annotated_path":  str(out_path),
    }


if __name__ == "__main__":
    import sys
    image = sys.argv[1] if len(sys.argv) > 1 else "test_meal.jpg"
    result = detect_and_estimate(image)
    print(json.dumps(result, indent=2))