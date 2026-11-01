import sys
import requests

import requests

def get_coordinates(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city_name,
        "count": 1
    }

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()

    data = response.json()

    if not data.get("results"):
        return None

    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]

    return latitude, longitude


# # Temporary test - we'll delete this later
# print(get_coordinates("Boston"))
# print(get_coordinates("asdfghjkl"))

def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m"
    }

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()

    data = response.json()

    return data["current"]

# # Temporary test
# coords = get_coordinates("Boston")
# print(coords)
# print(get_weather(coords[0], coords[1]))


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 weather.py <city_name>")
        return

    city = " ".join(sys.argv[1:])

    try:
        coordinates = get_coordinates(city)

        if not coordinates:
            print(f"City not found: {city}")
            return

        latitude, longitude = coordinates
        weather = get_weather(latitude, longitude)

        print(f"\nWeather in {city.title()}")
        print(f"Temperature: {weather['temperature_2m']}°C")
        print(f"Wind speed: {weather['wind_speed_10m']} km/h")

    except requests.exceptions.RequestException:
        print("Couldn't connect to the weather service. Check your internet connection and try again.")

    except (KeyError, ValueError):
        print("Something went wrong while reading the weather data.")


if __name__ == "__main__":
    main()