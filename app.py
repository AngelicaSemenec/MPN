#imports
from flask import Flask, render_template, request, redirect, url_for, flash, \
    Response, session
from flask_bootstrap import Bootstrap
from filters import datetimeformat, file_type, file_name
from resources import get_bucket, get_bucket_list

from video import Video

from flask_pymongo import PyMongo 
from datetime import datetime
import bcrypt

import cv2
import time
from motion_detection import main_motion_detection
from no_detection import main_no_detection
from no_detection2 import main_no_detection2
from no_detection3 import main_no_detection3
from facial_detection import main_facial_detection

#Create Flask instance
app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'secret'   #Not the same as s3; this is for flask
app.jinja_env.filters['datetimeformat'] = datetimeformat    #Register the filter
app.jinja_env.filters['file_type'] = file_type
app.jinja_env.filters['file_name'] = file_name

app.config['MONGO_DBNAME'] = 'WTS' #Wheel-Time Streaming
app.config['MONGO_URI'] = "mongodb://localhost:27017/Users" #Port number for mongodb

mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return login()
    return render_template('index.html')

def login():
    users = mongo.db.users
    login_user = users.find_one({'username' : request.form['username']})

    if login_user is not None:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            login_user['lastLogin'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            users.save(login_user)
            return redirect(url_for('dashboard'))
    flash('Incorrect username or password!')
    return render_template('index.html')

@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    if request.method == 'POST':
        return createUser()
    return render_template('createAccount.html')

def createUser():
    users = mongo.db.users
    existing_user = users.find_one({'username' : request.form['username']})

    if existing_user is None:
        hashPW = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        email = request.form['email']
        company = request.form['company']
        dateCreated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        accountVerified = 'No'
        lastLogin = 'None'
        if hashPW and fname and lname and username and email and company:
            users.insert({'fname':fname, 'lname':lname, 'username':username, 'email':email, 'password':hashPW, 'company':company, 'dateCreated':dateCreated, 'accountVerified':accountVerified, 'lastLogin':lastLogin})
            flash('User added successfully!')
            flash('Log in to continue.')
            return redirect(url_for('index'))
        else:
            flash('Missing information!')
    else:
        flash('Username already exists!')
    return render_template('createAccount.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html', username=session['username'])

@app.route('/camera_motion_detection')
def camera_motion_detection():
    return Response(main_motion_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera_facial_detection')
def camera_facial_detection():
    return Response(main_facial_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera_normal_view')
def camera_normal_view():
    return Response(main_no_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera_normal_view2')
def camera_normal_view2():
    return Response(main_no_detection2(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera_normal_view3')
def camera_normal_view3():
    return Response(main_no_detection3(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html', username=session['username'])

@app.route('/logout')
def logout():
    session['username'] = None
    return redirect(url_for('index'))

@app.route('/homepage')
def homepage():
    #--> Display current alerts
    #--> Display directory
        #- Alerts
        #- Buses
            #- BusID Location Time  
        #- BusSearch
        #- AlertSearch

    my_bucket = get_bucket()
    alerts = my_bucket.objects.filter(Prefix='a')

    return render_template('homepage.html', my_bucket=my_bucket, files=alerts)

#--> Route for /Alerts
@app.route('/alerts')
def alerts():
    #--> Display Alerts
        #- AlertID BusID Location Time
    my_bucket = get_bucket()
    alerts = my_bucket.objects.filter(Prefix='a')

    return render_template('alerts.html', my_bucket=my_bucket, files=alerts)
    
#--> Route for /AlertID
@app.route('/alertID')
def alertID():
    #--> Display Alert
    return

#--> Route for /Buses
@app.route('/buses')
def buses():
    #--> Display Buses
        #- BusID Location Time Status
    my_bucket = get_bucket()
    alerts = my_bucket.objects.filter(Prefix='b')

    return render_template('buses.html', my_bucket=my_bucket, files=alerts)

def gen(video):
    for x in range(1000):
        frame = video.get_frame()['Body'].read()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Video()), mimetype='multipart/x-mixed-replace; boundary=frame')

#--> Route for /BusID
@app.route('/live_stream')
def live_stream():
    return render_template('video.html', username=session['username'])

#--> Pass file extension with /files
@app.route('/files')
def files():
    my_bucket = get_bucket()
    summaries = my_bucket.objects.all()

    return render_template('files.html', my_bucket=my_bucket, files=summaries)

@app.route('/upload', methods=['POST'])   #Route only accepts POST method
def upload():
    file = request.files['file']

    my_bucket = get_bucket()
    my_bucket.Object(file.filename).put(Body=file, Metadata={'status': 'Active'})

    flash('File uploaded successfully!')
    return redirect(url_for('files'))

@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    my_bucket = get_bucket()
    my_bucket.Object(key).delete()

    flash('File deleted successfully!')
    return redirect(url_for('files'))

@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']

    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )

#Run the application
if __name__ == '__main__':
    app.run()