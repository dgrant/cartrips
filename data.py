from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

client = MongoClient()
db = client.cartrips
trips = db['trips']

def add_trip(username, date, car, destination, reason, distance):
    trip = {'username': username,
            'date': date,
            'car': car,
            'destination': destination,
            'reason': reason,
            'distance': distance,
            'ctime': datetime.datetime.now(),
    }
    return trips.insert(trip)

def get_trips(username):
    ret = []
    for trip in trips.find({'username': username}):
        ret.append(trip)
    return ret

def delete_trip(objectid):
    return trips.remove(ObjectId(objectid))['n']
