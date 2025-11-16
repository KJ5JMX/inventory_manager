Inventory Manager – Flask API + CLI Tool

Inventory management application featuring:
• A Flask REST API with full CRUD routes
• External API integration using OpenFoodFacts
• Python CLI tool with commands for listing, adding, looking up, and enriched adding
• Automated test suite using pytest
• Git branching workflow following best practices

⸻

Features

Full CRUD Inventory API
• GET /inventory – list all items
• POST /inventory – add new item
• GET /inventory/<id> – get single item
• PATCH /inventory/<id> – update item
• DELETE /inventory/<id> – delete item

External API Integration
• /lookup?name= queries the OpenFoodFacts API
• CLI “enriched add” merges real product data (name + brand) into inventory

Python CLI Tool

Commands include:
• list
• add <name> <quantity>
• lookup <product_name>
• enrich-add <product_name> <quantity>

Automated Testing
• API tests
• CLI tests
• All tests run with pytest
