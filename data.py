from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

client = MongoClient()
db = client.cartrips
trips = db['trips']
odometers = db['odometers']

def get_years(username):
    years = set()
    for trip in trips.find({'username': username}):
        years.add(trip['date'].year)
    for odometer in odometers.find({'username': username}):
        years.add(odometer['date'].year)
    years = list(years)
    years.sort()
    return years

def get_cars(username, year):
    start = datetime.datetime(year, 1, 1)
    end = datetime.datetime(year, 12, 31)
    ret = set()
    for trip in trips.find({'username': username,
                            'date': {"$gte": start, "$lte": end},
        }):
        ret.add(trip['car'])
    for odometer in odometers.find({'username': username,
                            'date': {"$gte": start, "$lte": end},
        }):
        ret.add(odometer['car'])

    return ret

def add_odometer(username, date, car, km):
    odometer = {'username': username, 'car': car, 'date': date, 'km': km}
    return odometers.insert(odometer)

def get_odometers(username, year):
    start = datetime.datetime(year, 1, 1)
    end = datetime.datetime(year, 12, 31)
    ret = []
    for odometer in odometers.find({'username': username,
                                    'date': {"$gte": start, "$lte": end},
                                   }).sort("date"):
        ret.append(odometer)
    return ret

def get_last_odometer(username, car, year):
    start = datetime.datetime(year, 1, 1)
    end = datetime.datetime(year, 12, 31)
    ret = []
    for odometer in odometers.find(
            {'username': username,
             'car': car,
             'date': {"$gte": start, "$lte": end},
             }).sort("date"):
        ret.append(odometer)
    return ret[-1]

def get_first_odometer(username, car, year):
    start = datetime.datetime(year, 1, 1)
    end = datetime.datetime(year, 12, 31)
    ret = []
    for odometer in odometers.find(
            {'username': username,
             'car': car,
             'date': {"$gte": start, "$lte": end},
             }).sort("date"):
        ret.append(odometer)
    return ret[0]

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

def get_trips(username, year):
    start = datetime.datetime(year, 1, 1)
    end = datetime.datetime(year, 12, 31)
    ret = []
    for trip in trips.find({'username': username,
                            'date': {"$gte": start, "$lte": end},
                           }).sort("date"):
        ret.append(trip)
    return ret

def get_total_km_for_year(username, year, car):
    ret = 0
    for trip in trips.find({'username': username, 'car': car}):
        if trip['date'].year == year:
            ret += int(trip['distance'])
    return ret


def delete_trip(objectid):
    return trips.remove(ObjectId(objectid))['n']
