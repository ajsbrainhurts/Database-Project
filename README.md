# Database-Project
For my project, I'd like to create an inventory control management system for a chain grocery store.

# Entities
Products: product name(ID), product type, price
Customers: customer name(ID), customer type(store membership?), amount paid
Store: store location, store name(ID), phone number
Orders: order ID, total cost(linked to amount paid by customer), store ID(linked to store)
Inventory: item ID (product name), quantity, restock point
Suppliers: supplier name, contact info, amount due
Employees: employee name(ID), job description, contact info
Sales: sale name(ID), product ID(item that discount is linked to), amount discounted, date of sale

# Questions / Use cases
1. I want to be able to place an order with this system and calculate the total price of said order.
2. Keep track of inventory within store and be able to restock when needed.
3. Apply sales to items and calculate the price of an order after a discount has been applied.
