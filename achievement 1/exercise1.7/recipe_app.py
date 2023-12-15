# set up sqlalchemy, create engine and session, run program
from sqlalchemy import create_engine, func

engine = create_engine("mysql://root:Elizavi2021!@localhost/task_database")

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Sequence
from sqlalchemy.types import Integer, String

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


# create model
class Recipe(Base):
    __tablename__ = "final_recipes"
    id = Column(
        Integer, Sequence("recipe_id_seq"), primary_key=True, autoincrement=True
    )
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return (
            "<Recipe ID: "
            + str(self.id)
            + "-"
            + self.name
            + "-"
            + self.difficulty
            + ">"
        )

    def __str__(self):
        return (
            "\n"
            + self.name
            + "\nRecipe ID: "
            + str(self.id)
            + "\nIngredients: "
            + self.ingredients
            + "\nCooking time: "
            + str(self.cooking_time)
            + " minutes\nDifficulty: "
            + self.difficulty
        )


def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        return "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        return "Intermediate"
    elif cooking_time >= 10 and len(ingredients) >= 4:
        return "Hard"


def return_ingredients_as_list():
    if Recipe.ingredients == "":
        return []
    else:
        return list(Recipe.ingredients.lower().split(",").strip())


Base.metadata.create_all(engine)


def create_recipe():
    print()
    print("=" * 30)
    print("Create a New Recipe")
    print("-" * 30)

    # setting the entered name as the recipe's name if under 50 characters
    name_is_valid = False
    while name_is_valid == False:
        name_input = input("Enter the name of your recipe: ")
        if len(name_input) <= 50:
            name = name_input
            name_is_valid = True
        else:
            print()
            print("*" * 30)
            print(
                "The name of your recipe must be less than 50 characters. Please try again."
            )
            print("*" * 30)
            print()

    # setting the entered ingredients as the recipe's ingredients
    ingredients = []
    num_ingredients_is_valid = False
    while num_ingredients_is_valid == False:
        number_of_ingredients = input(
            "Enter the number of ingredients in your recipe: "
        )
        if number_of_ingredients.isnumeric():
            ingredient_number = 1
            while ingredient_number <= int(number_of_ingredients):
                ingredient = input("\tEnter an ingredient: ")
                ingredients.append(ingredient)
                ingredient_number += 1
            num_ingredients_is_valid = True
        else:
            print()
            print("*" * 30)
            print("The number of ingredients must be a number. Please try again")
            print("*" * 30)
            print()

    # setting the entered cooking time as the recipe's cooking time if a number
    cooking_time_is_valid = False
    while cooking_time_is_valid == False:
        cooking_time_input = input(
            "Enter how long your recipe will take to make in minutes: "
        )
        if cooking_time_input.isnumeric():
            cooking_time = int(cooking_time_input)
            cooking_time_is_valid = True
        else:
            print()
            print("*" * 30)
            print("Your cooking time must be a number. Please try again.")
            print("*" * 30)
            print()

            # Calculate the new recipe_id
        max_recipe_id = session.query(func.max(Recipe.id)).scalar()
        # Set the new recipe_id to be one greater than the maximum (or 1 if no recipes exist)
        new_recipe_id = (max_recipe_id or 0) + 1

    # object based on Recipe model to add new recipe to database
    ingredients_string = ", ".join(ingredients)
    recipe_entry = Recipe(
        id=new_recipe_id,
        name=name,
        ingredients=ingredients_string,
        cooking_time=cooking_time,
        difficulty=calculate_difficulty(cooking_time, ingredients),
    )
    session.add(recipe_entry)
    session.commit()


# view all recipes
def view_all_recipes():
    print("=" * 30)
    print("All Recipes")
    print("-" * 30)
    recipes_list = session.query(Recipe).all()
    if not recipes_list:
        print("\nYou don't have any recipes yet! Try creating a new recipe.")
    else:
        for recipe in recipes_list:
            print(recipe)



def search_by_ingredients():
    print("=" * 30)
    print("All Ingredients")
    print("-" * 30)

    # check whether there are recipes to search
    if session.query(Recipe).count() == 0:
        print("\nYou don't have any recipes yet! Try creating a new recipe.")
        return None
    else:
        # add all ingredients to a list
        results = session.query(Recipe.ingredients).all()
        all_ingredients = []
        for result in results:
            ingredient_list = list(result[0].lower().split(", "))
            for ingredient in ingredient_list:
                if ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)

        # create a numbered list of ingredients
        printed_ingredients = list(enumerate(all_ingredients, 1))
        for ingredient in printed_ingredients:
            print(str(ingredient[0]) + ". " + ingredient[1])

        # allow users to select ingredients to search
        try:
            search_input = input(
                "\nSelect the number of one or more ingredients you'd like to search in recipes (separate numbers by a space): "
            )
            search_input_list = list(search_input.split(" "))
            search_ingredients = []
            for item in search_input_list:
                search_ingredients.append(all_ingredients[int(item) - 1])
            print("\nThe following recipes include your selected ingredients:")
        # if the user made an invalid selection
        except:
            print()
            print("*" * 30)
            print("Ingredient number is not valid.")
            print("*" * 30)
            print()
            return None
        else:
            conditions = []
            for ingredient in search_ingredients:
                like_term = "%" + ingredient + "%"
                conditions.append(Recipe.ingredients.like(like_term))
            searched_recipes = session.query(Recipe).filter(*conditions).all()
            for recipe in searched_recipes:
                print(recipe)


