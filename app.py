from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "inventory.json"

# Load inventory from file or create a new one
def load_inventory():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"steel": 100, "plastic": 200, "wood": 150}

# Save inventory to file
def save_inventory(inventory):
    with open(DATA_FILE, "w") as f:
        json.dump(inventory, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def home():
    inventory = load_inventory()
    message = ""

    if request.method == "POST":
        action = request.form.get("action")
        material = request.form.get("material").lower().strip()

        # Check shortage
        if action == "check":
            qty = int(request.form.get("quantity", 0))
            if material in inventory:
                available = inventory[material]
                shortage = qty - available
                message = f"Shortage: {shortage} units" if shortage > 0 else "No shortage! You have enough stock."
            else:
                message = "Material not found in inventory."

        # Restock material
        elif action == "restock":
            qty = int(request.form.get("add_quantity", 0))
            if material in inventory:
                inventory[material] += qty
                save_inventory(inventory)
                message = f"{qty} units added to {material}. Total: {inventory[material]} units."
            else:
                message = "Material not found in inventory."

        # Add new material
        elif action == "add":
            qty = int(request.form.get("new_quantity", 0))
            if material not in inventory:
                inventory[material] = qty
                save_inventory(inventory)
                message = f"New material '{material}' added with {qty} units."
            else:
                message = "Material already exists!"

    return render_template("index.html", inventory=inventory, message=message)

if __name__ == "__main__":
    app.run(debug=True)
