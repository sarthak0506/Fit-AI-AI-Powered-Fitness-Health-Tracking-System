# Model2_FitnessAI/recipes.py

RECIPES = {
    "paneer paratha": {
        "ingredients": ["Whole wheat flour 2 cups", "Paneer 100g crumbled", "Green chilli 1 chopped", "Cumin seeds 1 tsp", "Salt to taste", "Oil 1 tsp"],
        "steps": ["Knead soft dough with flour and water", "Mix paneer with chilli, cumin and salt", "Stuff paneer mix into dough balls", "Roll flat and cook on tawa with minimal oil", "Serve hot with curd"],
        "prep_time": "20 mins", "protein_g": 22, "kcal": 450,
    },
    "moong dal chilla": {
        "ingredients": ["Moong dal 1 cup (soaked 4hrs)", "Ginger 1 inch", "Green chilli 1", "Salt + cumin", "Oil spray"],
        "steps": ["Blend soaked dal with ginger and chilli", "Add salt and cumin, make thin batter", "Pour on hot non-stick pan like pancake", "Cook 2 min each side", "Serve with mint chutney"],
        "prep_time": "15 mins", "protein_g": 18, "kcal": 350,
    },
    "oats": {
        "ingredients": ["Rolled oats 1 cup", "Milk 1 cup", "Banana 1", "Mixed nuts 1 tbsp", "Honey 1 tsp"],
        "steps": ["Boil milk and add oats", "Cook stirring for 3-4 minutes", "Top with sliced banana and nuts", "Drizzle honey and serve warm"],
        "prep_time": "10 mins", "protein_g": 15, "kcal": 400,
    },
    "boiled eggs": {
        "ingredients": ["Eggs 3", "Water", "Salt + pepper"],
        "steps": ["Boil water in a pot", "Add eggs and cook 8-10 min for hard boiled", "Cool in cold water, peel and serve", "Season with salt and pepper"],
        "prep_time": "12 mins", "protein_g": 18, "kcal": 210,
    },
    "chicken curry": {
        "ingredients": ["Chicken breast 200g", "Onion 1 large", "Tomato 2", "Ginger garlic paste 1 tbsp", "Cumin + coriander 1 tsp each", "Turmeric + chilli powder", "Oil 1 tsp"],
        "steps": ["Marinate chicken with turmeric and salt 15 min", "Saute onion till golden in 1 tsp oil", "Add ginger garlic paste, cook 2 min", "Add tomatoes and spices, cook till oil separates", "Add chicken, cook covered 15-20 min", "Garnish with coriander"],
        "prep_time": "35 mins", "protein_g": 42, "kcal": 320,
    },
    "grilled chicken": {
        "ingredients": ["Chicken breast 200g", "Lemon juice 2 tbsp", "Garlic 3 cloves minced", "Olive oil 1 tsp", "Mixed herbs + paprika", "Salt + pepper"],
        "steps": ["Mix lemon, garlic, oil and spices for marinade", "Marinate chicken minimum 30 minutes", "Heat grill pan on high", "Grill 6-7 min each side", "Rest 5 min before slicing"],
        "prep_time": "45 mins", "protein_g": 44, "kcal": 280,
    },
    "dal": {
        "ingredients": ["Toor dal 1 cup", "Tomato 1", "Onion 1", "Turmeric 1/2 tsp", "Cumin seeds 1 tsp", "Mustard seeds 1 tsp", "Ghee 1 tsp"],
        "steps": ["Pressure cook dal with turmeric and salt (3 whistles)", "Heat ghee, add mustard and cumin seeds", "Add onion, cook till golden", "Add tomato, cook till soft", "Mix tadka into dal, simmer 5 min"],
        "prep_time": "25 mins", "protein_g": 20, "kcal": 300,
    },
    "rajma": {
        "ingredients": ["Rajma 1 cup (soaked overnight)", "Onion 2", "Tomato 2", "Ginger garlic paste 1 tbsp", "Rajma masala 2 tsp", "Oil 1 tsp"],
        "steps": ["Pressure cook soaked rajma (5-6 whistles)", "Saute onion till golden", "Add ginger garlic paste and tomatoes", "Add spices, cook till oil separates", "Add cooked rajma, simmer 15 min", "Serve with rice"],
        "prep_time": "40 mins", "protein_g": 22, "kcal": 350,
    },
    "sprouts chaat": {
        "ingredients": ["Mixed sprouts 1 cup", "Tomato 1 chopped", "Onion 1 small chopped", "Lemon juice 1 tbsp", "Chaat masala 1/2 tsp", "Coriander leaves"],
        "steps": ["Steam sprouts 5 minutes", "Mix with chopped vegetables", "Add lemon juice and chaat masala", "Toss well and garnish with coriander", "Serve immediately"],
        "prep_time": "10 mins", "protein_g": 10, "kcal": 180,
    },
    "whey protein shake": {
        "ingredients": ["Whey protein 1 scoop (30g)", "Cold water or milk 250ml", "Ice cubes optional", "Banana optional for extra calories"],
        "steps": ["Add liquid to shaker first", "Add protein powder", "Shake vigorously 30 seconds", "Add ice and drink immediately post workout"],
        "prep_time": "2 mins", "protein_g": 25, "kcal": 130,
    },
}

def get_recipe(meal_name):
    meal_lower = meal_name.lower()
    for key, data in RECIPES.items():
        if key in meal_lower or any(w in meal_lower for w in key.split()):
            return {"name": key.title(), **data}
    return None