class Recipe:
    all_ingredients = []

    def __init__(self, name, cooking_time):
        self.name = name
        self.ingredients = []
        self.cooking_time = cooking_time
        self.difficulty = None

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_cooking_time(self):
        return self.cooking_time

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    def add_ingredients(self, *ingredients):
        for ingredient in ingredients:
            self.ingredients.append(ingredient)
        self.update_all_ingredients()

    def get_ingredients(self):
        return self.ingredients

    # Sets the difficulty attribute based on the number of ingredients and cooking time.
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    def get_difficulty(self):
        if self.difficulty == None:
            self.calculate_difficulty()
        return self.difficulty

    # Checks if an ingredient is in the recipe.
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    # Updates the all_ingredients list with the ingredients of the recipe.
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)

    # Returns a string representation of the recipe.
    def __str__(self):
        output = (
            f"Recipe: {self.name}\n"
            + f"coking time: {self.cooking_time} minutes\n"
            + f"difficulty: {self.get_difficulty()}\n"
            + f"ingredients:\n"
        )
        for ingredient in self.ingredients:
            output += f"\t{ingredient}\n"
        return output


# Method to search for a recipe based on an ingredient.
def recipe_search(data, search_term):
    found_recipes = []  # Keep track of printed recipe names
    for recipe in data:
        if (
            recipe.search_ingredient(search_term)
            and recipe.get_name() not in found_recipes
        ):
            print(recipe)
            found_recipes.append(recipe.get_name())
    print()


# Create a recipe for tea.
tea = Recipe("Tea", 5)
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
print(tea)

# Create a recipe for Coffee.
coffee = Recipe("Coffee", 5)
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
print(coffee)

# Create a recipe for Cake.
cake = Recipe("Cake", 50)
cake.add_ingredients(
    "Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"
)
print(cake)

# Create a recipe for Banana Smoothie.
banana_smoothie = Recipe("Banana Smoothie", 5)
banana_smoothie.add_ingredients(
    "Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"
)
print(banana_smoothie)

# Wrap the recipes into a list called recipes_list.
recipes_list = [tea, coffee, cake, banana_smoothie]

# search for recipes containing "Water", "Sugar", or "Bananas"
for search_term in ["Water", "Sugar", "Bananas"]:
    print("-" * 50)
    print()
    print(f"Recipes containing {search_term}:")
    recipe_search(recipes_list, search_term)
    print()
