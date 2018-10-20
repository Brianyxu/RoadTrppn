from yelpapi import YelpAPI 
from pprint import pprint
import math
import operator
secret = open('yelp_key.txt', 'r')
ykey = secret.read()
secret.close()
yelp_api = YelpAPI(ykey)

MODERATE_NUMBER_OF_REVIEWS = 50

def getYelp(test):
    response=[]
    for key, value in test.items():
        #if key > begin_interval and key < end_interval:
        response.append(yelp_api.search_query(term='restaurants', latitude=value[0], longitude=value[1], sort_by='rating', limit=5))
    initial=[]
    for i in range(len(response)):
        for j in range(5):
            rating = response[i]['businesses'][j]['rating']
            review_count = response[i]['businesses'][j]['review_count']
            weighted = round(float(rating) + 5 * float(1-math.pow(math.e,-review_count/MODERATE_NUMBER_OF_REVIEWS)),3)
            if response[i]['businesses'][j]['location']['address1'] and not response[i]['businesses'][j]['is_closed']:
                name = response[i]['businesses'][j]['name']
                address = response[i]['businesses'][j]['location']['address1']+", "+response[i]['businesses'][j]['location']['city']+", "+response[i]['businesses'][j]['location']['state']+" "+response[i]['businesses'][j]['location']['zip_code']
                initial.append({'name': name, 'address': address, 'rating':weighted})
    result = [dict(tupleized) for tupleized in set(tuple(name.items()) for name in initial)]
    result2 = sorted(result, key=lambda k: k['rating'], reverse=True)
    return (result2)
# for key, value in initial.items():
#     if value not in final.values():
#         final[key] = value

# tentative = sorted(final.items(), key=lambda x: x[1], reverse=True)
# print (tentative)
# response = yelp_api.search_query(term='restaurants', longitude=-86.81009, latitude=36.15568, sort_by='rating', limit=5)
# pprint(response)