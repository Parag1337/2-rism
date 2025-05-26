from flask import Flask, render_template, request, redirect, url_for
import json
import os
import datetime

app = Flask(__name__, 
    static_folder='../',  # Keep this as is
    static_url_path='',   # Add this line
    template_folder='../templates')

# Load travel data from JSON file
def load_travel_data():
    try:
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to the main project directory
        project_dir = os.path.dirname(script_dir)
        # Path to the JSON file
        json_path = os.path.join(project_dir, 'travel_data.json')
        
        with open(json_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading travel data: {e}")
        return {"destinations": []}

@app.route('/')
def index():
    # Serve the static index.html file from the root directory
    return app.send_static_file('Index.html')

@app.route('/search_flights', methods=['POST'])
def search_flights():
    # Get form data
    departure = request.form.get('departure')
    destination = request.form.get('location')
    travel_date = request.form.get('date')
    guests = request.form.get('guests')
    
    # Load travel data
    travel_data = load_travel_data()
    
    # Find matching destination
    matching_destination = None
    for dest in travel_data['destinations']:
        if dest['name'] == destination.split(',')[0].strip():  # Extract destination name before the comma
            matching_destination = dest
            break
    
    # Find matching flights
    matching_flights = []
    if matching_destination:
        for flight in matching_destination['flights']:
            if flight['departure'] == departure:
                # Add formatted date to the flight data
                flight_with_date = flight.copy()
                flight_with_date['travel_date'] = travel_date
                flight_with_date['guests'] = guests
                flight_with_date['destination'] = matching_destination['name']
                matching_flights.append(flight_with_date)
    
    # If no flights found, send an appropriate message
    if not matching_flights:
        return render_template('no_flights.html', 
                               departure=departure, 
                               destination=destination, 
                               date=travel_date)
    
    # Render the results page with the matching flights
    return render_template('flight_results.html', 
                           flights=matching_flights, 
                           departure=departure, 
                           destination=destination,
                           date=travel_date,
                           guests=guests)

@app.route('/book_flight', methods=['POST'])
def book_flight():
    # Get form data
    flight_no = request.form.get('flight_no')
    departure = request.form.get('departure')
    destination = request.form.get('destination')
    travel_date = request.form.get('date')
    guests = request.form.get('guests')
    
    # Here you would typically save the booking to a database
    # For now, we'll just render a booking confirmation page
    return render_template('booking_confirmation.html',
                          flight_no=flight_no,
                          departure=departure,
                          destination=destination,
                          date=travel_date,
                          guests=guests)

if __name__ == '__main__':
    app.run(debug=True)