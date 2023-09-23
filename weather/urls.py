from django.urls import path
from .views import *

urlpatterns = [
    path('', my_view, name = "home"),
    path('search/', search_view, name='search'),
    path('api/weather/current/', current_weather_api, name='api'),
    path('api/weather/search/<str:city>/', search_weather_api, name='search_weather_api'),
    path('api/weather/forecast/<str:city>/', forecast_weather_api, name='forecast_weather_api'),
    path('register/', register, name='register'),
    path('login/', custom_login, name='login'),
    path('logout/', logout_view, name='logout'),
]
