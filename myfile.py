import json
import os

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


if __name__ == "__main__":
    run_cli()
