from django.shortcuts import render
from .models import City
from .forms import CityForm
import requests
import time


def weather(request):
    appid = '6f294ebd8540089535d352348ca0a432'  # api ключ для погоды
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + appid

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()

        city_info = {
            'city': city.name,
            'country': res['sys']['country'],
            'time': time.ctime(res['dt'] - 10800 + res['timezone']),
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon']
        }
        all_cities.append(city_info)

    context = {'all_info': all_cities, 'form': form}

    return render(request, 'main/weather.html', context)
