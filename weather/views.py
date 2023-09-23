from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import JsonResponse
import requests
import datetime


@login_required
def my_view(request):
    city = request.user.city
    API_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
    appid = "bbc5fd24bb52b944a45a27a82d72b557"
    api_parrams = {
        "q": city,
        "appid": appid,
        "units": "metric",
    }
    response = requests.get(API_Endpoint, params=api_parrams)
    response.raise_for_status()
    weather_data = response.json()

    temp = round(weather_data["list"][0]["main"]["temp"])
    city = weather_data["city"]["name"]
    country = weather_data["city"]["country"]
    real_feel = round(weather_data["list"][0]["main"]["feels_like"])
    wind = round(weather_data["list"][0]["wind"]["speed"])
    humidity = round(weather_data["list"][0]["wind"]["gust"])
    pressure = weather_data["list"][0]["main"]["pressure"]
    day = weather_data["list"][0]["weather"][0]["main"]
    icon = weather_data["list"][0]["weather"][0]["icon"]
    d = weather_data['list'][0]["dt_txt"][11::1][:2:]
    base = f"https://openweathermap.org/img/wn/{icon}@2x.png"

    info_list = []
    for d in range(39):
        i = weather_data['list'][d]["dt_txt"][11::1][:2:]
        if i == "12":
            temp = round(weather_data["list"][d]["main"]["temp"])
            icon = weather_data["list"][d]["weather"][0]["icon"]

            y = int(weather_data['list'][d]["dt_txt"][0:4])
            d = int(weather_data['list'][d]["dt_txt"][8:10])
            m = int(weather_data['list'][d]["dt_txt"][5:7])
            data = datetime.datetime(y, m, d)
            weekday_name = data.strftime('%a')

            info_list.append(temp)
            info_list.append(weekday_name)
            info_list.append(icon)
    return render(request, 'weather/home.html', {'city': city,'country': country, 'temp': temp,'real_feel': real_feel ,'wind':wind,'humidity':humidity,'pressure': pressure , 'main': base ,'day':day,'info_list':info_list})

@login_required
def search_view(request):


    if request.method == 'GET':
        search_query = request.GET.get('q')
        API_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
        appid = "bbc5fd24bb52b944a45a27a82d72b557"

        api_parrams = {
            "q": search_query,
            "appid": appid,
            "units": "metric",
        }

        response = requests.get(API_Endpoint, params=api_parrams)
        response.raise_for_status()
        weather_data = response.json()

        temp = round(weather_data["list"][0]["main"]["temp"])
        city = weather_data["city"]["name"]
        country = weather_data["city"]["country"]
        real_feel = round(weather_data["list"][0]["main"]["feels_like"])
        wind = round(weather_data["list"][0]["wind"]["speed"])
        humidity = round(weather_data["list"][0]["wind"]["gust"])
        pressure = weather_data["list"][0]["main"]["pressure"]
        day = weather_data["list"][0]["weather"][0]["main"]
        icon = weather_data["list"][0]["weather"][0]["icon"]
        d = weather_data['list'][0]["dt_txt"][11::1][:2:]
        base = f"https://openweathermap.org/img/wn/{icon}@2x.png"

        info_list = []
        for d in range(39):
            i = weather_data['list'][d]["dt_txt"][11::1][:2:]
            if i == "12":
                temp = round(weather_data["list"][d]["main"]["temp"])
                icon = weather_data["list"][d]["weather"][0]["icon"]

                y = int(weather_data['list'][d]["dt_txt"][0:4])
                d = int(weather_data['list'][d]["dt_txt"][8:10])
                m = int(weather_data['list'][d]["dt_txt"][5:7])
                data = datetime.datetime(y, m, d)
                weekday_name = data.strftime('%a')

                info_list.append(temp)
                info_list.append(weekday_name)
                info_list.append(icon)




    return render(request, 'weather/search_results.html', {'city': city,'country': country, 'temp': temp,'real_feel': real_feel ,
                                                'wind':wind,'humidity':humidity,
                                                 'pressure': pressure , 'main': base ,'day':day,'info_list':info_list , "weekday_name":weekday_name})


