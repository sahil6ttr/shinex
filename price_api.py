from flask import Flask, request, jsonify
from price_engine import calculate_price

app = Flask(__name__)

@app.route("/price", methods=["POST"])
def price():
    data = request.json

    total = calculate_price(
        vehicle_category=data["vehicle_category"],
        service_type=data["service_type"],
        pickup_km=data.get("pickup_km", 0),
        monsoon=data.get("monsoon", False),
        monthly_pass=data.get("monthly_pass", False)
    )

    return jsonify({"total_price": total})

if __name__ == "__main__":
    app.run(debug=True, port=5002)
