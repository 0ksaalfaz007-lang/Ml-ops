import joblib
import numpy as np
from datetime import datetime
from config.paths_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template, request

app = Flask(__name__)

loaded_model = joblib.load(MODEL_OUTPUT_PATH)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get form data
            booking_year = int(request.form["booking_year"])
            booking_month = int(request.form["booking_month"])
            booking_day = int(request.form["booking_day"])

            arrival_month = int(request.form["arrival_month"])
            arrival_date = int(request.form["arrival_date"])   # renamed from arrival_date for clarity

            no_of_special_request = int(request.form["no_of_special_request"])
            avg_price_per_room = float(request.form["avg_price_per_room"])
            market_segment_type = int(request.form["market_segment_type"])
            no_of_week_nights = int(request.form["no_of_week_nights"])
            no_of_weekend_nights = int(request.form["no_of_weekend_nights"])
            type_of_meal_plan = int(request.form["type_of_meal_plan"])
            room_type_reserved = int(request.form["room_type_reserved"])

            # Calculate Lead Time (in days)
            booking_date_str = f"{booking_year}-{booking_month:02d}-{booking_day:02d}"
            arrival_date_str = f"2026-{arrival_month:02d}-{arrival_date:02d}"   # Assuming arrival year is 2026 (same as default)

            booking_dt = datetime.strptime(booking_date_str, "%Y-%m-%d")
            arrival_dt = datetime.strptime(arrival_date_str, "%Y-%m-%d")

            lead_time = (arrival_dt - booking_dt).days

            if lead_time < 0:
                return render_template("index.html",
                                     prediction=None,
                                     error="Arrival date cannot be before booking date!")

            # Prepare features for model
            features = np.array([[lead_time, no_of_special_request, avg_price_per_room,
                                  arrival_month, arrival_date, market_segment_type,
                                  no_of_week_nights, no_of_weekend_nights,
                                  type_of_meal_plan, room_type_reserved]])

            prediction = loaded_model.predict(features)

            return render_template('index.html', prediction=prediction[0])

        except ValueError:
            return render_template("index.html",
                                 prediction=None,
                                 error="Please enter valid numbers in all fields.")

    return render_template("index.html", prediction=None, error=None)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)