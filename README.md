
#  Weather Watch Lite

**Weather Watch Lite** is a full-stack weather tracking application built using **Flask** for the backend and **React + Vite** for the frontend. The app allows users to register, search weather conditions for any location, save their favorite cities, and view a detailed 7-day forecast—delivering both real-time insights and personalized weather tracking.

---

##  Project Structure

```plaintext
weather-watch-lite/
│
├── client/         # React frontend
│   ├── src/
│   ├── public/
│   └── ...
│
└── server/         # Flask backend
    ├── app.py
    ├── models.py
    ├── seed.py
    └── ...
```

---

##  Technologies Used

###  Frontend (React + Vite)
- **React**: Frontend library for building UI components
- **Vite**: Fast build tool and development server
- **React Router DOM**: Client-side routing
- **Custom CSS**: For styling components and animations
- **Fetch API**: For communicating with the Flask backend

###  Backend (Flask REST API)
- **Flask**: Python micro web framework
- **Flask-RESTful**: RESTful API creation
- **SQLAlchemy + Flask-SQLAlchemy**: ORM for database interactions
- **Flask-Migrate**: Database migrations
- **Flask-CORS**: Cross-Origin Resource Sharing
- **Werkzeug**: Password hashing
- **Faker**: Generates dummy data for development

---

##  Features

###  User Authentication (Backend)
- Register new users with email, username, and password
- Passwords securely hashed using Werkzeug
- Token-based authentication (JWT) planned for full implementation

###  Weather Functionality
- Search weather data by city or country name
- Real-time data fetched from the backend (powered by OpenWeatherMap API)
- View current temperature, humidity, wind speed, and weather conditions
- View a 7-day forecast, each with temperature, condition, and humidity

###  Saved Locations
- Logged-in users can save their favorite cities
- Revisit saved locations for quick weather updates
- Delete saved locations from the dashboard

###  Search History
- Automatically records searches made by logged-in users
- Useful for tracking previously checked locations

---

##  Local Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Velma96/weather-watch-lite.git
cd weather-watch-lite
```

---

## ⚙️ Backend Setup (Flask API)

```bash
cd server
```

### Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Configure Environment Variables:

Create a `.env` file with:

```env
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URI=sqlite:///weather_api.db
SECRET_KEY=your_secret_key_here
```

### Run database migrations:

```bash
flask db init
flask db migrate
flask db upgrade
```

### Seed the database (optional, for development):

```bash
python seed.py
```

### Start the Flask server:

```bash
python app.py
```

> Your API will be available at: `http://localhost:5555`

---

## 🖼️ Frontend Setup (React + Vite)

```bash
cd client
```

### Install dependencies:

```bash
npm install
```

### Start the development server:

```bash
npm run dev
```

> Your frontend app will run at: `http://localhost:5173`

---

## 🌐 Frontend Pages

| Page | Description |
|------|-------------|
| **Homepage** | Includes a hero section, a search bar, and default weather display |
| **Dashboard** | Displays user's saved locations, and allows delete/save |
| **SearchBar Component** | Accepts user input, calls the backend API, and conditionally renders save buttons |
| **ForecastCard Component** | Displays a visual forecast summary for a 7-day period |
| **Login/Signup** *(Planned)* | User auth and route guarding |

---

##  API Overview (Backend)

Your Flask API provides these RESTful endpoints:

### Users
- `GET /users`: Get all users
- `POST /users`: Create a new user
- `PUT /users/<id>`: Update user details
- `DELETE /users/<id>`: Remove a user

### Saved Locations
- `GET /saved-locations`: Get all saved locations
- `POST /saved-locations`: Save a location
- `DELETE /saved-locations/<id>`: Delete a location

### Search Records
- `POST /search-records`: Save a user search query
- `GET /search-records`: Fetch past user searches

### Weather
- `GET /weather/search?location=<name>`: Get weather and forecast by city/country name
- `GET /weather-data/<id>`: Retrieve stored weather data

---

##  Example Requests

### POST `/users` (Register a user)

```json
{
  "username": "phoebe",
  "email": "phoebe@example.com",
  "password": "securepass123"
}
```

### GET `/weather/search?location=Nairobi`

Returns weather data and a 7-day forecast for Nairobi.

---

##  Search Functionality (Frontend)

The SearchBar component:
- Accepts input and calls `http://localhost:5000/weather/search?location=<city>`
- Handles errors and empty results
- Shows a loading spinner during the request
- Displays a “Save Location” button if the user is authenticated

---

##  Security and Authentication

- Passwords are securely hashed using Werkzeug
- JWT-based authentication is planned
- Token stored in `localStorage` and sent in `Authorization` headers

---

##  Planned Enhancements

- [ ] Implement JWT login & protected routes
- [ ] Add login/signup forms and auth context to frontend
- [ ] Improve error UX (toasts, modals)
- [ ] Add unit tests (backend and frontend)
- [ ] Mobile responsiveness improvements
- [ ] Add OpenAPI/Swagger documentation
- [ ] Enable live weather updates with polling or sockets
- [ ] Add support for weather alerts

---

##  Contributing

Contributions are welcome! Here's how to get started:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Commit and push (`git commit -m 'Add my feature' && git push`)
5. Submit a Pull Request

---

##  License

This project is licensed under the [MIT License](LICENSE)

---

##  About the Project

Weather Watch Lite is a project by **Phoebe Velma Awuor**, **Natalie Wanjiku**,**Ngugi Louis** and **Mohamed Issa**,designed to demonstrate how a software engineer can combine real-world APIs, user authentication, and frontend/backend integration to build a practical, data-driven weather app.

---