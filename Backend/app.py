from flask import Flask, render_template, request, redirect, url_for, session, flash
import sys
import os

# Add the parent directory to the path so we can import myfile.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import functions from myfile.py
from myfile import (
    load_travel_data, 
    get_destinations, 
    get_flights_for_destination, 
    get_hotels_for_destination,
    get_departure_cities,
    get_destination_details,
    # New imported functions
    get_bookings_filepath,
    load_bookings,
    save_bookings,
    create_flight_booking,
    create_hotel_booking,
    get_user_bookings
)

app = Flask(__name__, 
    static_folder='../',
    static_url_path='',
    template_folder='../templates')
app.secret_key = 'your_secret_key_here'  # For session management

# User database (in a real app, this would be in a database)
users = {
    'demo@example.com': {'password': 'password123', 'name': 'Demo User'}
}

# Load bookings from JSON file
bookings_db = load_bookings()

@app.route('/')
def index():
    # Get the project directory path for the JSON file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    json_path = os.path.join(project_dir, 'travel_data.json')
    
    # Load travel data
    travel_data = load_travel_data(json_path)
    
    # Get list of destinations and departure cities for frontend dropdowns
    destinations = get_destinations(travel_data)
    departure_cities = get_departure_cities(travel_data)
    
    # Render the index template with data from JSON
    return render_template('Index.html', 
                          user_name=session.get('user_name'),
                          destinations=destinations,
                          departure_cities=departure_cities)

@app.route('/search_flights', methods=['POST'])
def search_flights():
    # Get form data
    departure = request.form.get('departure')
    destination = request.form.get('location')
    travel_date = request.form.get('date')
    guests = request.form.get('guests')
    
    # Get the project directory path for the JSON file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    json_path = os.path.join(project_dir, 'travel_data.json')
    
    # Use imported function to load travel data
    travel_data = load_travel_data(json_path)
    
    # Extract destination name before the comma
    destination_name = destination.split(',')[0].strip() if destination and ',' in destination else destination
    
    # Use imported function to get flights for the destination
    flights = get_flights_for_destination(travel_data, destination_name)
    
    # Filter flights by departure
    matching_flights = []
    for flight in flights:
        if flight['departure'] == departure:
            # Add formatted date to the flight data
            flight_with_date = flight.copy()
            flight_with_date['travel_date'] = travel_date
            flight_with_date['guests'] = guests
            matching_flights.append(flight_with_date)
    
    # If no flights found, send an appropriate message
    if not matching_flights:
        return render_template('no_flights.html', 
                               departure=departure, 
                               destination=destination_name, 
                               date=travel_date)
    
    # Render the results page with the matching flights
    return render_template('flight_results.html', 
                           flights=matching_flights, 
                           departure=departure, 
                           destination=destination_name,
                           date=travel_date,
                           guests=guests)

@app.route('/book_flight', methods=['POST'])
def book_flight():
    # Check if user is logged in
    if 'user_email' not in session:
        flash('Please log in to book a flight', 'danger')
        return redirect(url_for('login'))
    
    # Get user email from session
    user_email = session['user_email']
    
    # Create flight data dictionary from form
    flight_data = {
        'flight_no': request.form.get('flight_no'),
        'airline': request.form.get('airline'),
        'departure': request.form.get('departure'),
        'destination': request.form.get('destination'),
        'date': request.form.get('date'),
        'departure_time': request.form.get('departure_time'),
        'arrival_time': request.form.get('arrival_time'),
        'price': request.form.get('price'),
        'guests': request.form.get('guests')
    }
    
    # Use the create_flight_booking function from myfile.py
    booking_id, booking = create_flight_booking(user_email, bookings_db, flight_data)
    
    # Render the booking confirmation page
    return render_template('booking_confirmation.html',
                          booking_id=booking_id,
                          flight_no=flight_data['flight_no'],
                          airline=flight_data['airline'],
                          departure=flight_data['departure'],
                          destination=flight_data['destination'],
                          date=flight_data['date'],
                          departure_time=flight_data['departure_time'],
                          arrival_time=flight_data['arrival_time'],
                          price=flight_data['price'],
                          guests=flight_data['guests'])

