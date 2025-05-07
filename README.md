# 🌤️ Django Weather App

A responsive, user-authenticated Django web application that fetches and displays real-time weather data, including a 7-day forecast and visual charts, powered by the OpenWeatherMap API.

---

## 🚀 Features

- 🔐 User authentication (login/signup/logout)
- 🏙️ Search weather by city
- ⭐ Save favorite cities (per user)
- 📊 7-day forecast using Chart.js
- 🌓 Dark/light theme toggle
- 🗺️ Interactive map integration (planned)
- 📦 Deployed-ready with clean structure

---

## ⚙️ Tech Stack

- **Backend**: Django 5.x
- **Frontend**: HTML, CSS (Bootstrap), Chart.js
- **API**: OpenWeatherMap (One Call / Forecast API)
- **Auth**: Django’s built-in auth system
- **Storage**: SQLite (dev), extensible to PostgreSQL/MySQL

---

## 🛠️ Setup Instructions

### 🔧 1. Clone & Install
```bash
git clone https://github.com/yourusername/django-weather-app.git
cd django-weather-app
python -m venv wvenv
wvenv\Scripts\activate
pip install -r requirements.txt
```

### 🔐 2. Set Your API Key

Create a `.env` file in your project root:
```env
OPENWEATHER_API_KEY=your_api_key_here
```

### ⚙️ 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### ▶️ 4. Start the Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

---

## 📁 Project Structure (Simplified)

```
weather_project/
├── weather/              # Main Django app
│   ├── templates/
│   │   ├── weather/
│   │   └── registration/
│   ├── views.py
│   ├── models.py
│   └── urls.py
├── static/               # Static assets
├── templates/            # Base templates
├── manage.py
└── .env
```

---

## 📌 Roadmap

- [x] Real-time weather search
- [x] Auth system
- [x] Save favorite cities
- [x] Chart.js 7-day forecast
- [x] Dark/light mode
- [ ] Map integration

