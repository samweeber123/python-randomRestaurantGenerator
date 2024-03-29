import os
import random
import requests

from dotenv import load_dotenv

load_dotenv()

def miles_to_meters(miles):
    return miles * 1609

def get_coordinates(location):
    # Using Google Geocoding API to get coordinates from location name
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location,
        "key": os.getenv("GOOGLE_MAPS_API_KEY")
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "OK":
        # Extracting latitude and longitude from the response
        lat_lng = data["results"][0]["geometry"]["location"]
        return f"{lat_lng['lat']},{lat_lng['lng']}"
    else:
        print("Error getting coordinates:", data.get("error_message", "Unknown error"))
        return None

def get_restaurants(location, radius, keyword=None, price=None):
    # Get coordinates from location name
    coordinates = get_coordinates(location)
    if coordinates is None:
        return None

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": coordinates,
        "radius": radius,
        "type": "restaurant",
        "key": os.getenv("GOOGLE_MAPS_API_KEY")
    }

    if keyword:
        params["keyword"] = keyword
    
    if price is not None:
        if price == "Cheap":
            params["minprice"] = 0
            params["maxprice"] = 2
        elif price == "Expensive":
            params["minprice"] = 3
            params["maxprice"] = 4

    response = requests.get(url, params=params)
    data = response.json()

    restaurants = []
    for result in data.get("results", []):
        restaurant_info = {
            "name": result["name"],
            "rating": result.get("rating", "Rating not available"),
            "location": result["vicinity"]
        }
        restaurants.append(restaurant_info)

    return restaurants

def pick_random_restaurant(restaurants):
    if restaurants:
        random_restaurant = random.choice(restaurants)
        return random_restaurant["name"], random_restaurant["rating"], random_restaurant["location"]
    else:
        return "No restaurants found.", "", ""

if __name__ == "__main__":
    print("Enter your location (latitude,longitude or location name):")
    location = input()
    print("Enter the radius in miles:")
    radius = miles_to_meters(int(input()))
    print("Enter a keyword:")
    keyword = input()
    print("Enter your price preference (Cheap or Expensive):")
    price_preference = input().capitalize()  # Capitalize to handle case-insensitivity
    json_response = get_restaurants(location, radius, keyword, price_preference)
    print("JSON Response:")
    print(json_response)
