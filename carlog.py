#!/usr/bin/env python
from flask import Flask, redirect, request, render_template, session, url_for
import data
import datetime

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'dlakfdlkhdaghdao84157-98415-98hfdjTQ$%$%$%'

@app.route("/addtrip", methods=['POST'])
def addtrip():
    if 'username' in session:
        username = session['username']
        date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d')
        car = request.form['car']
        destination = request.form['destination']
        reason = request.form['reason']
        distance = request.form['distance']
        objectid = data.add_trip(username, date, car, destination, reason, distance)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route("/addodometer", methods=['POST'])
def addodometer():
    if 'username' in session:
        username = session['username']
        date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d')
        car = request.form['car']
        km = request.form['km']
        objectid = data.add_odometer(username, date, car, km)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route("/deletetrip/<objectid>")
def deletetrip(objectid):
     if 'username' in session:
         num_removed = data.delete_trip(objectid)
         return redirect(url_for('index'))
     else:
         return redirect(url_for('login'))

@app.route("/deleteodometer/<objectid>")
def deleteodometer(objectid):
     if 'username' in session:
         num_removed = data.delete_odometer(objectid)
         return redirect(url_for('index'))
     else:
         return redirect(url_for('login'))

@app.route("/<int:year>")
def index_with_year(year):
    return index(year)

@app.route("/")
def index(year=None):
    if year == None:
        year = datetime.datetime.now().year
    if 'username' in session:
        username = session['username']
        years = data.get_years(username)
        trips = data.get_trips(username, year)
        odometers = data.get_odometers(username, year)
        cars = data.get_cars(username, year)
        totalkm = {}
        for car in cars:
            totalkm[car] = data.get_total_km_for_year(username, year, car)
        return render_template('index.html', username=username,
                               trips=trips,
                               odometers=odometers,
                               totalkm=totalkm,
                               cars=cars,
                               years=years,
                               selected_year=year)
    else:
        return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        passowrd = request.form['password']
        return redirect(url_for('index'))
    else: #GET
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0')
