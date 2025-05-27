import json
import os
import datetime

# Data Loading and Retrieval Functions

def load_travel_data(filepath='travel_data.json'):
    """
    Load travel data from JSON file
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        dict: Travel data
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return {"destinations": [], "flights": [], "hotels": []}
    except json.JSONDecodeError:
        print(f"Error: File {filepath} is not valid JSON.")
        return {"destinations": [], "flights": [], "hotels": []}


def get_destinations(data):
    """
    Get list of destination names
    
    Args:
        data (dict): Travel data
        
    Returns:
        list: List of destination names
    """
    destinations = []
    if "destinations" in data:
        for d in data["destinations"]:
            if "name" in d:
                destinations.append(d["name"])
    return destinations


def get_flights_for_destination(data, dest_name):
    """
    Get flights for a specific destination
    
    Args:
        data (dict): Travel data
        dest_name (str): Destination name
        
    Returns:
        list: List of flights for the destination
    """
    flights = []
    if "flights" in data:
        for flight in data["flights"]:
            if flight.get("destination") == dest_name:
                flights.append(flight)
    return flights


def get_hotels_for_destination(data, dest_name):
    """
    Get hotels for a specific destination
    
    Args:
        data (dict): Travel data
        dest_name (str): Destination name
        
    Returns:
        list: List of hotels for the destination
    """
    hotels = []
    if "hotels" in data:
        for hotel in data["hotels"]:
            if hotel.get("destination") == dest_name:
                hotels.append(hotel)
    return hotels


def get_departure_cities(data):
    """
    Get unique departure cities from flight data
    
    Args:
        data (dict): Travel data
        
    Returns:
        list: List of departure cities
    """
    cities = set()
    if "flights" in data:
        for flight in data["flights"]:
            if "departure" in flight:
                cities.add(flight["departure"])
    return sorted(list(cities))


def get_destination_details(data, dest_name):
    """
    Get details for a specific destination
    
    Args:
        data (dict): Travel data
        dest_name (str): Destination name
        
    Returns:
        dict: Destination details
    """
    if "destinations" in data:
        for dest in data["destinations"]:
            if dest.get("name") == dest_name:
                return dest
    return None


# CLI Interaction Functions

def select_destination(destinations):
    """CLI function to select a destination from a list"""
    print("\nAvailable destinations:")
    for i, dest in enumerate(destinations, 1):
        print(f"{i}. {dest}")
    
    while True:
        try:
            choice = int(input("\nSelect a destination (number): "))
            if 1 <= choice <= len(destinations):
                return destinations[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def display_travel_options(data, dest_name):
    print("\nOptions for " + dest_name + ":")

    flights = get_flights_for_destination(data, dest_name)
    if len(flights) > 0:
        print("\nFlights:")
        i = 0
        while i < len(flights):
            f = flights[i]
            flight_no = f["flight_no"] if "flight_no" in f else "N/A"
            departure = f["departure"] if "departure" in f else "N/A"
            arrival = f["arrival_time"] if "arrival_time" in f else "N/A"
            price = f["price"] if "price" in f else "N/A"
            print("  - Flight " + str(flight_no) + " from " + str(departure) + " at " + str(arrival) + " | Price: " + str(price))
            i += 1
    else:
        print("No flights available.")

    hotels = get_hotels_for_destination(data, dest_name)
    if len(hotels) > 0:
        print("\nHotels:")
        i = 0
        while i < len(hotels):
            h = hotels[i]
            name = h["hotel_name"] if "hotel_name" in h else "N/A"
            rating = h["rating"] if "rating" in h else "N/A"
            price = h["price_per_night"] if "price_per_night" in h else "N/A"
            print("  - " + str(name) + " | Rating: " + str(rating) + " | Price/night: " + str(price))
            i += 1
    else:
        print("No hotels available.")


def run_cli(filepath='travel_data.json'):
    data = load_travel_data(filepath)
    destinations = get_destinations(data)

    if len(destinations) == 0:
        print("No destinations loaded. Exiting.")
        return

    print("Welcome to Travel Planner CLI!")
    dest_name = select_destination(destinations)
    if dest_name == "":
        return

    display_travel_options(data, dest_name)


# === New booking-related functions ===

def get_bookings_filepath():
    """Get the path to the bookings JSON file"""
    # Assuming myfile.py is in the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'booking_details.json')


def load_bookings():
    """Load bookings from JSON file"""
    filepath = get_bookings_filepath()
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}  # Return empty dict if file doesn't exist yet
    except Exception as e:
        print(f"Error loading bookings: {e}")
        return {}  # Return empty dict on error


def save_bookings(bookings_data):
    """Save bookings to JSON file"""
    filepath = get_bookings_filepath()
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(bookings_data, f, indent=2)
        print(f"Bookings successfully saved to {filepath}")
        return True
    except Exception as e:
        print(f"Error saving bookings: {e}")
        return False


def create_flight_booking(user_email, bookings_db, flight_data):
    """Create a flight booking and save it to the bookings database"""
    # Generate a booking reference number
    booking_id = f"BK{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Create booking object
    booking = {
        'id': booking_id,
        'type': 'flight',
        'flight_no': flight_data.get('flight_no'),
        'airline': flight_data.get('airline'),
        'departure': flight_data.get('departure'),
        'destination': flight_data.get('destination'),
        'date': flight_data.get('date'),
        'departure_time': flight_data.get('departure_time'),
        'arrival_time': flight_data.get('arrival_time'),
        'price': flight_data.get('price'),
        'guests': flight_data.get('guests'),
        'status': 'confirmed',
        'booking_date': datetime.datetime.now().strftime('%Y-%m-%d')
    }
    
    # Store the booking in our bookings_db
    if user_email not in bookings_db:
        bookings_db[user_email] = []
    
    bookings_db[user_email].append(booking)
    
    # Save the updated bookings to JSON file
    save_bookings(bookings_db)
    
    print(f"Flight booking added for {user_email}: {booking_id}")
    
    return booking_id, booking


def create_hotel_booking(user_email, bookings_db, hotel_data):
    """Create a hotel booking and save it to the bookings database"""
    # Generate a booking reference number
    booking_id = f"BK{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Create booking object
    booking = {
        'id': booking_id,
        'type': 'hotel',
        'hotel_name': hotel_data.get('hotel_name'),
        'destination': hotel_data.get('destination'),
        'check_in': hotel_data.get('check_in'),
        'check_out': hotel_data.get('check_out'),
        'price': hotel_data.get('price'),
        'guests': hotel_data.get('guests'),
        'status': 'confirmed',
        'booking_date': datetime.datetime.now().strftime('%Y-%m-%d')
    }
    
    # Store the booking in our bookings_db
    if user_email not in bookings_db:
        bookings_db[user_email] = []
    
    bookings_db[user_email].append(booking)
    
    # Save the updated bookings to JSON file
    save_bookings(bookings_db)
    
    print(f"Hotel booking added for {user_email}: {booking_id}")
    
    return booking_id, booking


def get_user_bookings(user_email):
    """Get all bookings for a specific user"""
    fresh_bookings = load_bookings()
    user_bookings = fresh_bookings.get(user_email, [])
    print(f"Found {len(user_bookings)} bookings for user {user_email}")
    return user_bookings


if __name__ == "__main__":
    run_cli()
