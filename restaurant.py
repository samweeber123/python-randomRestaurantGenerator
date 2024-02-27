from dotenv import load_dotenv
from pprint import pprint
import requests
import os
import random

load_dotenv()

def miles_to_meters(miles):
    return miles * 1609

def get_restaurants(location, radius):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }
    params = {
        "location": location,
        "radius": radius,
        "categories": "restaurants"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "error" in data:
        print("Error:", data["error"]["description"])
        return None

    return data.get("businesses", [])

def pick_random_restaurant(restaurants):
    if restaurants:
        random_restaurant = random.choice(restaurants)
        return random_restaurant["name"]
    else:
        return "No restaurants found."
    
if __name__ == "__main__" :
    location = input("Enter your location: ")
    radius = int(input("Enter the radius in miles: "))
    
    if not bool(location.strip()):
        location = "London"

    restaurants = get_restaurants(location, miles_to_meters(radius))
    random_restaurant = pick_random_restaurant(restaurants)
    pprint(random_restaurant)