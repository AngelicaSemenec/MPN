from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
import cv2
import time


VIDEO_SRC4 = "static/video-streaming/ultrahd60fps.mp4"

sub = cv2.createBackgroundSubtractorMOG2()  # create background subtractor

def main_no_detection3():

    cap = cv2.VideoCapture(VIDEO_SRC4)
    # Read until video is completed
    while(cap.isOpened()):

        time.sleep(0.01)
        ret, img = cap.read()
        if ret == True:
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            # keep continuously iterates the frames
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else: #if vid finish repeat, not tested
            frame = cv2.VideoCapture(VIDEO_SRC1)
            continue
