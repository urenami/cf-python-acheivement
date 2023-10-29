# Recipe Collection

This repository contains a collection of simple recipes. Each recipe is stored as a dictionary with the following attributes:

- **name (str):** Recipe name
- **cooking_time (int):** Cooking time in minutes
- **preparation_time (int):** Preparation time in minutes
- **ingredients (list):** List of ingredients (str)

## Data Structure

I've chosen to use dictionaries to store recipe data because of the need to handle different data types and the flexibility of dictionaries. Dictionaries can store various data types, making them suitable for recipe names, ingredients, and cooking/preparation times. Dictionaries are also mutable, allowing for easy updates and additions.

Recipe dictionaries are stored within the `all_recipes` list, which provides a sequential and flexible structure for storing and managing multiple recipes.

## Usage

- Access recipes by using the respective dictionary within the `all_recipes` list.
- Each recipe includes attributes like the name, cooking time, preparation time, and ingredients.