# edit a recipe
def edit_recipe():
    print("=" * 30)
    print("Edit a Recipe")
    print("-" * 30)

    # check whether there are recipes to edit
    if session.query(Recipe).count() == 0:
        print("\n You don\t have any recipes yet! Try creating a new recipe.")
        return None
    else:
        results = session.query(Recipe.id, Recipe.name).all()
        print("Your recipes:")
        for result in results:
            print("\n\tRecipe ID:", result[0])
            print("\tRecipe name:", result[1])
        try:
            selected_id = input("\nEnter a recipe's ID to choose a recipe to edit: ")
            recipe_to_edit = (
                session.query(Recipe).filter(Recipe.id == int(selected_id)).one()
            )
            print("\nYou have selected the following recipe to edit:")
            print("\n\t1. Name:", recipe_to_edit.name)
            print("\n\t2. Ingredients:", recipe_to_edit.ingredients)
            print("\n\t3. Cooking Time:", recipe_to_edit.cooking_time, "minutes")
        except:
            print()
            print("*" * 30)
            print("Recipe ID is not valid.")
            print("*" * 30)
            print()
        else:
            edit_input = input(
                "\nChoose which part of the recipe you want to edit by entering the corresponding number listed above: "
            )
            if edit_input == "1":
                new_name = input("Select a new name: ")
                if len(new_name) <= 50:
                    recipe_to_edit.name = new_name
                    session.commit()
                    print("\nYour recipe's name has been updated:", recipe_to_edit.name)
                else:
                    print()
                    print("*" * 30)
                    print("Recipe name is too long. Please try again.")
                    print("*" * 30)
                    print()
            elif edit_input == "2":
                new_ingredients = input(
                    "List the recipe's ingredients, separated by commas: "
                )
                if len(new_ingredients) <= 255:
                    new_ingredients_list = list(new_ingredients.lower().split(", "))
                    new_difficulty = calculate_difficulty(
                        recipe_to_edit.cooking_time, new_ingredients_list
                    )
                    recipe_to_edit.ingredients = new_ingredients
                    recipe_to_edit.difficulty = new_difficulty
                    session.commit()
                    print(
                        "\nYour recipe's ingredients have been updated:",
                        recipe_to_edit.ingredients,
                    )
                else:
                    print()
                    print("*" * 30)
                    print("Ingredient list is too long. Please try again.")
                    print("*" * 30)
                    print()
            elif edit_input == "3":
                new_cooking_time = input(
                    "Enter your recipe's cooking time in minutes: "
                )
                if new_cooking_time.isnumeric():
                    new_difficulty = calculate_difficulty(
                        int(new_cooking_time),
                        list(recipe_to_edit.ingredients.lower().split(", ")),
                    )
                    recipe_to_edit.cooking_time = int(new_cooking_time)
                    recipe_to_edit.difficulty = new_difficulty
                    session.commit()
                    print(
                        "\nYour recipe's cooking time has been updated:",
                        recipe_to_edit.cooking_time,
                        "minutes",
                    )
                else:
                    print()
                    print("*" * 30)
                    print("Invalid cooking time. Please try again.")
                    print("*" * 30)
                    print()
            else:
                print("Invalid choice. Please try again.")


# delete a recipe
def delete_recipe():
    print("=" * 30)
    print("Delete a Recipe")
    print("-" * 30)

    # check whether there are recipes in database
    if session.query(Recipe).count() == 0:
        print("\n You don\t have any recipes yet! Try creating a new recipe.")
        return None
    else:
        results = session.query(Recipe.id, Recipe.name).all()
        print("Your recipes:")
        for result in results:
            print("\n\tRecipe ID:", result[0])
            print("\tRecipe name:", result[1])

        try:
            selected_id = input("\nEnter the ID of the recipe you want to delete: ")
            recipe_to_delete = (
                session.query(Recipe).filter(Recipe.id == int(selected_id)).one()
            )
            print("You have chosen to delete", recipe_to_delete.name)
        except:
            print()
            print("*" * 30)
            print("Recipe ID is not valid.")
            print("*" * 30)
            print()
        else:
            confirmation = input(
                "\nAre you sure you want to delete this recipe (enter yes or no)? "
            )
            if confirmation == "yes":
                session.delete(recipe_to_delete)
                session.commit()
                print("\nYour recipe has been deleted.")
            elif confirmation == "no":
                print("Your recipe has not been deleted. Returning to the main menu.")
                return None
            else:
                print("There has been an error. Returning to the main menu.")
                return None


# main menu
def main_menu():
    choice = ""

    while choice != "quit":
        print("=" * 30)
        print("Main Menu")
        print("-" * 30)
        print("What would you like to do? Pick an option:\n")
        print("\t1. Create a new recipe.")
        print("\t2. Search for recipes that match an ingredient.")
        print("\t3. Update an existing recipe.")
        print("\t4. Delete a recipe.")
        print("\t5. View all recipes.")
        print("\nType 'quit' to exit the program.")

        choice = input("\nEnter your choice here: ")
        if choice == "1":
            create_recipe()
        elif choice == "2":
            search_by_ingredients()
        elif choice == "3":
            edit_recipe()
        elif choice == "4":
            delete_recipe()
        elif choice == "5":
            view_all_recipes()
        elif choice == "quit":
            print("Goodbye!")
        else:
            print("Error. Please try again.")


# run program
main_menu()
session.close()
engine.dispose()
