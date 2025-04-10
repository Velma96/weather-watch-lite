# Weather API

## Description
This is a RESTful API built with Flask that provides weather information, user management, saved locations, and search history functionalities. It uses Flask-RESTful for creating resources, SQLAlchemy for database interactions, and Werkzeug for password hashing.

## Features
- **User Management**:
  - Register, update, and delete users.
  - Retrieve user details.
- **Saved Locations**:
  - Save, update, and delete user locations.
  - Retrieve saved locations with associated weather data.
- **Search Records**:
  - Store user search queries with associated locations.
  - Retrieve search history.
- **Weather Data**:
  - Store and retrieve weather information for specific locations.

## Technologies Used
- **Flask**: A micro web framework for Python.
- **Flask-RESTful**: An extension for building REST APIs with Flask.
- **SQLAlchemy**: A Python SQL toolkit and Object-Relational Mapper.
- **Flask-SQLAlchemy**: An extension that simplifies using SQLAlchemy with Flask.
- **Flask-Migrate**: An extension that handles SQLAlchemy database migrations for Flask applications.
- **Flask-Cors**: An extension for handling Cross-Origin Resource Sharing (CORS) in Flask applications.
- **Faker**: A library for generating fake data.
- **Werkzeug**: A comprehensive WSGI web application library used for password hashing.

## Database Schema
The application uses the following data models:
- **User**: Stores user information (username, email, password hash)
- **SavedLocation**: Represents a location saved by a user
- **WeatherData**: Contains weather information for a specific location
- **SearchRecord**: Tracks user search history
- **SearchLocationAssociation**: Junction table connecting search records with locations

## Setup

1. **Clone the repository:**
   ```
   git clone https://github.com/Velma96/weather-watch-lite
   cd server  # To work on the backend
   ```

2. **Create a virtual environment:**
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory with the following variables:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   DATABASE_URI=sqlite:///weather_api.db
   SECRET_KEY=your_secret_key_here
   ```

5. **Set up the database:**
   The application uses SQLite for database storage. The database URI is set in `app.py`.

6. **Run migrations:**
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

## Usage

1. **Run the application:**
   ```
   python app.py
   ```
   The API will be accessible at `http://localhost:5555`.

2. **Seed the database:**
   To populate the database with sample data, run:
   ```
   python seed.py
   ```

## API Endpoints

### User Resource
- `GET /users`: Get all users.
- `GET /users/<id>`: Get a specific user by ID.
- `POST /users`: Create a new user.
  - Required fields: `username`, `email`, `password`.
- `PUT /users/<id>`: Update an existing user.
  - Updatable fields: `username`, `email`, `password`.
- `DELETE /users/<id>`: Delete a user.

### Saved Location Resource
- `GET /saved-locations`: Get all saved locations.
- `GET /saved-locations/<id>`: Get a specific saved location by ID.
- `POST /saved-locations`: Create a new saved location.
  - Required fields: `user_id`, `location_name`.
- `PUT /saved-locations/<id>`: Update an existing saved location.
  - Updatable fields: `location_name`.
- `DELETE /saved-locations/<id>`: Delete a saved location and associated weather data.

### Search Record Resource
- `GET /search-records`: Get all search records.
- `GET /search-records/<id>`: Get a specific search record by ID.
- `POST /search-records`: Create a new search record.
  - Required fields: `user_id`, `query`.
  - Optional fields: `location_ids` (list of saved location IDs).
- `PUT /search-records/<id>`: Update an existing search record.
  - Updatable fields: `query`, `location_ids` (list of saved location IDs).
- `DELETE /search-records/<id>`: Delete a search record.

### Weather Data Resource
- `GET /weather-data`: Get all weather data.
- `GET /weather-data/<id>`: Get a specific weather data entry by ID.
- `POST /weather-data`: Create a new weather data entry.
  - Required fields: `location_id`, `current_temperature`, `current_humidity`, `current_wind_speed`, `weather_condition`, `forecast_data`.
- `PUT /weather-data/<id>`: Update an existing weather data entry.
  - Updatable fields: `current_temperature`, `current_humidity`, `current_wind_speed`, `weather_condition`, `forecast_data`.
- `DELETE /weather-data/<id>`: Delete a weather data entry.

## Example API Requests and Responses

### Creating a new user
```
POST /users
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password123"
}
```

Response:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2025-04-10T12:00:00Z"
}
```

### Saving a location
```
POST /saved-locations
Content-Type: application/json

{
  "user_id": 1,
  "location_name": "New York, NY"
}
```

Response:
```json
{
  "id": 1,
  "user_id": 1,
  "location_name": "New York, NY",
  "created_at": "2025-04-10T12:05:00Z"
}
```

## Error Handling
The API returns standard HTTP status codes:
- `200 OK`: Successful request
- `201 Created`: Resource successfully created
- `400 Bad Request`: Invalid request (missing or invalid parameters)
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

Error responses include a JSON object with an error message:
```json
{
  "error": "User not found"
}
```

## Seeding the Database
The `seed.py` script populates the database with fake data for testing and development purposes. It performs the following actions:
- Creates 15 users, each with a unique username, email, and a hashed password.
- Creates 1-3 saved locations for each user, using city names generated by Faker.
- Generates weather data for each saved location, including current temperature, humidity, wind speed, weather condition, and a 7-day forecast.
- Creates 2-4 search records for each user, using search queries generated by Faker.
- Associates each search record with 1-2 saved locations that belong to the user.

## Authentication and Security
The API uses Werkzeug for password hashing. However, a proper authentication system with token-based authentication (JWT) is planned for future implementation.

## To Do
- Implement token-based authentication (JWT/OAuth)
- Add unit and integration tests
- Swagger/OpenAPI documentation
- Rate limiting for API endpoints
- Implement caching for weather data

## Contributing
Contributions are welcome! To contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes and write tests.
4. Submit a pull request.

## License
[MIT License](LICENSE)

## About
This project was created as a demonstration of building a RESTful API with Flask. It lets users save favorite locations, fetch and view weather forecasts, and revisit past searches — making personal weather tracking easy and insightful.