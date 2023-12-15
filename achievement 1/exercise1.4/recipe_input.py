import pickle

def calc_difficulty(cooking_time, ingredients):
  if cooking_time < 10 and len(ingredients) < 4:
    difficulty = 'Easy'
  elif cooking_time < 10 and len(ingredients) >= 4:
    difficulty = 'Medium'
  elif cooking_time >= 10 and len(ingredients) < 4:
    difficulty = 'Intermediate'
  elif cooking_time >= 10 and len(ingredients) >= 4:
    difficulty = 'Hard'
  return difficulty

def take_recipe():
  recipe_name = input('Recipe name: ')
  cooking_time = int(input('Cooking time in minutes: '))
  ingredients = list(input('Ingredients: ').lower().split(', '))
 
  recipe = {
    'Name': recipe_name,
    'Cooking time': cooking_time,
    'Ingredients': ingredients,
    'Difficulty': calc_difficulty(cooking_time, ingredients)
  }

  return recipe

filename = input('Filename where recipes are stored: ')

try: 
  recipe_file = open(filename, 'rb')
  data = pickle.load(recipe_file)
except FileNotFoundError:
  print('Creating file to store recipes: ' + filename)
  data = {
    'recipes_list': [],
    'all_ingredients': []
  }
except:
  print('Creating file to store recipes: ' + filename)
  data = {
    'recipes_list': [],
    'all_ingredients': []
  }
finally:
  recipes_list = data['recipes_list']
  all_ingredients = data['all_ingredients']
  recipe_file.close()

recipes_list_length = int(input('How many recipes do you want to add? '))

for i in range(recipes_list_length):
  recipe = take_recipe()
  recipes_list.append(recipe)
  for ingredient in recipe['Ingredients']:
    if not ingredient in all_ingredients:
      all_ingredients.append(ingredient)

data = {
  'recipes_list': recipes_list,
  'all_ingredients': all_ingredients
}

recipe_file = open(filename, 'wb')
pickle.dump(data, recipe_file)
recipe_file.close()