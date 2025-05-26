import json

# Data Loading and Retrieval Functions

def load_travel_data(filepath='travel_data.json'):
    try:
        file = open(filepath, 'r')
        data = json.load(file)
        file.close()
        return data
    except FileNotFoundError:
        print("Error: JSON file not found.")
        return {"destinations": []}
    except json.JSONDecodeError:
        print("Error: Could not decode JSON.")
        return {"destinations": []}


def get_destinations(data):
    destinations = []
    if "destinations" in data:
        for d in data["destinations"]:
            if "name" in d:
                destinations.append(d["name"])
    return destinations


def get_flights_for_destination(data, dest_name):
    if "destinations" in data:
        for i in range(len(data["destinations"])):
            dest = data["destinations"][i]
            if "name" in dest and dest["name"].lower() == dest_name.lower():
                if "flights" in dest:
                    return dest["flights"]
    return []


def get_hotels_for_destination(data, dest_name):
    if "destinations" in data:
        for i in range(len(data["destinations"])):
            dest = data["destinations"][i]
            if "name" in dest and dest["name"].lower() == dest_name.lower():
                if "hotels" in dest:
                    return dest["hotels"]
    return []


# CLI Interaction Functions

def select_destination(destinations):
    print("Available destinations:")
    i = 0
    while i < len(destinations):
        print("  " + str(i + 1) + ". " + destinations[i])
        i += 1

    choice = input("\nEnter number or name of destination: ")

    # Numeric selection
    if choice.isdigit():
        idx = int(choice) - 1
        if idx >= 0 and idx < len(destinations):
            return destinations[idx]

    # Name selection
    i = 0
    while i < len(destinations):
        if choice.strip().lower() == destinations[i].lower():
            return destinations[i]
        i += 1

    print("Invalid selection.")
    return ""


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
