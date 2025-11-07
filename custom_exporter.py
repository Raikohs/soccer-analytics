from prometheus_client import start_http_server, Gauge
import requests
import time

CITY = "Uralsk"
API_KEY = "ce5edb25369820b92c9d6c218246e794"


temperature = Gauge('weather_temperature_celsius', 'Current temperature in Celsius')
feels_like = Gauge('weather_feels_like_celsius', 'Feels like temperature in Celsius')
temp_min = Gauge('weather_temp_min_celsius', 'Minimum temperature in Celsius')
temp_max = Gauge('weather_temp_max_celsius', 'Maximum temperature in Celsius')
humidity = Gauge('weather_humidity_percent', 'Current humidity in percent')
pressure = Gauge('weather_pressure_hpa', 'Current pressure in hPa')
wind_speed = Gauge('weather_wind_speed_mps', 'Current wind speed in m/s')
wind_deg = Gauge('weather_wind_deg', 'Wind direction in degrees')
clouds = Gauge('weather_clouds_percent', 'Cloudiness in percent')
visibility = Gauge('weather_visibility_meters', 'Visibility in meters')
sunrise = Gauge('weather_sunrise_timestamp', 'Sunrise time (Unix timestamp)')
sunset = Gauge('weather_sunset_timestamp', 'Sunset time (Unix timestamp)')

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature.set(data['main']['temp'])
        feels_like.set(data['main']['feels_like'])
        temp_min.set(data['main']['temp_min'])
        temp_max.set(data['main']['temp_max'])
        humidity.set(data['main']['humidity'])
        pressure.set(data['main']['pressure'])
        wind_speed.set(data['wind'].get('speed', 0))
        wind_deg.set(data['wind'].get('deg', 0))
        clouds.set(data['clouds']['all'])
        visibility.set(data.get('visibility', 0))
        sunrise.set(data['sys']['sunrise'])
        sunset.set(data['sys']['sunset'])
    else:
        print("⚠️ Failed to fetch weather data:", response.status_code)

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        get_weather()
        time.sleep(30)
