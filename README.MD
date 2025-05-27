
# ✈️ 2rism – Travel Booking Web Application

2rism is a comprehensive travel booking platform built with Flask, enabling users to search and book flights and hotels, manage their bookings, and maintain user sessions—all within a responsive web interface.

---

## 📌 Features

- **Flight Booking**: Search and book flights between various destinations.
    
- **Hotel Booking**: Find and reserve hotels at popular travel destinations.
    
- **User Dashboard**: View and manage all your bookings in one place.
    
- **Authentication**: User registration, login, and session management.
    
- **Responsive Design**: Modern UI compatible with desktop and mobile devices.
    

---

## 🏗️ Project Structure

```
2rism-main/
├── Backend/              # Flask application
│   └── app.py            # Main application file
├── templates/            # HTML templates
│   ├── Index.html        # Homepage
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # User dashboard
│   ├── flight_results.html  # Flight search results
│   └── hotel_result.html    # Hotel search results
├── css/                  # CSS stylesheets
│   ├── style.css         # Main stylesheet
│   └── mobile.css        # Mobile-specific styles
├── JS/                   # JavaScript files
│   ├── script.js         # Main script file
│   └── form-validation.js # Form validation script
├── Imgs/                 # Image assets
│   ├── Logo/             # Application logos
│   ├── icons/            # UI icons
│   └── hotels/           # Hotel images
├── myfile.py             # Utility functions
├── travel_data.json      # Travel data (destinations, flights, hotels)
├── booking_details.json  # User booking records
└── run_server.bat        # Batch file to start the server
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.7 or higher
    
- pip (Python package installer)
    

### Steps

1. **Download the Repository**
    
    You can either:
    
    - **Clone the repository**:
        
        ```bash
        git clone https://github.com/Parag1337/2-rism.git
        cd 2-rism
        ```
        
    - **Download as ZIP**:
        
        - Navigate to the [2rism GitHub repository](https://github.com/Parag1337/2-rism).
            
        - Click on the green **Code** button and select **Download ZIP**.
            
        - Extract the ZIP file to your desired location.
            
2. **Install Dependencies**
    
    Install the required Python packages:
    
    ```bash
    pip install flask==2.0.1 werkzeug==2.0.1
    ```
    

---

## 🚀 Running the Application

You can run the 2rism application using either of the following methods:

### Method 1: Using the Batch File (Windows Only)

1. Navigate to the extracted `2rism-main` directory.
    
2. Double-click the `run_server.bat` file.
    
3. The server will start, and you can access the application at `http://127.0.0.1:5000/`.
    

### Method 2: Manual Start

1. Open a command prompt or terminal.
    
2. Navigate to the `Backend` directory:([Reddit](https://www.reddit.com/r/learnpython/comments/1bismq5/how_can_i_run_a_flask_app_for_completely_free/?utm_source=chatgpt.com "How can I run a flask app for completely free (preferably with GitHub ..."))
    
    ```bash
    cd path/to/2rism-main/Backend
    ```
    

3. Run the Flask application:
    
    ```bash
    python app.py
    ```
    

4. The server will start, and you can access the application at `http://127.0.0.1:5000/`.
    

---

## 👥 User Guide

### Homepage

- Search for flights between destinations.
    
- Access links to destinations, hotels, flights, and activities.
    
- Login or register using the top-right corner.
    

### Flight Search

- Select departure city, destination, date, and number of guests.
    
- Click "Search" to view available flights.
    
- Results display flight details and pricing.
    
- Click "Book Now" to book a flight (login required).
    

### Hotel Search

- Navigate to the "Hotels And Restaurants" section.
    
- Select location, check-in/check-out dates, and number of guests.
    
- Click "Find Hotels" to view available accommodations.
    
- Results display hotel details, amenities, and pricing.
    
- Click "Book Now" to book a hotel (login required).
    

### User Authentication

- **Register**: Create a new account with name, email, and password.
    
- **Login**: Access your account using email and password.
    
- **Demo Account**:
    
    - Email: `demo@example.com`
        
    - Password: `password123`
        

### Dashboard

- View all your flight and hotel bookings.
    
- See booking details like dates, prices, and confirmation numbers.
    
- Access links to book new trips.
    

---

## 🗃️ Data Management

### Travel Data (`travel_data.json`)

- Destinations with names, descriptions, and images.
    
- Flights with routes, airlines, times, and prices.
    
- Hotels with details, amenities, and rates.
    

### Bookings (`booking_details.json`)

- Unique booking IDs.
    
- User email as the key.
    
- Details of each booking (flights or hotels).
    
- Dates, prices, and status.
    

---

## 🧠 Technical Details

### Routes

- `/`: Homepage with search forms.
    
- `/search_flights`: Process flight search and display results.
    
- `/search_hotels`: Process hotel search and display results.
    
- `/book_flight`: Create flight booking.
    
- `/book_hotel`: Create hotel booking.
    
- `/login`, `/register`: User authentication.
    
- `/dashboard`: User booking management.
    
- `/logout`: End user session.([Railway Docs](https://docs.railway.com/guides/flask?utm_source=chatgpt.com "Deploy a Flask App - Railway Docs"))
    

### Utility Functions (`myfile.py`)

- `load_travel_data()`: Read travel data from JSON.
    
- `get_destinations()`, `get_departure_cities()`: Extract location lists.
    
- `get_flights_for_destination()`, `get_hotels_for_destination()`: Filter travel options.
    
- `create_flight_booking()`, `create_hotel_booking()`: Process bookings.
    
- `save_bookings()`, `load_bookings()`: Manage booking storage.
    

### Session Management

- User authentication status is stored in Flask sessions.
    
- Sessions maintain user state across requests.
    
- When logged in, users can access protected routes (bookings, dashboard).
    

---

## 🚀 Potential Enhancements

- Integrate a database (e.g., SQLite, PostgreSQL) to replace JSON storage.
    
- Implement payment processing functionality.
    
- Add email confirmations for bookings.
    
- Develop an admin panel for managing listings.
    
- Enable user reviews and ratings.
    
- Offer travel package bundles (flight + hotel).([Reddit](https://www.reddit.com/r/flask/comments/1cbsy13/deploy_and_update_flask_app_from_git_to_local/?utm_source=chatgpt.com "Deploy and Update flask app from git to local server - Reddit"))
    

---

## 🛠️ Troubleshooting

### Server Won't Start

- Check Python installation.
    
- Verify Flask is installed.
    
- Ensure port 5000 isn't in use.
    

### Booking Not Appearing in Dashboard

- Confirm you're logged in.
    
- Check `booking_details.json` file exists and is writable.
    
- Verify JSON structure is valid.
    

### Missing Images

- Ensure all image paths in `travel_data.json` are correct.
    
- Check that image files exist in the specified directories.
    

---

## 🧰 Technologies Used

- **Backend**: Python 3.7+, Flask 2.0.1
    
- **Frontend**: HTML5, CSS3, JavaScript
    
- **Data Storage**: JSON files
    
- **UI Components**: Custom CSS, ScrollReveal.js, Swiper.js

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.