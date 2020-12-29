from django.shortcuts import render
import requests
from .models import City
from . import info
from .forms import CityForm


def home(request):
    cities = City.objects.all()
    cities_data = []
    success_message, error_message = "", ""

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            is_new_city_exist = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={new_city}&appid={info.API_KEY}").json()
            if is_new_city_exist['cod'] == 200:
                form.save()
                success_message = "City added successfully"
            else:
                error_message = "city dose not exist!"

    form = CityForm()

    for _city in cities:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={_city}&appid={info.API_KEY}").json()

        city_status = {
            "city_name": response['name'],
            'tmep': response['main']['temp'],
            'weather': response['weather'][0]['main'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }

        cities_data.append(city_status)

    context = {
        'full_data': cities_data,
        'form': form,
        'error_message': error_message,
        "success_message": success_message
    }
    return render(request, 'home.html', context)
