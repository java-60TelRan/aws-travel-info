import requests


URL = "http://api.weatherapi.com/v1/current.json"
API_KEY = "312f5712e6b047058f2200626252611"
def getWeather(city:str)->str:
    resp = requests.get(URL, {"key":API_KEY, "q":city})
    res = f"{city} is wrong city"
    if not resp.status_code == 400:
        resp.raise_for_status()
        data = resp.json()
        res = f"Weather in {data["location"]["name"]}: temperature is {data["current"]["temp_c"]}\u00B0C , {data["current"]["condition"]["text"]},\n\
        speed of wind: {data["current"]["wind_kph"]} kph, Humidity is {data["current"]["humidity"]}%"
    return res