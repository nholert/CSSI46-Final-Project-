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
