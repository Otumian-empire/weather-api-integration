from django.shortcuts import render
from dotenv import load_dotenv
import requests

from pathlib import Path
import os

from .models import City
from .forms import CityForm


load_dotenv()
API_KEY = os.getenv("API_KEY")


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=' + API_KEY
    cities = City.objects.all()

    if request.method == 'POST': 
        form = CityForm(request.POST)
        form.save()

    form = CityForm()


    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city.name)).json()

        weather = {
            'city': city.name,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }

        weather_data.append(weather)


    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/index.html', context)
