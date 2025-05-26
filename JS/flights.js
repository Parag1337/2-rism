// flights.js - Handle flight selection based on departure and destination

document.addEventListener('DOMContentLoaded', function() {
    // Reference to the select elements
    const departureSelect = document.getElementById('departure');
    const destinationSelect = document.getElementById('location');
    const flightSelect = document.getElementById('flight');
    
    // Variables to store travel data
    let travelData = null;
    
    // Fetch the travel data from the JSON file
    fetch('/travel_data.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            travelData = data;
            console.log('Travel data loaded:', travelData);
            
            // Set up event listeners
            setupEventListeners();
        })
        .catch(error => {
            console.error('Error fetching travel data:', error);
            // Display a user-friendly error message
            flightSelect.innerHTML = '<option value="" disabled selected>Error loading flight data</option>';
        });
    
    // Setup event listeners for the select elements
    function setupEventListeners() {
        departureSelect.addEventListener('change', updateFlightOptions);
        destinationSelect.addEventListener('change', updateFlightOptions);
    }
    
    // Update flight options based on selected departure and destination
    function updateFlightOptions() {
        // Reset flight select
        flightSelect.innerHTML = '<option value="" disabled selected>Select flight</option>';
        
        const selectedDeparture = departureSelect.value;
        const selectedDestination = destinationSelect.value;
        
        // If either departure or destination is not selected, return
        if (!selectedDeparture || !selectedDestination) {
            return;
        }
        
        // Find the selected destination in the travel data
        const destination = travelData.destinations.find(dest => dest.name === selectedDestination);
        
        if (destination) {
            // Filter flights based on the selected departure
            const availableFlights = destination.flights.filter(flight => 
                flight.departure === selectedDeparture);
            
            if (availableFlights.length > 0) {
                // Add options for each available flight
                availableFlights.forEach(flight => {
                    const option = document.createElement('option');
                    option.value = flight.flight_no;
                    option.textContent = `${flight.flight_no} - ${flight.arrival_time} - ${flight.price}`;
                    flightSelect.appendChild(option);
                });
            } else {
                // No flights available for the selected combination
                const noFlightOption = document.createElement('option');
                noFlightOption.disabled = true;
                noFlightOption.selected = true;
                noFlightOption.textContent = 'No flights available for this route';
                flightSelect.appendChild(noFlightOption);
            }
        }
    }
});