@app.route('/search_hotels', methods=['POST'])
def search_hotels():
    # Get form data
    destination = request.form.get('location')
    check_in = request.form.get('check_in')
    check_out = request.form.get('check_out')
    guests = request.form.get('guests')
    
    # Get the project directory path for the JSON file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    json_path = os.path.join(project_dir, 'travel_data.json')
    
    # Use imported function to load travel data
    travel_data = load_travel_data(json_path)
    
    # Extract destination name before the comma
    destination_name = destination.split(',')[0].strip() if destination and ',' in destination else destination
    
    # Use imported function to get hotels for the destination
    hotels = get_hotels_for_destination(travel_data, destination_name)
    
    # If no hotels found, send an appropriate message
    if not hotels:
        return render_template('no_hotels.html', 
                               destination=destination, 
                               check_in=check_in,
                               check_out=check_out)
    
    # Render the results page with the matching hotels
    return render_template('hotel_result.html', 
                           hotels=hotels, 
                           destination=destination,
                           check_in=check_in,
                           check_out=check_out,
                           guests=guests)

@app.route('/book_hotel', methods=['POST'])
def book_hotel():
    # Check if user is logged in
    if 'user_email' not in session:
        flash('Please log in to book a hotel', 'danger')
        return redirect(url_for('login'))
    
    # Get user email from session
    user_email = session['user_email']
    
    # Create hotel data dictionary from form
    hotel_data = {
        'hotel_name': request.form.get('hotel_name'),
        'destination': request.form.get('destination'),
        'check_in': request.form.get('check_in'),
        'check_out': request.form.get('check_out'),
        'guests': request.form.get('guests'),
        'price': request.form.get('price')
    }
    
    # Use the create_hotel_booking function from myfile.py
    booking_id, booking = create_hotel_booking(user_email, bookings_db, hotel_data)
    
    # Render the booking confirmation page
    return render_template('hotel_booking_confirmation.html',
                          booking_id=booking_id,
                          hotel_name=hotel_data['hotel_name'],
                          destination=hotel_data['destination'],
                          check_in=hotel_data['check_in'],
                          check_out=hotel_data['check_out'],
                          price=hotel_data['price'],
                          guests=hotel_data['guests'])

@app.route('/api/destinations')
def api_destinations():
    # Get the project directory path for the JSON file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    json_path = os.path.join(project_dir, 'travel_data.json')
    
    # Use imported function to load travel data
    travel_data = load_travel_data(json_path)
    
    # Use imported function to get list of destinations
    destination_names = get_destinations(travel_data)
    
    destinations = []
    for name in destination_names:
        for dest in travel_data.get('destinations', []):
            if dest.get('name') == name:
                destinations.append({
                    'name': dest.get('name', ''),
                    'country': dest.get('country', ''),
                    'description': dest.get('description', ''),
                    'image': dest.get('image', '')
                })
                break
    
    return {'destinations': destinations}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users and users[email]['password'] == password:
            # Set session variables
            session['user_email'] = email
            session['user_name'] = users[email]['name']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists
        if email in users:
            flash('Email already registered', 'danger')
            return render_template('register.html')
        
        # Create new user
        users[email] = {
            'password': password,  # In production, use password hashing
            'name': f"{first_name} {last_name}"
        }
        
        # In a real app, you would save the user to a database here
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    # If GET request, display registration form
    return render_template('register.html')

@app.route('/logout')
def logout():
    # Clear session variables
    session.pop('user_email', None)
    session.pop('user_name', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if 'user_email' not in session:
        flash('Please log in to access your dashboard', 'danger')
        return redirect(url_for('login'))
    
    # Get the user's email from the session
    user_email = session['user_email']
    
    # Use the imported function to get user bookings
    user_bookings = get_user_bookings(user_email)
    
    return render_template('dashboard.html', 
                         user_name=session.get('user_name'),
                         bookings=user_bookings)

if __name__ == '__main__':
    app.run(debug=True)