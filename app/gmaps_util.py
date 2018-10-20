import googlemaps
import time
import json

# https://stackoverflow.com/questions/15380712/how-to-decode-polylines-from-google-maps-direction-api-in-php
def decode_polyline(polyline_str):
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so just keep
    # track of whether we've hit the end of the string. In each
    # while loop iteration, a single coordinate is decoded.
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dictionary to apply them later
        for unit in ['latitude', 'longitude']: 
            shift, result = 0, 0
            while True:
                byte = ord(polyline_str[index]) - 63
                index+=1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break
            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)
        lat += changes['latitude']
        lng += changes['longitude']
        coordinates.append((lat/100000.0, lng/100000.0))
    return coordinates

def get_gmaps_coordinates(start_location, end_location, time_interval, start_time=None): 
    """
    Returns a list of coordinates along a route, filtered by a time interval

    Arguments
    ---------
    start_location : tuple
        (latitude, longitude) floats
    end_location : tuple
        (latitude, longitude) floats
    time_interval : tuple
        (begin epoch time, end epoch time)
    start_time : float
        Epoch time when trip begins

    Returns
    -------
    filtered_points : list
        list of dictionaries with arrival time as key and 
        (latitude, longitude) tuple as value
    """
    secret = open('app/gmaps_key.txt', 'r')
    gkey = secret.read()
    secret.close()
    gmaps = googlemaps.Client(key=gkey)

    start_loc = start_location
    end_loc = end_location
    t_interval = (time.time(), time.time()+7200)
    if start_time is None:
        time_start = time.time()

    result = gmaps.directions(start_loc, end_loc, mode='driving', 
        departure_time=time_start)
    # print(json.dumps(result, indent=4))
    legs = result[0]['legs']

    points = decode_polyline(result[0]['overview_polyline']['points'])
    interval_time = legs[0]['duration']['value']/len(points)
    current_time = time_start
    filtered_points = {}

    for index, p in enumerate(points):
        current_time += interval_time
        if index % 8 != 0: # arbitrarily use every 8th point
            continue
        if (current_time > t_interval[0] and current_time < t_interval[1]):
            filtered_points[current_time] = (p[0], p[1])
            # print("Lat: {} Long: {} Time: {}".format(p[0], p[1], current_time))

    return filtered_points

# print(get_gmaps_coordinates('Vanderbilt University, Nashville', 'Klaus Advanced Computing Center, Atlanta', (time.time(), time.time()+3600)))