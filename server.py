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
    keyword = request.args.get('Keyword')
    price_preference = request.args.get('Price')  # Get the price preference from the request
    if price_preference:
        price_preference = price_preference
    else:
        price_preference = None
    restaurants = get_restaurants(location, radius, keyword=keyword, price=price_preference)  # Pass the price preference to the get_restaurants function
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
