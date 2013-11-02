from flask import Flask, redirect, request, render_template, session, url_for
import data
import datetime

app = Flask(__name__)
app.secret_key = 'dlakfdlkhdaghdao84157-98415-98hfdjTQ$%$%$%'

@app.route("/addtrip", methods=['POST'])
def addtrip():
    if 'username' in session:
        username = session['username']
        print request.form['date']
        date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d')
        car = request.form['car']
        destination = request.form['destination']
        reason = request.form['reason']
        distance = request.form['distance']
        objectid = data.add_trip(username, date, car, destination, reason, distance)
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

@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        trips = data.get_trips(username)
        defaults = {'date': datetime.datetime.now()}
        return render_template('index.html', username=username, trips=trips)
    else:
        return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
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
