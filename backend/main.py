# CMC Hub Order Management System 
# CSCI 46 Final Project 
# comment


# 1.) Order sorting using Queue/Linked List 

# Erin - Create the menu data models 
"""
- add all real menu items (drinks, bakery, grill)
- Assign each item a prep category or time estimate (short, medium, long)
""" 

# Person 2 - Order sorting system using queue/linked list 
"""
- use queue/linked list to sort orders based on a rotation between in-person orders, short orders, 
  medium orders, and long orders

"""

# 2.) Inventory management using a Hash Table - Ishita

# Person 3 - Inventory managaement using hash table 
"""
- add all real menu items (drinks, bakery, grill)
- for each item, map: 
     - number of times ordered
     - ingredients required
     - current stock
     - reorder threshold
            Example:
            inventory["burger"] = {
            "timesOrdered": 120,
            "stock": 35,
            "reorderThreshold": 20
"""

# -----------------------------------
# Person 3: Inventory Management
# CMC Hub Order Management System
# -----------------------------------

class HashTable:
    def __init__(self, size=50):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return sum(ord(char) for char in key) % self.size

    def set(self, key, value):
        index = self._hash(key)
        bucket = self.table[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))

    def get(self, key):
        index = self._hash(key)
        bucket = self.table[index]

        for existing_key, value in bucket:
            if existing_key == key:
                return value
        return None

    def keys(self):
        all_keys = []
        for bucket in self.table:
            for key, _ in bucket:
                all_keys.append(key)
        return all_keys

    def items(self):
        all_items = []
        for bucket in self.table:
            for key, value in bucket:
                all_items.append((key, value))
        return all_items


