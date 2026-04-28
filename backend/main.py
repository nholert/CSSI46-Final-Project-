# CSCI 46 Final Project 
# CMC Hub Order Management System 


# This file simulates an ordering system that classifies orders by prep effort,
# processes them using a rotating multi-queue (instead of FIFO),
# and tracks inventory using a hash table with low-stock alerts. 

from dataclasses import dataclass
from typing import Dict, List
from collections import deque


# PART I: inputting the Hub Menu, categorizing orders by prep time 

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


# - Each item has:
#     name
#     section
#     prep_points (base effort)
#     prep_minutes (rough estimate)
#     price
#     is_store_item (True for packaged/store items)

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
    MenuItem("Burger", "grill", 3, 6, 7.95),
    MenuItem("Cheeseburger", "grill", 3, 6, 8.45),
    MenuItem("Chicken Sandwich", "grill", 3, 6, 8.75),
    MenuItem("Turkey Sandwich", "grill", 2, 4, 7.25),
    MenuItem("Sandwich", "grill", 3, 5, 8.50),
    MenuItem("Quesadilla", "grill", 3, 5, 7.95),
    MenuItem("Chicken Quesadilla", "grill", 4, 6, 8.95),

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
    MenuItem("Salad", "store", 1, 0, 6.75, True),
    MenuItem("Chicken Salad", "s0re", 1, 0, 6.75, True),
]


MENU_BY_NAME: Dict[str, MenuItem] = {item.name.lower(): item for item in MENU_ITEMS}


def get_item(name: str):
    return MENU_BY_NAME.get(name.lower())


def calculate_order_points(item_names: List[str], customizations: int = 0) -> int:
    total = 0
    for name in item_names:
        item = get_item(name)
        if item is None:
            raise ValueError(f"Menu item not found: {name}")
        total += item.prep_points
    return total + customizations


def calculate_order_minutes(item_names: List[str], customizations: int = 0) -> int:
    total = 0
    for name in item_names:
        item = get_item(name)
        if item is None:
            raise ValueError(f"Menu item not found: {name}")
        total += item.prep_minutes
    return total + customizations


def calculate_order_total(item_names: List[str]) -> float:
    total = 0
    for name in item_names:
        item = get_item(name)
        if item is None:
            raise ValueError(f"Menu item not found: {name}")
        total += item.price
    return total


def classify_order(item_names: List[str], customizations: int = 0) -> str:
    total_points = calculate_order_points(item_names, customizations)
    return get_prep_category(total_points)


# Part II: Order Manager - keeping queues of orders to minimize wait time
# orders rotate between four queues: in-person, short, medium, and long orders

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
        else:
            raise ValueError("Invalid order category or source.")

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
        return self.medium_queue.popleft()
      elif current == "long" and self.long_queue:
        self.index = (self.index + 1) % 4
        return self.long_queue.popleft()

      self.index = (self.index + 1) % 4

    return None

# Part III: Inventory Manager - Tracks inventory stock, reorder thresholds, and times ordered. 
# Can place orders, restock, print inventory, and report low-stock items
class HashTable:
    def __init__(self, size=50):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return sum(ord(char) for char in key) % self.size

    def set(self, key, value):
        key = key.lower()
        index = self._hash(key)
        bucket = self.table[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))

    def get(self, key):
        key = key.lower()
        index = self._hash(key)
        bucket = self.table[index]

        for existing_key, value in bucket:
            if existing_key == key:
                return value

        return None

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
        for item in MENU_ITEMS:
            item_data = {
                "category": item.section,
                "timesOrdered": 0,
                "stock": 7, # setting the stock low for the demo to demonstrate low stock warning
                "reorderThreshold": 5
            }
            self.inventory.set(item.name, item_data)

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

        if item["stock"] <= item["reorderThreshold"]:
            print(f"Warning: '{item_name}' is at or below reorder threshold.")

        return True

    def process_order_inventory(self, item_names):
        for item_name in item_names:
            success = self.place_order(item_name, 1)
            if not success:
                print(f"Could not process inventory for: {item_name}")

    def low_stock_items(self):
        low_stock = []

        for item_name, item_data in self.inventory.items():
            if item_data["stock"] <= item_data["reorderThreshold"]:
                low_stock.append(
                    (item_name, item_data["stock"], item_data["reorderThreshold"])
                )

        return low_stock

    def most_ordered_items(self):
        items = self.inventory.items()
        return sorted(items, key=lambda pair: pair[1]["timesOrdered"], reverse=True)

    def print_low_stock_report(self):
        print("\n--- Low Stock Report ---")
        low_stock = self.low_stock_items()

        if not low_stock:
            print("No items are low in stock.")
            return

        for item_name, stock, threshold in low_stock:
            print(f"{item_name}: stock = {stock}, reorder threshold = {threshold}")
    

