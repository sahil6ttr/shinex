def calculate_price(vehicle_category, service_type,
                    pickup_km=0, monsoon=False, monthly_pass=False):

    CAR_PRICES = {
        "Hatchback": {"Basic": 200, "Complete": 350, "Premium": 500},
        "Sedan": {"Basic": 250, "Complete": 450, "Premium": 650},
        "SUV": {"Basic": 350, "Complete": 550, "Premium": 800},
        "Luxury": {"Basic": 500, "Complete": 800, "Premium": 1200}
    }

    BIKE_PRICES = {
        "Scooter": {"Basic": 80, "Complete": 120},
        "Commuter": {"Basic": 100, "Complete": 150},
        "Sports": {"Basic": 120, "Complete": 180},
        "Superbike": {"Basic": 150, "Complete": 350}
    }

    price = 0

    if vehicle_category in CAR_PRICES:
        price = CAR_PRICES[vehicle_category][service_type]

    elif vehicle_category in BIKE_PRICES:
        price = BIKE_PRICES[vehicle_category][service_type]

    pickup_charge = 0
    if pickup_km > 1:
        pickup_charge = max(30, int(pickup_km * 15))

    surcharge = 50 if monsoon and vehicle_category == "SUV" else 0

    total = price + pickup_charge + surcharge

    if monthly_pass:
        total *= 0.85   # 15% discount

    return int(total)
