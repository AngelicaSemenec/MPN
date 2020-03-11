#imports
from flask import Flask, render_template, request, redirect, url_for, flash, \
    Response, session
from flask_bootstrap import Bootstrap
from filters import datetimeformat, file_type, file_name
from resources import get_bucket, get_bucket_list

#Create Flask instance
app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'secret'   #Not the same as s3; this is for flask
app.jinja_env.filters['datetimeformat'] = datetimeformat    #Register the filter
app.jinja_env.filters['file_type'] = file_type
app.jinja_env.filters['file_name'] = file_name

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

#--> Route for /BusID
@app.route('/busID')
def busID():
    #--> Display bus
        #- LiveStream Location Time
    return

#Index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bucket = request.form['bucket']
        session['bucket'] = bucket
        return redirect(url_for('files'))
    else:
        buckets = get_bucket_list()
        return render_template('index.html', buckets=buckets)    #Renders the template

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