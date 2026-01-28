from flask import Flask, request, jsonify
from db import get_connection
from price_engine import calculate_price

app = Flask(__name__)

@app.route("/book", methods=["POST"])
def create_booking():
    data = request.json

    # Auto calculate price
    total_price = calculate_price(
        vehicle_category=data["vehicle_category"],
        service_type=data["service_type"],
        pickup_km=data.get("pickup_km", 0),
        monsoon=data.get("monsoon", False),
        monthly_pass=data.get("monthly_pass", False)
    )

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO bookings
    (vehicle_category, service_type, price, booking_date, start_time, end_time)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        data["vehicle_category"],
        data["service_type"],
        total_price,
        data["booking_date"],
        data["start_time"],
        data["end_time"]
    )

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "✅ Booking Confirmed!",
        "total_price": total_price
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
