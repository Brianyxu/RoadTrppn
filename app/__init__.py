import os
import time

from flask import request, jsonify, Flask
from app.gmaps_util import get_gmaps_coordinates
from app.yelp_util import get_yelp


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
)

@app.route('/restaurants', methods=['GET'])
def restaurants():
    if request.method == 'GET':
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data'}), 400

        #coords = get_gmaps_coordinates(json_data[])
        coords = get_gmaps_coordinates('Vanderbilt University, Nashville', 'Klaus Advanced Computing Center, Atlanta', (time.time(), time.time()+3600))
        restaurants = get_yelp(coords)
        print("Restaurants:")
        print(restaurants)
        return jsonify({'Restaurants': str(len(restaurants))}), 200

@app.route('/directions', methods=['GET'])
def directions():
    if request.method == 'GET':
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data'}), 400


if __name__ == '__main__':
    app.run(debug=True)

