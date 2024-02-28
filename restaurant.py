from dotenv import load_dotenv
from pprint import pprint
import requests
import os
import random
import geocoder

load_dotenv()

def miles_to_meters(miles):
    return miles * 1609

def get_longitute_latitude():
    g = geocoder.ip('me')
    latitude = g.latlng[0]
    longitude = g.latlng[1]
    return latitude, longitude

latitude, longitude = get_longitute_latitude()

#OpenCage API
def get_zip_code(latitude, longitude):
    API_KEY = os.getenv('OPENCAGE_API_KEY')
    url = f'https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['results']:
        components = data['results'][0]['components']
        zip_code = components.get('postcode')
        return zip_code
    else:
        return None
    
zip_code = get_zip_code(latitude,longitude)


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

    use_current_location = input("Do you want to use your current location? (y/n): ").lower()
    if use_current_location == "y":
        location = str(zip_code)
    else:
        location = input("Enter the location: ")
        if not bool(location.strip()):
            location = "London"
    radius = int(input("Enter the radius in miles: "))
    
    
    restaurants = get_restaurants(location, miles_to_meters(radius))
    random_restaurant = pick_random_restaurant(restaurants)
    pprint(random_restaurant)
    pprint(location)
    