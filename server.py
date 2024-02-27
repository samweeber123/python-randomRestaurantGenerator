from flask import Flask, render_template, request
from restaurant import get_restaurants, pick_random_restaurant, miles_to_meters
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/restaurant')
def get_restaurant():
    location = request.args.get('Location')
    if not bool(location.strip()):
        location = "London"
    radius_in_meters = int(request.args.get('Radius'))
    radius = miles_to_meters(radius_in_meters)
    restaurants = get_restaurants(location, radius)
    random_restaurant = pick_random_restaurant(restaurants)
    return render_template(
        "restaurants.html",
        title=random_restaurant,
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)