class InventoryManager:
    def __init__(self):
        self.inventory = HashTable()
        self.load_menu_items()

    def load_menu_items(self):
        menu_items = {
            # Drinks
            "coffee": {
                "category": "drink",
                "timesOrdered": 0,
                "ingredients": {"coffee beans": 1, "water": 1},
                "stock": 50,
                "reorderThreshold": 10
            },
            "latte": {
                "category": "drink",
                "timesOrdered": 0,
                "ingredients": {"espresso": 1, "milk": 1},
                "stock": 40,
                "reorderThreshold": 8
            },
            "matcha": {
                "category": "drink",
                "timesOrdered": 0,
                "ingredients": {"matcha": 1, "milk": 1},
                "stock": 30,
                "reorderThreshold": 6
            },
            "iced tea": {
                "category": "drink",
                "timesOrdered": 0,
                "ingredients": {"tea concentrate": 1, "ice": 1},
                "stock": 35,
                "reorderThreshold": 7
            },

            # Bakery
            "croissant": {
                "category": "bakery",
                "timesOrdered": 0,
                "ingredients": {"croissant dough": 1, "butter": 1},
                "stock": 25,
                "reorderThreshold": 5
            },
            "muffin": {
                "category": "bakery",
                "timesOrdered": 0,
                "ingredients": {"muffin batter": 1},
                "stock": 20,
                "reorderThreshold": 5
            },
            "cookie": {
                "category": "bakery",
                "timesOrdered": 0,
                "ingredients": {"cookie dough": 1},
                "stock": 30,
                "reorderThreshold": 6
            },

            # Grill
            "burger": {
                "category": "grill",
                "timesOrdered": 0,
                "ingredients": {"bun": 1, "patty": 1, "lettuce": 1, "cheese": 1},
                "stock": 35,
                "reorderThreshold": 10
            },
            "quesadilla": {
                "category": "grill",
                "timesOrdered": 0,
                "ingredients": {"tortilla": 1, "chicken": 1, "cheese": 2, "avocado": 1},
                "stock": 30,
                "reorderThreshold": 8
            },
            "grilled cheese": {
                "category": "grill",
                "timesOrdered": 0,
                "ingredients": {"bread": 2, "cheese": 2, "butter": 1},
                "stock": 22,
                "reorderThreshold": 5
            },
            "fries": {
                "category": "grill",
                "timesOrdered": 0,
                "ingredients": {"potatoes": 1, "oil": 1, "salt": 1},
                "stock": 40,
                "reorderThreshold": 10
            } 
        }

        for item_name, item_data in menu_items.items():
            self.inventory.set(item_name, item_data)

    def add_item(self, item_name, category, ingredients, stock, reorder_threshold):
        item_data = {
            "category": category,
            "timesOrdered": 0,
            "ingredients": ingredients,
            "stock": stock,
            "reorderThreshold": reorder_threshold
        }
        self.inventory.set(item_name, item_data)

    def place_order(self, item_name, quantity=1):
        item = self.inventory.get(item_name)

        if item is None:
            print(f"Item '{item_name}' not found in inventory.")
            return False

        if item["stock"] < quantity:
            print(f"Not enough stock for '{item_name}'. Current stock: {item['stock']}")
            return False

        item["timesOrdered"] += quantity
        item["stock"] -= quantity
        self.inventory.set(item_name, item)

        print(f"Order placed: {quantity} x {item_name}")
        print(f"Remaining stock: {item['stock']}")

        if item["stock"] <= item["reorderThreshold"]:
            print(f"Warning: '{item_name}' is at or below reorder threshold.")

        return True

    def restock_item(self, item_name, amount):
        item = self.inventory.get(item_name)

        if item is None:
            print(f"Item '{item_name}' not found in inventory.")
            return

        item["stock"] += amount
        self.inventory.set(item_name, item)
        print(f"Restocked '{item_name}' by {amount}. New stock: {item['stock']}")

    def get_item_info(self, item_name):
        item = self.inventory.get(item_name)

        if item is None:
            print(f"Item '{item_name}' not found.")
            return None

        return item

    def low_stock_items(self):
        low_stock = []

        for item_name, item_data in self.inventory.items():
            if item_data["stock"] <= item_data["reorderThreshold"]:
                low_stock.append((item_name, item_data["stock"], item_data["reorderThreshold"]))

        return low_stock

    def most_ordered_items(self):
        items = self.inventory.items()
        return sorted(items, key=lambda pair: pair[1]["timesOrdered"], reverse=True)

    def print_inventory(self):
        print("\n--- Current Inventory ---")
        for item_name, item_data in self.inventory.items():
            print(f"{item_name}:")
            print(f"  Category: {item_data['category']}")
            print(f"  Times Ordered: {item_data['timesOrdered']}")
            print(f"  Ingredients: {item_data['ingredients']}")
            print(f"  Stock: {item_data['stock']}")
            print(f"  Reorder Threshold: {item_data['reorderThreshold']}")
            print()

    def print_low_stock_report(self):
        print("\n--- Low Stock Report ---")
        low_stock = self.low_stock_items()

        if not low_stock:
            print("No items are low in stock.")
            return

        for item_name, stock, threshold in low_stock:
            print(f"{item_name}: stock = {stock}, reorder threshold = {threshold}")

# Example test 
if __name__ == "__main__":
    manager = InventoryManager()

    manager.print_inventory()

    manager.place_order("burger", 3)
    manager.place_order("latte", 2)
    manager.place_order("fries", 5)
    manager.place_order("croissant", 21)   # should trigger low stock warning
    manager.place_order("bagel", 30)       # should fail (not enough stock)

    manager.print_low_stock_report()

    print("\n--- Most Ordered Items ---")
    for item_name, item_data in manager.most_ordered_items():
        print(f"{item_name}: {item_data['timesOrdered']} orders")

    manager.restock_item("croissant", 10)
    manager.print_low_stock_report()

# Natalie - Testing, Program Flow
"""
Make sure the program flows, tie everything together 
Create test cases and make sure all the functions work, fix bigs 
use backend functions to display an output for the demo 
"""
