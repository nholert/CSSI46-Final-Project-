# CSSI46-Final-Project- CMC Hub Order Management System

This project simulates an ordering system that:

- Classifies orders by prep effort (short, medium, long)
- Uses a rotating multi-queue system to reduce wait times
- Tracks inventory with stock levels and low-stock alerts using hash tables

## How to Run:
Open the Python file
cd to your file location 
run the command python main.py 

Then, follow the instructions in the terminal to:
    - Add orders
    - View queues
    - Process orders
    - Check inventory

## Collaborators Summary: 
- Erin: created data models for the menu, inputted Hub menu items, created a system to classify orders as short/medium/long.
- Ishita: set up the queue system that adds orders to 4 queues: in-person, short, medium, and long, and rotates between each queue. 
- Matteo: set up the inventory management system using hash tables that tracks inventory of each menu item and warns if an item is at a low stock threshold. 
- Natalie: compiled everyone's code together to create an output and demo. Fixed bugs, tested code, and edited each person's section to flow as one program. Set up a demo ordering system displaying functionality of backend code. 
