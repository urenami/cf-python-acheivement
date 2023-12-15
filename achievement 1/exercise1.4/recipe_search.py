import pickle

# Function to display the details of a recipe
def display_recipe(recipe):
    print("Recipe:", recipe["name"])
    print("Cooking time (min):", recipe["cooking_time"])
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty:", recipe["difficulty"])
    print()


# Function to search for recipes containing a particular ingredient
def search_ingredient(data):
    # print the list of ingredients
    print("Available ingredients:")
    for index, ingredient in enumerate(data["all_ingredients"]):
        print(index, ingredient)
    print()
    # ask the user for the ingredient they want to search for
    try:
        ingredient_searched = data["all_ingredients"][
            int(input("Enter the number of the ingredient you want to search for: "))
        ]
    except ValueError:
        print("Incorrect input. Please enter a valid number.")
        return
    else:
        # search for recipes containing the ingredient
        recipes_found = []
        for recipe in data["recipes_list"]:
            if ingredient_searched in recipe["ingredients"]:
                recipes_found.append(recipe)
        # display the recipes found
        for recipe in recipes_found:
            display_recipe(recipe)


# Main code

# ask the user for the name of the file containing the recipes
filename = input("Enter the filename where you've stored your recipes: ")

try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File doesn't exist")
except EOFError:
    print("The file is empty. No recipes to display.")
else:
    search_ingredient(data)
finally:
    print("Goodbye!")