@login_required
def current_weather_api(request):

    API_Endpoint = "https://api.openweathermap.org/data/2.5/weather"
    appid = "bbc5fd24bb52b944a45a27a82d72b557"

    api_params = {
        "q": "Chisinau",
        "appid": appid,
        "units": "metric",
    }

    response = requests.get(API_Endpoint, params=api_params)

    if response.status_code == 200:
        weather_data = response.json()

        temperature = round(weather_data["main"]["temp"])
        city = weather_data["name"]
        country = weather_data["sys"]["country"]
        weather_description = weather_data["weather"][0]["description"]
        real_feel = round(weather_data["main"]["feels_like"])
        wind = round(weather_data["wind"]["speed"])
        pressure = weather_data["main"]["pressure"]
        icon = weather_data["weather"][0]["icon"]

        return JsonResponse({
            'city': city,
            'country': country,
            'temperature': temperature,
            'weather_description': weather_description,
            'real_feel': real_feel,
            'wind': wind,
            'pressure':pressure,
            'icon':icon
        })
    else:
        return JsonResponse({'error': 'Unable to fetch weather data'}, status=500)

@login_required
def search_weather_api(request, city):

    API_Endpoint = "https://api.openweathermap.org/data/2.5/weather"
    appid = "bbc5fd24bb52b944a45a27a82d72b557"

    api_params = {
        "q": city,
        "appid": appid,
        "units": "metric",
    }

    response = requests.get(API_Endpoint, params=api_params)

    if response.status_code == 200:
        weather_data = response.json()

        temperature = round(weather_data["main"]["temp"])
        city = weather_data["name"]
        country = weather_data["sys"]["country"]
        weather_description = weather_data["weather"][0]["description"]
        real_feel = round(weather_data["main"]["feels_like"])
        wind = round(weather_data["wind"]["speed"])
        pressure = weather_data["main"]["pressure"]
        icon = weather_data["weather"][0]["icon"]

        # Returnați datele sub formă de răspuns JSON
        return JsonResponse({
            'city': city,
            'country': country,
            'temperature': temperature,
            'weather_description': weather_description,
            'real_feel': real_feel,
            'wind': wind,
            'pressure': pressure,
            'icon': icon
        })
    else:
        return JsonResponse({'error': 'Unable to fetch weather data'}, status=500)


#@login_required
def forecast_weather_api(request,city):

    API_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
    appid = "bbc5fd24bb52b944a45a27a82d72b557"

    api_params = {
        "q": city,
        "appid": appid,
        "units": "metric",
    }

    response = requests.get(API_Endpoint, params=api_params)

    if response.status_code == 200:
        forecast_data = response.json()


        day_list = []
        temp_list = []
        icon_list = []
        for d in range(39):
            i = forecast_data['list'][d]["dt_txt"][11::1][:2:]
            if i == "12":
                temp = round(forecast_data["list"][d]["main"]["temp"])
                icon = forecast_data["list"][d]["weather"][0]["icon"]
                y = int(forecast_data['list'][d]["dt_txt"][0:4])
                d = int(forecast_data['list'][d]["dt_txt"][8:10])
                m = int(forecast_data['list'][d]["dt_txt"][5:7])
                data = datetime.datetime(y, m, d)

                weekday_name = data.strftime('%a')
                temp_list.append(temp)
                day_list.append(weekday_name)
                icon_list.append(icon)
        forecast={
            '0':{
                'day': day_list[0],
                'temp': f'{temp_list[0]}',
                'icon': icon_list[0]
            },
            '1': {
                'day': day_list[1],
                'temp': f'{temp_list[1]}',
                'icon': icon_list[1]
            },
            '2': {
                'day': day_list[2],
                'temp': f'{temp_list[2]}',
                'icon': icon_list[2]
            },
            '3': {
                'day': day_list[3],
                'temp': f'{temp_list[3]}',
                'icon': icon_list[3]
            },
            '4': {
                'day': day_list[4],
                'temp': f'{temp_list[4]}',
                'icon': icon_list[4]
            }
        }

        return JsonResponse({'forecast':forecast})
    else:
        return JsonResponse({'error': 'Unable to fetch forecast data'}, status=500)


from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from weather.models import CustomUser
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'weather/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
        return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'weather/login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('home')