# Part IV: Program Output // Demo


def create_order(order_id, customer_name, source, item_names, customizations=0):
    category = classify_order(item_names, customizations)
    points = calculate_order_points(item_names, customizations)
    minutes = calculate_order_minutes(item_names, customizations)
    total_price = calculate_order_total(item_names)

    return {
        "order_id": order_id,
        "customer_name": customer_name,
        "source": source,
        "items": item_names,
        "customizations": customizations,
        "category": category,
        "prep_points": points,
        "prep_minutes": minutes,
        "total_price": total_price
    }


def print_order(order):
    print(f"\nOrder #{order['order_id']} for {order['customer_name']}")
    print(f"Source: {order['source']}")
    print(f"Items: {order['items']}")
    print(f"Prep Points: {order['prep_points']}")
    print(f"Estimated Prep Time: {order['prep_minutes']} minutes")
    print(f"Category: {order['category']}")
    print(f"Total Price: ${order['total_price']:.2f}")


def print_queues(order_manager):
    print("\n--- Current Queue Status ---")
    print(f"In-Person Queue: {[order['order_id'] for order in order_manager.in_person_queue]}")
    print(f"Short Queue: {[order['order_id'] for order in order_manager.short_queue]}")
    print(f"Medium Queue: {[order['order_id'] for order in order_manager.medium_queue]}")
    print(f"Long Queue: {[order['order_id'] for order in order_manager.long_queue]}")
    print("----------------------------")


def show_menu():
    print("\n--- MENU ---")
    for item in MENU_ITEMS:
        print(f"{item.name} - ${item.price:.2f} | {item.prep_points} prep points")


def run_order_demo():
    order_manager = OrderManager()
    inventory_manager = InventoryManager()
    order_id = 1

    print("\nWelcome to the CMC Hub Order Management Demo!")

    while True:
        print("\n1. Show menu")
        print("2. Add a new order")
        print("3. Show current queues")
        print("4. Process all orders")
        print("5. Show inventory report")
        print("6. Show most ordered items")
        print("7. Exit demo")

        choice = input("\nChoose an option: ")

        if choice == "1":
            show_menu()

        elif choice == "2":
            customer_name = input("Customer name: ")

            source = input("Source, enter 'in-person' or 'online': ").lower()
            while source not in ["in-person", "online"]:
                source = input("Invalid. Enter 'in-person' or 'online': ").lower()

            items_input = input("Enter item names separated by commas: ")
            item_names = [item.strip() for item in items_input.split(",")]

            try:
                customizations = int(input("Number of customizations: "))
            except ValueError:
                customizations = 0

            try:
                order = create_order(
                    order_id,
                    customer_name,
                    source,
                    item_names,
                    customizations
                )

                order_manager.add_order(order)

                print("\nOrder added successfully.")
                print_order(order)

                if source == "in-person":
                    print("This order was placed in the IN-PERSON queue.")
                else:
                    print(f"This order was placed in the {order['category'].upper()} queue.")

                print_queues(order_manager)
                order_id += 1

            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "3":
            print_queues(order_manager)

        elif choice == "4":
          print("\n--- Auto-Processing All Orders ---")

          processed_count = 0

          while True:
              next_order = order_manager.get_next_order()

              if next_order is None:
                  break

              processed_count += 1

              print(f"\nStep {processed_count}:")
              print(f"Preparing Order #{next_order['order_id']}")
              print(f"Customer: {next_order['customer_name']}")
              print(f"Items: {next_order['items']}")

              if next_order["source"] == "in-person":
                  print("Pulled from: IN-PERSON queue")
              else:
                  print(f"Pulled from: {next_order['category'].upper()} queue")

              print(f"Prep points: {next_order['prep_points']}")
              print(f"Estimated prep time: {next_order['prep_minutes']} minutes")

              inventory_manager.process_order_inventory(next_order["items"])

              print_queues(order_manager)

          print(f"\nFinished processing {processed_count} orders.")

        elif choice == "5":
            inventory_manager.print_low_stock_report()

        elif choice == "6":
            print("\n--- Most Ordered Items ---")
            for item_name, item_data in inventory_manager.most_ordered_items()[:10]:
                print(f"{item_name}: {item_data['timesOrdered']} orders")

        elif choice == "7":
            print("\nDemo ended.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    run_order_demo()
