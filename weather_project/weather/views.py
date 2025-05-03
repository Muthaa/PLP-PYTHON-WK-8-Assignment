# weather/views.py
import requests
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth import login
from .forms import SignUpForm
from .models import FavoriteCity
from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import render
from django.conf import settings
from datetime import datetime

API_KEY = settings.OPENWEATHERMAP_API_KEY

def home(request):
    return render(request, 'weather/home.html')

def result(request):
    city = request.GET.get('city')
    weather = get_weather_data(city)
    context = {'city': city, 'weather': weather}
    return render(request, 'weather/result.html', context)

def get_weather_data(city):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city}"
            f"&appid={API_KEY}&units=metric"
        )
        response = requests.get(url)
        data = response.json()
        
        if data.get('cod') != 200:
            return None

        weather = {
            'temp': data['main']['temp'],
            'description': data['weather'][0]['description'].title(),
            'humidity': data['main']['humidity'],
            'wind': data['wind']['speed'],
        }
        return weather
    except Exception:
        return None

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('home')
        else:
            print("Form errors:", form.errors)
    else:
        form = SignUpForm()
    return render(request, 'weather/signup.html', {'form': form})

@login_required
def save_favorite(request):
    city = request.GET.get('city')
    if city:
        FavoriteCity.objects.get_or_create(user=request.user, city=city)
    return redirect('home')

@login_required
def dashboard(request):
    favorites = FavoriteCity.objects.filter(user=request.user)
    
    city_data = []
    for item in favorites:
        weather = get_weather_data(item.city)
        if weather:
            city_data.append({'city': item.city, 'weather': weather})

    # Determine selected city (via ?forecast_city=CityName)
    selected_city = request.GET.get('forecast_city') or (favorites[0].city if favorites else None)
    
    weather_data = []
    if selected_city:
        lat, lon = get_coordinates(selected_city)
        if lat and lon:
            forecast = get_7_day_forecast(lat, lon)
            for day in forecast:
                weather_data.append({
                    'date': datetime.fromtimestamp(day['dt']),
                    'temp_day': day['temp']['day'],
                    'temp_night': day['temp']['night'],
                    'weather': day['weather'][0]['description'],
                })

    print("Selected city:", selected_city)
    print("Weather data count:", len(weather_data))
    lat, lon = get_coordinates(selected_city)
    print("Lat/Lon for", selected_city, ":", lat, lon)

    forecast = get_7_day_forecast(lat, lon)
    print("Forecast length:", len(forecast))


    return render(request, 'weather/dashboard.html', {
        'city_data': city_data,
        'weather_data': weather_data,
        'selected_city': selected_city,
        'favorite_cities': [fc.city for fc in favorites],
    })

# Example view to fetch 7-day forecast
def weather_dashboard(request):
    api_key = settings.OPENWEATHERMAP_API_KEY
    city = 'London'  # You can make this dynamic or user-specific

    # OpenWeatherMap API URL for 7-day forecast (forecast endpoint)
    url = f"http://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude=hourly,minutely&appid={api_key}&units=metric"
    
    # Use the city's latitude and longitude to get the data (static example)
    latitude = 51.5074  # Example: London latitude
    longitude = -0.1278  # Example: London longitude

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        forecast = data['daily']  # This contains the 7-day forecast

        # Extract necessary information (date, temperature, weather description, etc.)
        weather_data = []
        for day in forecast:
            weather_data.append({
                'date': day['dt'],  # Unix timestamp, you can format this as a date
                'temp_day': day['temp']['day'],
                'temp_night': day['temp']['night'],
                'weather': day['weather'][0]['description'],
            })

        # Pass the weather data to the template
        context = {
            'weather_data': weather_data,
        }
        return render(request, 'weather/dashboard.html', context)
    else:
        # Handle error if data retrieval fails
        return render(request, 'weather/dashboard.html', {'error': 'Failed to retrieve data'})

def get_coordinates(city):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    res = requests.get(url)
    data = res.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    return None, None

def get_7_day_forecast(lat, lon):
    url = (
        f"http://api.openweathermap.org/data/2.5/onecall"
        f"?lat={lat}&lon={lon}&exclude=hourly,minutely&appid={API_KEY}&units=metric"
    )
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()['daily']
    return []