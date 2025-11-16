import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app

# Setup Flask test client
client = app.test_client()


def test_get_inventory():
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 3


def test_post_inventory():
    payload = {"name": "TestItem", "quantity": 7}
    response = client.post("/inventory", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "TestItem"
    assert data["quantity"] == 7


def test_get_inventory_item():
    response = client.get("/inventory/1")
    data = response.get_json()
    assert response.status_code in (200, 404)  # item may have been deleted
    # If exists, ensure structure:
    if response.status_code == 200:
        assert "name" in data
        assert "quantity" in data


def test_lookup_route():
    response = client.get("/lookup?name=Nutella")
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.get_json()
        assert "product_name" in data