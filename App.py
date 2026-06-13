from flask import Flask, request, jsonify
from woocommerce import API

app = Flask(__name__)

# WooCommerce API Configuration
wcapi = API(
    url="https://yourwebsite.com",
    consumer_key="ck_xxxxxxxxxxxxxxxxx",
    consumer_secret="cs_xxxxxxxxxxxxxxxxx",
    version="wc/v3",
    timeout=30
)

# =========================
# HOME ROUTE
# =========================
@app.route("/")
def home():
    return jsonify({
        "message": "Professional E-Commerce API Running"
    })


# =========================
# GET ALL PRODUCTS
# =========================
@app.route("/products", methods=["GET"])
def get_products():
    try:
        products = wcapi.get("products").json()
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# ADD NEW PRODUCT
# =========================
@app.route("/add-product", methods=["POST"])
def add_product():
    data = request.get_json()

    required_fields = [
        "name",
        "price",
        "description",
        "short_description",
        "category_id"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    product_data = {
        "name": data["name"],
        "type": "simple",
        "regular_price": str(data["price"]),
        "description": data["description"],
        "short_description": data["short_description"],
        "categories": [
            {
                "id": data["category_id"]
            }
        ]
    }

    try:
        result = wcapi.post("products", product_data).json()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# UPDATE STOCK
# =========================
@app.route("/update-stock/<int:product_id>", methods=["PUT"])
def update_stock(product_id):
    data = request.get_json()

    if not data or "stock" not in data:
        return jsonify({"error": "stock field required"}), 400

    stock_data = {
        "manage_stock": True,
        "stock_quantity": int(data["stock"])
    }

    try:
        result = wcapi.put(
            f"products/{product_id}",
            stock_data
        ).json()

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# GET ORDERS
# =========================
@app.route("/orders", methods=["GET"])
def get_orders():
    try:
        orders = wcapi.get("orders").json()
        return jsonify(orders)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# UPDATE ORDER STATUS
# =========================
@app.route("/update-order/<int:order_id>", methods=["PUT"])
def update_order(order_id):

    data = request.get_json()
    status = data.get("status", "completed")

    try:
        result = wcapi.put(
            f"orders/{order_id}",
            {"status": status}
        ).json()

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# DELETE PRODUCT
# =========================
@app.route("/delete-product/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):

    try:
        result = wcapi.delete(
            f"products/{product_id}",
            params={"force": True}
        ).json()

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
