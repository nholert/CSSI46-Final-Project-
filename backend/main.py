# CMC Hub Order Management System 
# CSCI 46 Final Project 
# comment


# menu.py
# CSCI 46 Final Project - CMC Hub Order Management System
#
# Notes:
# - This file models a realistic Hub-style menu for project use.
# - Each item has:
#     name
#     section
#     prep_points (base effort)
#     prep_minutes (rough estimate)
#     price
#     is_store_item (True for packaged/store items)
#
# - IMPORTANT:
#   prep_points are for INDIVIDUAL items.
#   The ORDER module should sum prep_points across all items in an order
#   and then classify the ENTIRE order as:
#       short  = 1 to 3 points
#       medium = 4 to 6 points
#       long   = 7+ points

from dataclasses import dataclass
from typing import Dict, List


def get_prep_category(total_points: int) -> str:
    """Classify a whole order based on total prep points."""
    if total_points <= 0:
        return "invalid"
    if 1 <= total_points <= 3:
        return "short"
    if 4 <= total_points <= 6:
        return "medium"
    return "long"


@dataclass(frozen=True)
class MenuItem:
    name: str
    section: str              # drinks, bakery, grill, store, etc.
    prep_points: int          # base effort for one item
    prep_minutes: int         # rough estimate for demo/simulation
    price: float
    is_store_item: bool = False


MENU_ITEMS: List[MenuItem] = [
    # COFFEE / DRINKS
    MenuItem("Coffee", "drinks", 1, 1, 2.50),
    MenuItem("Hot Tea", "drinks", 1, 1, 2.25),
    MenuItem("Iced Coffee", "drinks", 1, 1, 3.00),
    MenuItem("Espresso", "drinks", 1, 1, 2.75),
    MenuItem("Americano", "drinks", 1, 2, 3.25),
    MenuItem("Latte", "drinks", 2, 3, 4.75),
    MenuItem("Cappuccino", "drinks", 2, 3, 4.75),
    MenuItem("Mocha", "drinks", 2, 3, 5.00),
    MenuItem("Hot Chocolate", "drinks", 1, 2, 3.50),
    MenuItem("Smoothie", "drinks", 2, 4, 5.75),
    MenuItem("Milkshake", "drinks", 2, 4, 5.95),

    # BAKERY / GRAB-AND-GO
    MenuItem("Bagel", "bakery", 1, 1, 2.50),
    MenuItem("Bagel with Cream Cheese", "bakery", 1, 2, 3.25),
    MenuItem("Croissant", "bakery", 1, 1, 3.25),
    MenuItem("Muffin", "bakery", 1, 1, 3.00),
    MenuItem("Cookie", "bakery", 1, 1, 1.75),
    MenuItem("Brownie", "bakery", 1, 1, 2.25),
    MenuItem("Grilled Cheese", "bakery", 2, 4, 6.25),

    # GRILL / HOT FOOD
    MenuItem("Fries", "grill", 1, 3, 3.50),
    MenuItem("Onion Rings", "grill", 1, 4, 4.25),
    MenuItem("Chicken Wings", "grill", 3, 7, 8.95),
    MenuItem("Burger", "grill", 3, 6, 7.95),
    MenuItem("Cheeseburger", "grill", 3, 6, 8.45),
    MenuItem("Double Burger", "grill", 4, 8, 10.25),
    MenuItem("Veggie Burger", "grill", 3, 6, 8.25),
    MenuItem("Chicken Sandwich", "grill", 3, 6, 8.75),
    MenuItem("Grilled Sub", "grill", 3, 6, 8.95),
    MenuItem("Turkey Sandwich", "grill", 2, 4, 7.25),
    MenuItem("Club Sandwich", "grill", 3, 5, 8.50),
    MenuItem("Quesadilla", "grill", 3, 5, 7.95),
    MenuItem("Chicken Quesadilla", "grill", 4, 6, 8.95),
    MenuItem("Salad", "grill", 2, 3, 6.75),
    MenuItem("Chicken Salad", "grill", 3, 4, 8.25),

    # STORE / PACKAGED ITEMS
    # These should usually be "short" because they are grab-and-go.
    MenuItem("Bottled Water", "store", 1, 0, 2.00, True),
    MenuItem("Sparkling Water", "store", 1, 0, 2.50, True),
    MenuItem("Soda", "store", 1, 0, 2.50, True),
    MenuItem("Juice", "store", 1, 0, 3.00, True),
    MenuItem("Energy Drink", "store", 1, 0, 3.75, True),
    MenuItem("Yogurt Parfait", "store", 1, 0, 4.50, True),
    MenuItem("Fruit Cup", "store", 1, 0, 4.25, True),
    MenuItem("Chips", "store", 1, 0, 2.25, True),
    MenuItem("Granola Bar", "store", 1, 0, 1.75, True),
    MenuItem("Trail Mix", "store", 1, 0, 3.25, True),
    MenuItem("Candy", "store", 1, 0, 2.00, True),
]


