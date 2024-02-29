from flask import Flask, render_template, request, jsonify
from restaurant import get_restaurants, pick_random_restaurant, miles_to_meters, get_longitute_latitude, get_zip_code
from waitress import serve
#import geocoder

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/restaurant')
def get_restaurant():
    location = request.args.get('Location')  
    radius_in_meters = int(request.args.get('Radius'))
    radius = miles_to_meters(radius_in_meters)
    restaurants = get_restaurants(location, radius)
    random_restaurant = pick_random_restaurant(restaurants)
    return render_template(
        "restaurants.html",
        title=random_restaurant,
    )

# @app.route('/get_current_location', methods=['GET'])
# def get_current_location():
#     g = geocoder.ip('me')
#     latitude = g.latlng[0]
#     longitude = g.latlng[1]
#     zip_code = get_zip_code(latitude, longitude)
#     return str(zip_code)

if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=8000)