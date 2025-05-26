// form-validation.js - Validate the search form before submission

document.addEventListener('DOMContentLoaded', function() {
    // Get the form element
    const searchForm = document.querySelector('.showcase-search form');
    
    // Add event listener for form submission
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            // Get form fields
            const departure = document.getElementById('departure').value;
            const destination = document.getElementById('location').value;
            const date = document.getElementById('date').value;
            const guests = document.getElementById('guests').value;
            
            // Basic validation
            let isValid = true;
            let errorMessage = '';
            
            if (!departure) {
                errorMessage += 'Please select departure location.\n';
                isValid = false;
            }
            
            if (!destination) {
                errorMessage += 'Please select destination.\n';
                isValid = false;
            }
            
            if (!date) {
                errorMessage += 'Please select a date.\n';
                isValid = false;
            }
            
            if (!guests || guests < 1) {
                errorMessage += 'Please enter a valid number of guests.\n';
                isValid = false;
            }
            
            // Check if departure and destination are the same
            if (departure && destination && departure === destination.split(',')[0]) {
                errorMessage += 'Departure and destination cannot be the same.\n';
                isValid = false;
            }
            
            // If form is not valid, prevent submission and show error
            if (!isValid) {
                event.preventDefault();
                alert('Please fill out all required fields correctly:\n' + errorMessage);
            }
        });
    }
});
