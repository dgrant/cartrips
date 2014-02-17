#!/usr/bin/env python
from functools import wraps
from flask import Flask, g, redirect, request, render_template, session, url_for, jsonify, abort, make_response, send_from_directory
from flask.ext.httpauth import HTTPBasicAuth
import data
import datetime
import json

app = Flask(__name__)
app.secret_key = 'dlakfdlkhdaghdao84157-98415-98hfdjTQ$%$%$%'
auth = HTTPBasicAuth()

DATETIME_FORMAT = '%Y-%m-%d'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

#@app.route("/trips/addtrip", methods=['POST'])
@login_required
def addtrip():
    username = session['username']
    date = datetime.datetime.strptime(request.form['date'], DATETIME_FORMAT)
    car = request.form['car']
    destination = request.form['destination']
    reason = request.form['reason']
    distance = request.form['distance']
    objectid = data.add_trip(username, date, car, destination, reason, distance)
    return redirect(url_for('index'))

#@app.route("/trips/addodometer", methods=['POST'])
@login_required
def addodometer():
    username = session['username']
    date = datetime.datetime.strptime(request.form['date'], DATETIME_FORMAT)
    car = request.form['car']
    km = request.form['km']
    objectid = data.add_odometer(username, date, car, km)
    return redirect(url_for('index'))

#@app.route("/trips/deletetrip/<objectid>")
@login_required
def deletetrip(objectid):
     num_removed = data.delete_trip(objectid)
     return redirect(url_for('index'))

#@app.route("/trips/deleteodometer/<objectid>")
@login_required
def deleteodometer(objectid):
     num_removed = data.delete_odometer(objectid)
     return redirect(url_for('index'))

#@app.route("/trips/<int:year>")
@login_required
def index_with_year(year):
    return index(year)

#@app.route("/trips")
@login_required
def index(year=datetime.datetime.now().year):
    username = session['username']
    years = data.get_years(username)
    trips = data.get_trips(username, year)
    odometers = data.get_odometers(username, year)
    cars = data.get_cars(username, year)
    totalkm = data.get_total_km_for_year(username, year)
    return render_template('index.html', username=username,
                           trips=trips,
                           odometers=odometers,
                           totalkm=totalkm,
                           cars=cars,
                           years=years,
                           selected_year=year)

#@app.route("/trips/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        password = request.form['password']
        return redirect(url_for('index'))
    else: #GET
        return render_template('login.html')

#@app.route('/trips/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

############
# REST API #
############

# TODO: find a way to make this only apply to rest requests
@app.errorhandler(404)
def not_found(exception):
    return make_response(jsonify( {'error': 'Not found'}), 404)
     
@auth.get_password
def get_pw(username):
    return ""

# GET Trips
@app.route('/api/trips', methods=['GET'])
@auth.login_required
def get_trips():
    trips = data.get_trips(auth.username())
    for trip in trips:
        trip['_id'] = str(trip['_id'])
        trip['date'] = datetime.datetime.strftime(trip['date'], DATETIME_FORMAT)
        del trip['ctime']
    _json = jsonify({'trips': trips})
    return _json

# GET Trip
#@app.route('/api/trips/<trip_id>', methods=['GET'])
#@auth.login_required
def get_trip(trip_id):
    ret = data.get_trip(trip_id)
    if ret == None:
        abort(404)
    else:
        return jsonify(ret)

# POST Trip
#@app.route('/api/trips', methods=['POST'])
#@auth.login_required
def create_trip():
    if not request.json:
        abort(400)
    date = datetime.datetime.strptime(request.json['date'], DATETIME_FORMAT)
    car = request.json['car']
    destination = request.json['destination']
    reason = request.json['reason']
    distance = request.json['distance']
    tripid = data.add_trip(auth.username(), date, car, destination, reason, distance)

    ret = data.get_trip(tripid)

    return jsonify( {'trip': ret}), 201

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.root_path, filename)

@app.route('/')
def serve_home():
    return send_from_directory(app.root_path, 'index.html')

if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0', port=5001)
