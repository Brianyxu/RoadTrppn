import os
import time

from flask import request, jsonify, Flask
from app.gmaps_util import get_gmaps_coordinates, get_gmaps_directions
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

        # coords = get_gmaps_coordinates(json_data[])
        coords = get_gmaps_coordinates('Vanderbilt University, Nashville', 'Klaus Advanced Computing Center, Atlanta', (time.time(), time.time()+3600))
        restaurants = get_yelp(coords)
        return jsonify(restaurants), 200

@app.route('/directions', methods=['GET'])
def directions():
    if request.method == 'GET':
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data'}), 400

        # directions = get_gmaps_directions(json_data[])
        directions = get_gmaps_directions('Vanderbilt University, Nashville', 'Klaus Advanced Computing Center, Atlanta')
        return jsonify(directions), 200


if __name__ == '__main__':
    app.run(debug=True)

