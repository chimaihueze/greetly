
from django.http import JsonResponse
from django.views import View
import requests


class HelloView(View):
    """
    Hello View
    """
    def get_client_ip(self, request):
        """
        Get IP
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get(self, request, *args, **kwargs):
        visitor_name_raw = request.GET.get('visitor_name', 'Visitor')
        visitor_name = visitor_name_raw.strip('"')

        print(f"Visitor name raw: {visitor_name_raw}")
        print(f"Visitor name processed: {visitor_name}")

        client_ip = self.get_client_ip(request)

        # Fetch location data based on client IP
        location_response = requests.get(f'http://ip-api.com/json/{client_ip}')
        location_response.raise_for_status()
        location_data = location_response.json()

        city = location_data.get('city', 'Unknown')
        lat = location_data.get('lat')
        lon = location_data.get('lon')

        if lat is None or lon is None:
            raise ValueError("Latitude or longitude not found in location data")

        api_key = '4119686291c60153a40a37a39d8db374'

        weather_response = requests.get(
            f'https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={api_key}&include=minutely')
        weather_response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}')
        weather_data = weather_response.json()
        temperature = weather_data['main']['temp']
        temp = int(temperature - 273.15)

        response_data = {
            "client_ip": client_ip,
            "location": city,
            "greeting": f"Hello, {request.GET.get('visitor_name')}! The temperature is {temp} degrees Celsius in {city}"
        }

        return JsonResponse(response_data)
