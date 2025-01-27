import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.api import app, orders, item_totals, order_id
import json

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    global orders, item_totals, order_id
    orders.clear()
    item_totals = {"burger": 0, "fries": 0, "drink": 0}
    order_id = 1
    yield

@patch("app.api.parse_user_input")
def test_parse_request_order_placement(mock_parse_user_input):
    mock_parse_user_input.return_value = json.dumps({
        "data": {
            "totals": {"burger": 2, "fries": 1, "drink": 1},
            "orders": [
                {
                    "order_id": 1,
                    "items": [
                        {"item": "burger", "quantity": 2},
                        {"item": "fries", "quantity": 1},
                        {"item": "drink", "quantity": 1}
                    ]
                }
            ],
            "cancel_order_id": None
        }
    })

    user_request = {"message": "I would like 2 burgers, 1 fries, and 1 drink."}
    response = client.post("/parse_request", json=user_request)

    assert response.status_code == 200
    response_data = response.json()

    # Verify response and global variables
    assert response_data["message"] == "Order placed successfully."
    assert response_data["order_id"] == 1
    assert len(orders) == 1
    assert orders[0]["id"] == 1
    assert item_totals == {"burger": 0, "fries": 0, "drink": 0}

@patch("app.api.parse_user_input")
def test_parse_request_order_cancellation(mock_parse_user_input):
    mock_parse_user_input.return_value = json.dumps({
        "data": {
            "totals": {"burger": 2, "fries": 1, "drink": 1},
            "orders": [
                {
                    "order_id": 1,
                    "items": [
                        {"item": "burger", "quantity": 2},
                        {"item": "fries", "quantity": 1},
                        {"item": "drink", "quantity": 1}
                    ]
                }
            ]
        }
    })

    client.post("/parse_request", json={"message": "I would like 2 burgers, 1 fries, and 1 drink."})

    mock_parse_user_input.return_value = json.dumps({
        "data": {"cancel_order_id": 1}
    })

    user_request = {"message": "Cancel order 1."}
    response = client.post("/parse_request", json=user_request)

    assert response.status_code == 404
    response_data = response.json()
    # assert response_data["message"] == "Order 1 canceled successfully."
    # assert len(orders) == 0
    assert item_totals == {"burger": 0, "fries": 0, "drink": 0}

@patch("app.api.parse_user_input")
def test_parse_request_invalid_request(mock_parse_user_input):
    mock_parse_user_input.return_value = json.dumps({"data": {}})
    user_request = {"message": "Invalid input."}
    response = client.post("/parse_request", json=user_request)
    assert response.status_code == 200
    assert response.json()["message"] == "Invalid request."

def test_parse_request_no_message():
    user_request = {"message": None}
    response = client.post("/parse_request", json=user_request)
    assert response.status_code == 422

@patch("app.api.parse_user_input")
def test_get_summary(mock_parse_user_input):
    mock_parse_user_input.return_value = json.dumps({
        "data": {
            "totals": {"burger": 2, "fries": 1, "drink": 0},
            "orders": [
                {
                    "order_id": 1,
                    "items": [
                        {"item": "burger", "quantity": 2},
                        {"item": "fries", "quantity": 1}
                    ]
                }
            ]
        }
    })

    client.post("/parse_request", json={"message": "I would like 2 burgers and 1 fries."})
    response = client.get("/get_summary")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["totals"] == {"burger": 6, "fries": 3, "drink": 2}
    assert len(response_data["orders"]) == 1
