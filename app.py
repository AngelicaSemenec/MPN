#imports
from flask import Flask, render_template, request, redirect, url_for, flash, \
    Response, session
from flask_bootstrap import Bootstrap
from filters import datetimeformat, file_type, file_name
from resources import get_bucket, get_bucket_list

from video import Video

#Create Flask instance
app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'secret'   #Not the same as s3; this is for flask
app.jinja_env.filters['datetimeformat'] = datetimeformat    #Register the filter
app.jinja_env.filters['file_type'] = file_type
app.jinja_env.filters['file_name'] = file_name


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


#Index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_user = request.form['name']
        username = set_username(new_user)
        return render_template('index.html', username=username)
    #else if request.method == 'GET':
     #   return redirect(url_for('files'))
    else:
        username = '(no name)'
        return render_template('index.html')  

def set_username(new_name):
    username = new_name
    return username

@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    return render_template('createAccount.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')

@app.route('/logout')
def logout():
    return redirect(url_for('index'))


#--> Route for /Login
@app.route('/login')
def login():
    #--> Get user info
    #--> Verification
    #--> Redirect to user homepage
    return
#--> Route for /UserID
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
    #--> Display bus
        #- LiveStream Location Time
    #Function generator to create video stream
    return render_template('video.html')

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