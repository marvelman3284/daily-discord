import requests
from datetime import datetime

def get_weather(api_key: str, lat: float, lon: float) -> list[str]:
    """Get the weather for the week"""
    week_weather: list[str] = []

    # Request the weather for the next week
    complete_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&appid={api_key}"
    response = requests.get(complete_url).json()
    
    # Loop through the daily weather and format it
    for i in response['daily']:
        ts = i['dt']
        date = datetime.utcfromtimestamp(ts).strftime('%a %b %d')
        final = f"{date}: {i['temp']['day']}, low: {i['temp']['min']}, high: {i['temp']['max']}"
        week_weather.append(final)


    return week_weather

