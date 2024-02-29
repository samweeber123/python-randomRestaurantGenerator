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
    radius_in_miles = int(request.args.get('Radius'))
    radius = miles_to_meters(radius_in_miles)
    keyword = request.args.get('Keyword')  # Get the keyword from the request
    restaurants = get_restaurants(location, radius, keyword=keyword)  # Pass the keyword to the get_restaurants function
    random_restaurant_name, rating, restaurant_location = pick_random_restaurant(restaurants)
    return render_template(
        "restaurants.html",
        title=random_restaurant_name,
        rating=rating,
        location=restaurant_location
    )

if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=8000)
