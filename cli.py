import requests
import sys

API_URL = "http://127.0.0.1:5000"


def list_inventory():
    response = requests.get(f"{API_URL}/inventory")
    data = response.json()
    print("Inventory:")
    for item in data:
        print(f"ID: {item['id']}, Name: {item['name']}, Quantity: {item['quantity']}")


def add_inventory_item(name, quantity):
    payload = {"name": name, "quantity": quantity}
    response = requests.post(f"{API_URL}/inventory", json=payload)

    if response.status_code == 201:
        data = response.json()
        print(f"Item added successfully: {data['name']} (ID {data['id']}, Qty {data['quantity']})")
    else:
        print("Failed to add item:", response.text)

def lookup_product(name):
    url = f"{API_URL}/lookup"
    params = {"name": name}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Product Lookup Result:")
        print(f"Name: {data.get('product_name')}")
        print(f"Brand: {data.get('brand')}")
        print(f"Ingredients: {data.get('ingredients_text')}")   
    else:
        print("Failed to lookup product:", response.text)

def enrich_add_item(name, quantity):
    lookup_url = f"{API_URL}/lookup"
    params = {"name": name}
    lookup_response = requests.get(lookup_url, params=params)

    if lookup_response.status_code == 200:
        product = lookup_response.json()
    else:
        print("Lookup failed:", lookup_response.text)
        return
    
    real_name = product.get("product_name") or name 
    brand = product.get("brand") or "Unknown"

    final_name = f"{real_name} ({brand})"   

    payload = {"name": final_name, "quantity": quantity}

    add_response = requests.post(f"{API_URL}/inventory", json=payload)
    
    if add_response.status_code == 201:
          added = add_response.json()
          print(f"Enriched item added:")
          print(f"ID: {added['id']}")
          print(f"Name: {added['name']}")
          print(f"Quantity: {added['quantity']}")
    else:
            print("Failed to add enriched item:", add_response.text)
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cli.py <command>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        list_inventory()

    elif command == "add":
        if len(sys.argv) < 4:
            print("Usage: python cli.py add <name> <quantity>")
            sys.exit(1)
        name = sys.argv[2]
        quantity = int(sys.argv[3])
        add_inventory_item(name, quantity)

    elif command == "lookup":
        if len(sys.argv) < 3:
            print("Usage: python cli.py lookup <product_name>")
            sys.exit(1)
        name = sys.argv[2]
        lookup_product(name)
    
    elif command == "enrich-add":
        if len(sys.argv) < 4:
            print("Usage: python cli.py enrich-add <name> <quantity>")
            sys.exit(1)

        name = sys.argv[2]
        quantity = int(sys.argv[3])
        enrich_add_item(name, quantity)

    else:
        print(f"Unknown command: {command}")