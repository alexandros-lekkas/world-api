# World API 🌍

A FastAPI-based service providing info about countries, states, and cities.

## Features 🚀

- Fetch details of countries, states, and cities.
- Query states by country and cities by state and country.
- Supports pagination.
- Auto-generated Swagger documentation for testing and exploring routes.

## Installation & Setup 🛠️

### Prerequisites

- Python 3.10+
- SQLite3

### Clone the Repository

```bash
git clone https://github.com/alexandros-lekkas/world-api.git
cd world-api
```

### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate # For Linux/MacOS
venv\Scripts\activate # For Windows
```

### Install Dependencies

`pip install -r requirements.txt`

### Run the API

`uvicorn api.main:app --reload`

## API Endpoints 📡

### Countries

`GET /countries?page=<int>&pageSize=<int>`

`GET /countriies/{iso2}`

### States

`GET /states?page=<int>&pageSize=<int>`

`GET /states/{country_iso2}?page=<int>&pageSize=<int>`

`GET /states/details/{country_iso2}/{state_code}`

### Cities

`GET /cities?page=<int>&pageSize=<int>`

`GET /cities/{state_code}?page=<int>&pageSize=<int>`

`GET /cities/by-country/{country_iso2}?page=<int>&pageSize=<int>`

## Documentation 📖

By default, FastAPI enables Swagger UI and ReDoc documentation, available for testing and exploring API endpoints.

- Swagger UI: http://127.0.0.1:8000/docs

- ReDoc: http://127.0.0.1:8000/redoc

## Credit 👨‍💻

- Developer: [Alexandros Lekkas](https://github.com/alexandros-lekkas)

- Database: [Country States Cities Database](https://github.com/dr5hn/countries-states-cities-database)