MENU_BY_NAME: Dict[str, MenuItem] = {item.name: item for item in MENU_ITEMS}


def get_item(name: str) -> MenuItem | None:
    """Return a menu item by exact name, or None if missing."""
    return MENU_BY_NAME.get(name)


def items_by_section(section: str) -> List[MenuItem]:
    """Return all items in a given section."""
    return [item for item in MENU_ITEMS if item.section == section]


def calculate_order_points(item_names: List[str], customizations: int = 0) -> int:
    """
    Sum prep points for an order.
    Add +1 per customization, based on your team outline.
    """
    total = 0
    for name in item_names:
        item = get_item(name)
        if item is None:
            raise ValueError(f"Menu item not found: {name}")
        total += item.prep_points
    total += customizations
    return total


def calculate_order_minutes(item_names: List[str], customizations: int = 0) -> int:
    """
    Rough estimated prep time in minutes for an order.
    Adds 1 minute per customization for simulation purposes.
    """
    total = 0
    for name in item_names:
        item = get_item(name)
        if item is None:
            raise ValueError(f"Menu item not found: {name}")
        total += item.prep_minutes
    total += customizations
    return total


def classify_order(item_names: List[str], customizations: int = 0) -> str:
    """Return short / medium / long for the whole order."""
    total_points = calculate_order_points(item_names, customizations)
    return get_prep_category(total_points)


if __name__ == "__main__":
    # Quick test examples
    sample_order_1 = ["Coffee", "Bagel"]
    sample_order_2 = ["Burger", "Fries", "Milkshake"]
    sample_order_3 = ["Chicken Wings", "Chicken Quesadilla", "Milkshake"]

    for order in [sample_order_1, sample_order_2, sample_order_3]:
        points = calculate_order_points(order)
        minutes = calculate_order_minutes(order)
        category = classify_order(order)

        print(f"Order: {order}")
        print(f"Points: {points}")
        print(f"Estimated minutes: {minutes}")
        print(f"Category: {category}")
        print("-" * 40)

from collections import deque

class OrderManager:
  def __init__(self):
    self.in_person_queue = deque()
    self.short_queue = deque()
    self.medium_queue = deque()
    self.long_queue = deque()

    self.rotation = ["in_person", "short", "medium", "long"]
    self.index = 0

  def add_order(self, order):
    if order["source"] == "in-person":
      self.in_person_queue.append(order)
    elif order["category"] == "short":
      self.short_queue.append(order)
    elif order["category"] == "medium":
      self.medium_queue.append(order)
    elif order["category"] == "long":
      self.long_queue.append(order)

  def get_next_order(self):
    for _ in range(4):
      current = self.rotation[self.index]
      if current == "in_person" and self.in_person_queue:
        self.index = (self.index + 1) % 4
        return self.in_person_queue.popleft()
      elif current == "short" and self.short_queue:
        self.index = (self.index + 1) % 4
        return self.short_queue.popleft()
      elif current == "medium" and self.medium_queue:
        self.index = (self.index + 1) % 4
          eturn self.medium_queue.popleft()
      elif current == "long" and self.long_queue:
        self.index = (self.index + 1) % 4
        return self.long_queue.popleft()

      self.index = (self.index + 1) % 4

    return None

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
