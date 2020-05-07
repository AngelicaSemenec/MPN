from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
import cv2
import time

# VIDEO_SRC = "IP_address"
VIDEO_SRC4 = "static/video-streaming/fish4.mp4"

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def main_facial_detection():
    """Video streaming frame by frame"""
    cap = cv2.VideoCapture(VIDEO_SRC4)

    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
    height  = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
    print('[Motion] (w,h) => ', width, ',', height)

    totalframes  = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print('Total Frames = ', totalframes)

    framerate  = cap.get(cv2.CAP_PROP_FPS)
    print('Frame Rate = ', framerate)

    # stream video until completed
    while True:
        # Read the frame
        _, img = cap.read()
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        img = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

    cap.releases()
