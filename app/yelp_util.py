from yelpapi import YelpAPI 
from pprint import pprint
import math
import operator
import time

MODERATE_NUMBER_OF_REVIEWS = 50

def get_yelp(points):
    """
    Returns a list of dictionaries that contains name, address, and weighted rating of top restaurants along a route.

    Arguments
    ---------
    points is a list of dictionaries with keys being the time stamp and the values being the coordinates in a tuple

    Returns
    -------
    list of dictionaries with restaurant name, address, and weighted rating
        Removes duplicates, sorts by weighted rating
    """
    secret = open('app/yelp_key.txt', 'r')
    ykey = secret.read()
    secret.close()
    yelp_api = YelpAPI(ykey)

    response=[]
    for key, value in points.items():
        response.append(yelp_api.search_query(term='restaurants', latitude=value[0], longitude=value[1], sort_by='rating', limit=5))
        time.sleep(2) # sleep 2 seconds to avoid yelp api limits
    initial=[]
    for i in range(len(response)):
        for j in range(5):
            rating = response[i]['businesses'][j]['rating']
            review_count = response[i]['businesses'][j]['review_count']
            #Weighted formula, we set 50 as a moderate amount of reviews
            weighted = round(float(rating) + 5 * float(1-math.pow(math.e,-review_count/MODERATE_NUMBER_OF_REVIEWS)),3)
            if response[i]['businesses'][j]['location']['address1'] and not response[i]['businesses'][j]['is_closed']:
                name = response[i]['businesses'][j]['name']
                address = response[i]['businesses'][j]['location']['address1']+", "+response[i]['businesses'][j]['location']['city']+", "+response[i]['businesses'][j]['location']['state']+" "+response[i]['businesses'][j]['location']['zip_code']
                initial.append({'name': name, 'address': address, 'rating':weighted})
    #removes duplicates
    result = [dict(tupleized) for tupleized in set(tuple(name.items()) for name in initial)]
    #sorts by weighted average
    result2 = sorted(result, key=lambda k: k['rating'], reverse=True)
    return (result2)
