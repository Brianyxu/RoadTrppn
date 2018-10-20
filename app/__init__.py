import os
import time

from flask import Flask
from app.gmaps_util import get_gmaps_coordinates
from app.yelp_util import get_yelp


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
)

@app.route('/hello')
def hello():
    coords = get_gmaps_coordinates('Vanderbilt University, Nashville', 'Klaus Advanced Computing Center, Atlanta', (time.time(), time.time()+3600))
    print(coords)
    return(str(len(coords)))

if __name__ == '__main__':
    app.run(debug=True)