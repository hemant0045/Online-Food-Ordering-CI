
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == \
        "Online Food Ordering System"


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_restaurant_list(client):
    response = client.get("/restaurants")

    assert response.status_code == 200
    assert len(response.json) == 3


def test_restaurant_name(client):
    response = client.get("/restaurants")

    assert response.json[0]["name"] == "Pizza House"


def test_cart_total(client):
    response = client.post(
        "/cart/total",
        json={"price": 100, "quantity": 2}
    )

    assert response.status_code == 200
    assert response.json["total"] == 200


def test_cart_total_with_quantity(client):
    response = client.post(
        "/cart/total",
        json={"price": 150, "quantity": 3}
    )

    assert response.json["total"] == 450


def test_cart_negative_price(client):
    response = client.post(
        "/cart/total",
        json={"price": -100, "quantity": 2}
    )

    assert response.status_code == 400


def test_cart_negative_quantity(client):
    response = client.post(
        "/cart/total",
        json={"price": 100, "quantity": -2}
    )

    assert response.status_code == 400


def test_cart_invalid_price(client):
    response = client.post(
        "/cart/total",
        json={"price": "abc", "quantity": 2}
    )

    assert response.status_code == 400


def test_cart_invalid_quantity(client):
    response = client.post(
        "/cart/total",
        json={"price": 100, "quantity": 2.5}
    )

    assert response.status_code == 400


def test_place_order(client):
    response = client.post(
        "/orders",
        json={"items": ["Pizza"]}
    )

    assert response.status_code == 201
    assert response.json["status"] == "confirmed"


def test_empty_cart_order(client):
    response = client.post(
        "/orders",
        json={"items": []}
    )

    assert response.status_code == 400


def test_order_id(client):
    response = client.post(
        "/orders",
        json={"items": ["Burger"]}
    )

    assert response.json["order_id"] == 1001


def test_order_status(client):
    response = client.post(
        "/orders",
        json={"items": ["Pizza"]}
    )

    assert response.json["status"] == "confirmed"


def test_invalid_order_request(client):
    response = client.post(
        "/orders",
        json={}
    )

    assert response.status_code == 400
