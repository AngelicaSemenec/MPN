from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
from flask_bootstrap import Bootstrap
from resources import get_bucket, get_buckets_list # s3
import cv2
import time
from motion_detection import main_motion_detection
from no_detection import main_no_detection
from no_detection2 import main_no_detection2
from no_detection3 import main_no_detection3
from facial_detection import main_facial_detection

import time # dashboard

# import click
#
# @click.command()
# @click.option("--count", default=1, help="Number of greetings.")
# @click.option("--name", prompt="Your name", help="The person to greet.")
#

app = Flask(__name__)
Bootstrap(app) # pass app in Bootstrap
app.secret_key = 'flash_secret_key'


''' Default Page = Dashboard '''
@app.route('/', methods=['POST', 'GET'])
def dashboard():
    return render_template("dashboard.html")





@app.route('/camera_motion_detection')
def camera_motion_detection():
    return Response(main_motion_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera_facial_detection')
def camera_facial_detection():
    return Response(main_facial_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')


#
# def video_streaming():
#     """Video streaming frame by frame"""
#     cap = cv2.VideoCapture(VIDEO_SRC1)
#
#     # Read until video is completed
#     while(cap.isOpened()):
#       # Capture frame-by-frame
#         time.sleep(0.01)
#         ret, img = cap.read()
#         if ret == True:
#             frame = cv2.imencode('.jpg', img)[1].tobytes()
#             # keep continuously iterates the frames
#             yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#         else: #if vid finish repeat, not tested
#             frame = cv2.VideoCapture(VIDEO_SRC)
#             continue



@app.route('/camera_normal_view')
def camera_normal_view():
    return Response(main_no_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera_normal_view2')
def camera_normal_view2():
    return Response(main_no_detection2(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera_normal_view3')
def camera_normal_view3():
    return Response(main_no_detection3(), mimetype='multipart/x-mixed-replace; boundary=frame')












@app.route("/<debugvalue>")
def debug(debugvalue):
    return f"<h1>{debugvalue}</h>"


@app.route('/index', methods=['GET', 'POST'])
def index():

    ''' SETNAME '''
    if request.method == 'POST':
        new_user = request.form["name"]
        username = set_username(new_user)
        return render_template("index.html", username=username)
    else:
        username = '(no name)'
        return render_template("index.html")

def set_username(new_name):
    username = new_name
    return username



@app.route('/cloudstorage', methods=['GET', 'POST'])
def cloudstorage():
    if request.method == 'POST':
        bucket = request.form['bucket'] # list of buckets
        session['bucket'] = bucket      # store in session variable
        return redirect(url_for('files'))
    else:
        buckets = get_buckets_list()
        return render_template("cloudstorage.html", buckets=buckets)


@app.route('/files')
def files():
    # $ aws config
    my_bucket = get_bucket() # grab bucket
    summaries = my_bucket.objects.all()         # summaries gives the keys (file name)

    return render_template('files.html', my_bucket=my_bucket, files=summaries)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file'] # dictionary key
    my_bucket = get_bucket()      # bucket object
    my_bucket.Object(file.filename).put(Body=file) # put item into bucket

    flash('File upload to S3!')
    return redirect(url_for('files'))


@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    my_bucket = get_bucket()
    my_bucket.Object(key).delete()

    flash('File Deleted from S3!') # flash msg

    return redirect(url_for('files'))


@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']
    my_bucket = my_bucket = get_bucket()

    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain', # image
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )



if __name__ == '__main__':
    app.run(debug=True)
