import json
import os
import datetime

def load_travel_data(filepath='travel_data.json'):
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
    destinations = []
    if "destinations" in data:
        for destination in data["destinations"]:
            if "name" in destination:
                destinations.append(destination["name"])
    return destinations

def get_flights_for_destination(data, dest_name):
    flights = []
    if "flights" in data:
        for flight in data["flights"]:
            if flight.get("destination") == dest_name:
                flights.append(flight)
    return flights

def get_hotels_for_destination(data, dest_name):
    hotels = []
    if "hotels" in data:
        for hotel in data["hotels"]:
            if hotel.get("destination") == dest_name:
                hotels.append(hotel)
    return hotels

def get_departure_cities(data):
    cities = set()
    if "flights" in data:
        for flight in data["flights"]:
            if "departure" in flight:
                cities.add(flight["departure"])
    return sorted(list(cities))

def get_destination_details(data, dest_name):
    if "destinations" in data:
        for destination in data["destinations"]:
            if destination.get("name") == dest_name:
                return destination
    return None

def select_destination(destinations):
    print("\nAvailable destinations:")
    for index, destination in enumerate(destinations, 1):
        print(f"{index}. {destination}")
    
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
        counter = 0
        while counter < len(flights):
            flight = flights[counter]
            flight_number = flight["flight_no"] if "flight_no" in flight else "N/A"
            departure_city = flight["departure"] if "departure" in flight else "N/A"
            arrival_time = flight["arrival_time"] if "arrival_time" in flight else "N/A"
            ticket_price = flight["price"] if "price" in flight else "N/A"
            print(f"  - Flight {flight_number} from {departure_city} at {arrival_time} | Price: {ticket_price}")
            counter += 1
    else:
        print("No flights available for this destination.")

    hotels = get_hotels_for_destination(data, dest_name)
    
    if len(hotels) > 0:
        print("\nHotels:")
        counter = 0
        while counter < len(hotels):
            hotel = hotels[counter]
            hotel_name = hotel["hotel_name"] if "hotel_name" in hotel else "N/A"
            hotel_rating = hotel["rating"] if "rating" in hotel else "N/A"
            nightly_price = hotel["price_per_night"] if "price_per_night" in hotel else "N/A"
            print(f"  - {hotel_name} | Rating: {hotel_rating} | Price/night: {nightly_price}")
            counter += 1
    else:
        print("No hotels available at this destination.")

def run_cli(filepath='travel_data.json'):
    travel_data = load_travel_data(filepath)
    available_destinations = get_destinations(travel_data)

    if len(available_destinations) == 0:
        print("No destinations loaded from data file. Exiting application.")
        return

    print("Welcome to the 2rism Travel Planner Command Line Interface!")
    selected_destination = select_destination(available_destinations)
    
    if selected_destination == "":
        return

    display_travel_options(travel_data, selected_destination)

def get_bookings_filepath():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    booking_file_path = os.path.join(current_directory, 'booking_details.json')
    return booking_file_path

def load_bookings():
    booking_filepath = get_bookings_filepath()
    
    try:
        if os.path.exists(booking_filepath):
            with open(booking_filepath, 'r', encoding='utf-8') as booking_file:
                booking_data = json.load(booking_file)
                return booking_data
        else:
            return {}
    except Exception as error:
        print(f"Error loading bookings: {error}")
        return {}

def save_bookings(bookings_data):
    booking_filepath = get_bookings_filepath()
    
    try:
        with open(booking_filepath, 'w', encoding='utf-8') as booking_file:
            json.dump(bookings_data, booking_file, indent=2)
        
        print(f"Bookings successfully saved to {booking_filepath}")
        return True
    except Exception as error:
        print(f"Error saving bookings: {error}")
        return False

def create_flight_booking(user_email, bookings_db, flight_data):
    current_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    booking_reference = f"BK{current_timestamp}"
    
    flight_booking = {
        'id': booking_reference,
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
    
    if user_email not in bookings_db:
        bookings_db[user_email] = []
    
    bookings_db[user_email].append(flight_booking)
    save_bookings(bookings_db)
    
    print(f"Flight booking added for {user_email}: {booking_reference}")
    return booking_reference, flight_booking

def create_hotel_booking(user_email, bookings_db, hotel_data):
    current_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    booking_reference = f"BK{current_timestamp}"
    
    hotel_booking = {
        'id': booking_reference,
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
    
    if user_email not in bookings_db:
        bookings_db[user_email] = []
    
    bookings_db[user_email].append(hotel_booking)
    save_bookings(bookings_db)
    
    print(f"Hotel booking added for {user_email}: {booking_reference}")
    return booking_reference, hotel_booking

def get_user_bookings(user_email):
    all_bookings = load_bookings()
    user_specific_bookings = all_bookings.get(user_email, [])
    
    print(f"Found {len(user_specific_bookings)} bookings for user {user_email}")
    return user_specific_bookings

if __name__ == "__main__":
    run_cli()
