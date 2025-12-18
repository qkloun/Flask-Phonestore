# Welcome
A simple Flask-based web application for managing a smartphone inventory and shopping cart system.

## Features
- 🛒 **Shopping Cart Management** - Add, update, and remove items from your cart
- 👤 **Multi-User Support** - Individual carts for different user accounts via sessions
- 💾 **Persistent Storage** - Cart and inventory data saved to JSON file
- 💰 **Real-Time Price Calculation** - Automatic cart total updates
- 🔄 **Inventory Validation** - Ensures quantities don't exceed available stock
- 🧹 **Cart Reset** - Empty cart functionality for fresh starts

## Data Structure

The `inventory-data.json` file contains:
- **Inventory** - Product ID, name, price, and stock quantity
- **Carts** - User accounts with their selected items and quantities

## Prerequisites

- Python 3.x
- Flask (`pip install flask`)



