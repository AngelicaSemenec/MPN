from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
import cv2
import time

# VIDEO_SRC = "IP_address"
VIDEO_SRC2 = "static/video-streaming/goldfish3.mp4"

sub = cv2.createBackgroundSubtractorMOG2()  # create background subtractor

def main_motion_detection():
    """Video streaming frame by frame"""
    cap = cv2.VideoCapture(VIDEO_SRC2)

    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
    height  = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
    print('[Motion] (w,h) => ', width, ',', height)

    totalframes  = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print('Total Frames = ', totalframes)

    framerate  = cap.get(cv2.CAP_PROP_FPS)
    print('Frame Rate = ', framerate)
    # stream video until completed
    while(cap.isOpened()):
        ret, frame = cap.read()  # import image
        if not ret: #if streaming finished, repeat
            frame = cv2.VideoCapture(VIDEO_SRC2)
            continue

        if ret:  # if there is a frame continue with code
            image = cv2.resize(frame, (0, 0), None, 1, 1)  # resize image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # converts image to gray
            fgmask = sub.apply(gray)  # uses the background subtraction
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # kernel to apply to the morphology
            closing = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
            opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
            dilation = cv2.dilate(opening, kernel)
            retvalbin, bins = cv2.threshold(dilation, 220, 255, cv2.THRESH_BINARY)  # removes the shadows
            contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            minarea = 400
            maxarea = 50000
            for i in range(len(contours)):  # cycles through all contours in current frame
                if hierarchy[0, i, 3] == -1:  # using hierarchy to only count parent contours (contours not within others)
                    area = cv2.contourArea(contours[i])
                    # area of contour
                    if minarea < area < maxarea:  # area threshold for contour
                        # calculating centroids of contours
                        cnt = contours[i]
                        M = cv2.moments(cnt)
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        # gets bounding points of contour to create rectangle
                        # x,y is top left corner and w,h is width and height
                        x, y, w, h = cv2.boundingRect(cnt)
                        # creates a rectangle around contour
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        # Prints centroid text in order to double check later on
                        cv2.putText(image, str(cx) + "," + str(cy), (cx + 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX,.3, (0, 0, 255), 1)
                        cv2.drawMarker(image, (cx, cy), (0, 255, 255), cv2.MARKER_CROSS, markerSize=8, thickness=3,line_type=cv2.LINE_8)
        #cv2.imshow("countours", image)
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
