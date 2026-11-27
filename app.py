
from flask import Flask, jsonify, request

app = Flask(__name__)

restaurants = [
    {"id": 1, "name": "Pizza House"},
    {"id": 2, "name": "Burger Point"},
    {"id": 3, "name": "Food Corner"}
]

@app.route("/")
def home():
    return jsonify({
        "message": "Online Food Ordering System"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200

@app.route("/restaurants")
def get_restaurants():
    return jsonify(restaurants), 200

@app.route("/cart/total", methods=["POST"])
def calculate_total():
    data = request.get_json(silent=True) or {}

    price = data.get("price", 0)
    quantity = data.get("quantity", 0)

    if not isinstance(price, (int, float)) or isinstance(price, bool):
        return jsonify({"error": "Invalid price"}), 400

    if not isinstance(quantity, int) or isinstance(quantity, bool):
        return jsonify({"error": "Invalid quantity"}), 400

    if price < 0 or quantity < 0:
        return jsonify({"error": "Negative values not allowed"}), 400

    total = price * quantity

    return jsonify({
        "price": price,
        "quantity": quantity,
        "total": total
    }), 200

@app.route("/orders", methods=["POST"])
def place_order():
    data = request.get_json(silent=True) or {}

    items = data.get("items", [])

    if not isinstance(items, list) or len(items) == 0:
        return jsonify({
            "error": "Cart cannot be empty"
        }), 400

    return jsonify({
        "message": "Order placed successfully",
        "order_id": 1001,
        "status": "confirmed"
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
