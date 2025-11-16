from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

inventory = [
    {"id": 1, "name": "Laptop", "quantity": 10},
    {"id": 2, "name": "Smartphone", "quantity": 25},
    {"id": 3, "name": "Tablet", "quantity": 15}             
]


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)

#post
@app.route("/inventory", methods=["POST"])
def add_inventory_item():
    data = request.get_json()

    # Generate a new ID
    new_id = max(item["id"] for item in inventory) + 1 if inventory else 1

    new_item = {
        "id": new_id,
        "name": data["name"],
        "quantity": data.get("quantity", 0)
    }

    inventory.append(new_item)
    return jsonify(new_item), 201
#get
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    #find it
    item = next((item for item in inventory if item["id"] == item_id), None)

    if item is None:
        return jsonify({"error": "Item not found"}), 404
    else:
        return jsonify(item), 200
    
#patch
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    data = request.get_json()

    item = next((item for item in inventory if item["id"] == item_id), None)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    if "name" in data:
        item["name"] = data["name"]

    if "quantity" in data:
        item["quantity"] = data["quantity"]

    return jsonify(item), 200

#delete
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    global inventory
    item = next((item for item in inventory if item["id"] == item_id), None)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    inventory = [item for item in inventory if item["id"] != item_id]

    return jsonify({"message": "Item deleted"}), 200



#getting the actual data
@app.route("/lookup", methods=["GET"])
def lookup_product():
    product_name = request.args.get("name")

    if not product_name:
        return jsonify({"error": "Missing 'name' parameter"}), 400

    
    url = f"https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": product_name,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    
    if "products" not in data or len(data["products"]) == 0:
        return jsonify({"error": "Product not found"}), 404

    first = data["products"][0]

    result = {
        "product_name": first.get("product_name"),
        "brand": first.get("brands"),
        "ingredients_text": first.get("ingredients_text"),
        "nutriscore": first.get("nutriscore_grade")
    }

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)


    