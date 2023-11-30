class ShoppingList:
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []

    def add_item(self, item):
        if item not in self.shopping_list:
            self.shopping_list.append(item)

    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)

    def view_list(self):
        print(f"{self.list_name}:")
        for item in self.shopping_list:
            print(f"\t{item}")

pet_store_list = ShoppingList("Pet Store Shopping List")

items = ["dog food", "frisbee", "bowl", "collars", "flea collars"]

for item in items:
    pet_store_list.add_item(item)

pet_store_list.remove_item("flea collars")

pet_store_list.add_item("frisbee")          

pet_store_list.view_list()
