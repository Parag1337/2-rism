// Destination and flight data from JSON 
const destinationData = {
    "Paris": [
        {"flight_no": "AF101", "departure": "Mumbai", "arrival_time": "10:30 AM", "price": "$450"},
        {"flight_no": "BA204", "departure": "Delhi", "arrival_time": "11:45 AM", "price": "$480"}
    ],
    "Tokyo": [
        {"flight_no": "JL300", "departure": "Chennai", "arrival_time": "9:15 PM", "price": "$700"}
    ],
    "New York": [
        {"flight_no": "AA500", "departure": "Mumbai", "arrival_time": "7:00 AM", "price": "$650"}
    ],
    "London": [
        {"flight_no": "BA150", "departure": "Delhi", "arrival_time": "8:20 AM", "price": "$550"},
        {"flight_no": "VS300", "departure": "Mumbai", "arrival_time": "9:45 AM", "price": "$530"}
    ],
    "Sydney": [
        {"flight_no": "QF21", "departure": "Chennai", "arrival_time": "6:00 AM", "price": "$800"}
    ],
    "Dubai": [
        {"flight_no": "EK512", "departure": "Mumbai", "arrival_time": "2:30 AM", "price": "$400"},
        {"flight_no": "AI974", "departure": "Delhi", "arrival_time": "3:15 AM", "price": "$420"}
    ],
    "Rome": [
        {"flight_no": "AZ784", "departure": "Mumbai", "arrival_time": "12:00 PM", "price": "$600"}
    ],
    "Bangkok": [
        {"flight_no": "TG318", "departure": "Delhi", "arrival_time": "4:50 AM", "price": "$350"}
    ],
    "San Francisco": [
        {"flight_no": "UA789", "departure": "Delhi", "arrival_time": "8:00 AM", "price": "$720"},
        {"flight_no": "AI101", "departure": "Mumbai", "arrival_time": "9:30 AM", "price": "$740"}
    ],
    "Berlin": [
        {"flight_no": "LH900", "departure": "Mumbai", "arrival_time": "2:45 PM", "price": "$580"}
    ],
    "Barcelona": [
        {"flight_no": "IB650", "departure": "Delhi", "arrival_time": "11:20 AM", "price": "$620"}
    ],
    "Cape Town": [
        {"flight_no": "SA331", "departure": "Mumbai", "arrival_time": "3:10 AM", "price": "$880"}
    ],
    "Moscow": [
        {"flight_no": "SU213", "departure": "Delhi", "arrival_time": "5:50 AM", "price": "$610"}
    ]
};

// Update flight options based on selected destination
document.addEventListener('DOMContentLoaded', function() {
    const locationSelect = document.getElementById('location');
    const flightSelect = document.getElementById('flight');
    
    // Add event listener to update flights when destination changes
    locationSelect.addEventListener('change', function() {
        const selectedDestination = this.value;
        updateFlightOptions(selectedDestination);
    });
    
    // Function to update flight options
    function updateFlightOptions(destination) {
        // Clear current options except the first one
        flightSelect.innerHTML = '<option value="" disabled selected>Select flight</option>';
        
        // If we have flights for this destination, add them
        if (destinationData[destination]) {
            destinationData[destination].forEach(flight => {
                const option = document.createElement('option');
                option.value = flight.flight_no;
                option.textContent = `${flight.flight_no} - From ${flight.departure} (${flight.arrival_time}) - ${flight.price}`;
                flightSelect.appendChild(option);
            });
            
            // Enable the flight select
            flightSelect.disabled = false;
        } else {
            // If no flights are available
            const option = document.createElement('option');
            option.value = "";
            option.textContent = "No flights available";
            flightSelect.appendChild(option);
            flightSelect.disabled = true;
        }
    }
});
