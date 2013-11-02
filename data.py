from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

client = MongoClient()
db = client.cartrips
trips = db['trips']
odometers = db['odometers']

def add_odometer(username, date, car, km):
    odometer = {'username': username, 'car': car, 'date': date, 'km': km}
    return odometers.insert(odometer)

def get_odometers(username):
    ret = []
    for odometer in odometers.find({'username': username}).sort("date"):
        ret.append(odometer)
    return ret

def delete_odometer(objectid):
    return odometers.remove(ObjectId(objectid))['n'] 

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
    for trip in trips.find({'username': username}).sort("date"):
        ret.append(trip)
    return ret

def get_total_km_for_year(username, year):
    ret = 0
    for trip in trips.find({'username': username}):
        if trip['date'].year == year:
            ret += int(trip['distance'])
    return ret
   

def delete_trip(objectid):
    return trips.remove(ObjectId(objectid))['n']
