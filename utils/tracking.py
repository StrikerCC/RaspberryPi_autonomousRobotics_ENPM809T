#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tracking.py    
@Github  :   https://github.com/StrikerCC

@Modify Time      @Author       @Version    @Desciption
------------      -------       --------    -----------
5/3/2021 7:24 AM   Cheng Chen    1.0         None
'''

# import lib
import sys, os
# sys.path.insert(0, os.path.dirname(os.getcwd()))

import numpy as np

import cv2
from imutils.video import VideoStream
import imutils
import time

# from RaspberryPi_autonomousRobotics_ENPM809T.utils.image import find_ROI

sys.path.insert(0, os.path.dirname(os.getcwd()))
from RaspberryPi_autonomousRobotics_ENPM809T.utils.camera_pi import camera_pi


qrcode_results = ['J&J', 'MODERNA', 'PFIZER']

# def angle_of_object(camera_, color_limit_object):
#     frames_out = 10000
#
#     print('looking for object like ', object, 'for', frames_out, 'frames')
#
#     """find object in current frame"""
#     for i in range(frames_out):
#         img = camera_.view_one_frame()
#
#         """find a contour around the object"""
#         center, area = find_ROI(img, color_limit_object)
#         radius = np.sqrt(area/2/np.pi)
#
#         cv2.circle(img, center, int(radius), (255, 155, 155), 1)
#         cv2.imshow(str(center), img)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#
#         """calculate the pixel coord"""
#         angle = camera_.coord_img_to_pose(center)
#         angle[0] = -angle[0]
#
#         if area > 5.0:    # if the pixel cluster is big enough
#             """transform to img coord"""
#             print('frame', i, 'found object at', angle, 'degree')
#             return angle
#
#         if i % 100 == 0:
#             print('frame', i, 'haven\'t find object yet')
#
#     return None

# def get_qrcode():
#     command = 'sudo modprobe bcm2835-v4l2'
#     os.system(command)
#
#     # open video capture
#     cap = cv2.VideoCapture(0)
#
#     # define detector
#     detector = cv2.QRCodeDetector()
#     data = None
#
#     while True:
#         check, img = cap.read()
#         img = cv2.flip(img, -1)
#         data, bbox, _ = detector.detectAndDecode(img)
#
#         if bbox is not None:
#             for i in range(len(bbox)):
#                 cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(0, 0, 255), thickness=4)
#
#         if data is not None:
#             print("Data: ", data)
#             if data in qrcode_results:
#                 break
#
#         # show frame
#         cv2.imshow("QR code detector", img)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#     return data


def get_qrcode(camera_):
    # define detector
    detector = cv2.QRCodeDetector()
    # data = None

    while True:
        img = camera_.view_one_frame()
        data, bbox, _ = detector.detectAndDecode(img)

        if bbox is not None:
            for i in range(len(bbox)):
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(0, 0, 255), thickness=4)

        if data is not None:
            print("Data: ", data)
            if data in qrcode_results:
                break

        # show frame
        cv2.imshow("QR code detector", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    return data


def face_detect(camera_):
    # construct the argument parse and parse the arguments
    prototxt = r'/home/pi/ENPM809T/RaspberryPi_autonomousRobotics_ENPM809T/utils/deploy.prototxt.txt'
    model = r'/home/pi/ENPM809T/RaspberryPi_autonomousRobotics_ENPM809T/utils/res10_300x300_ssd_iter_140000.caffemodel'
    confidence_min = 0.5

    # load our serialized model from disk
    print("[INFO] loading model...")
    net = None
    try:
        net = cv2.dnn.readNetFromCaffe(prototxt, model)
    except:
        print('cannot load model', model)
    print("[INFO] starting video stream...")

    # loop over the frames from the video stream
    frame = camera_.view_one_frame()
    for i in range(50):
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = camera_.view_one_frame()
        frame = imutils.resize(frame, width=400)

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]

        if net is not None:
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                         (300, 300), (104.0, 177.0, 123.0))

            # pass the blob through the network and obtain the detections and
            # predictions
            net.setInput(blob)
            detections = net.forward()

            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence < confidence_min:
                    continue
                else:
                    # compute the (x, y)-coordinates of the bounding box for the
                    # object
                    frame_face = frame
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    # draw the bounding box of the face along with the associated
                    # probability
                    text = "{:.2f}%".format(confidence * 100)
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(frame_face, (startX, startY), (endX, endY),
                                  (0, 255, 0), 2)
                    cv2.putText(frame_face, text, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
                    cv2.imshow("Frame", cv2.flip(frame_face, -1))
                    key = cv2.waitKey(5) & 0xFF

                    print('found a face')
                    return frame_face
                # break

        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    return frame


# def face_detect():
#     # construct the argument parse and parse the arguments
#     prototxt = r'/home/pi/ENPM809T/RaspberryPi_autonomousRobotics_ENPM809T/utils/deploy.prototxt.txt'
#     model = r'/home/pi/ENPM809T/RaspberryPi_autonomousRobotics_ENPM809T/utils/res10_300x300_ssd_iter_140000.caffemodel'
#     confidence_min = 0.5
#
#     # load our serialized model from disk
#     print("[INFO] loading model...")
#     net = None
#     try:
#         net = cv2.dnn.readNetFromCaffe(prototxt, model)
#     except:
#         print('cannot load model', model)
#     print("[INFO] starting video stream...")
#     vs = VideoStream(src=0).start()
#     time.sleep(2.0)
#
#     frame = vs.read()
#     frame = imutils.resize(frame, width=400)
#
#     # loop over the frames from the video stream
#     for i in range(20):
#         # grab the frame from the threaded video stream and resize it
#         # to have a maximum width of 400 pixels
#         frame = vs.read()
#         frame = imutils.resize(frame, width=400)
#
#         # grab the frame dimensions and convert it to a blob
#         (h, w) = frame.shape[:2]
#
#         if net is not None:
#             blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
#                                          (300, 300), (104.0, 177.0, 123.0))
#
#             # pass the blob through the network and obtain the detections and
#             # predictions
#             net.setInput(blob)
#             detections = net.forward()
#
#             # loop over the detections
#             for i in range(0, detections.shape[2]):
#                 # extract the confidence (i.e., probability) associated with the
#                 # prediction
#                 confidence = detections[0, 0, i, 2]
#
#                 # filter out weak detections by ensuring the `confidence` is
#                 # greater than the minimum confidence
#                 if confidence < confidence_min:
#                     continue
#                 else:
#                     # compute the (x, y)-coordinates of the bounding box for the
#                     # object
#                     frame_face = frame
#                     box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
#                     (startX, startY, endX, endY) = box.astype("int")
#
#                     # draw the bounding box of the face along with the associated
#                     # probability
#                     text = "{:.2f}%".format(confidence * 100)
#                     y = startY - 10 if startY - 10 > 10 else startY + 10
#                     cv2.rectangle(frame_face, (startX, startY), (endX, endY),
#                                   (0, 255, 0), 2)
#                     cv2.putText(frame_face, text, (startX, y),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
#                     cv2.imshow("Frame", cv2.flip(frame_face, -1))
#                     key = cv2.waitKey(5) & 0xFF
#                     return frame_face
#                 # break
#
#         # show the output frame
#         cv2.imshow("Frame", cv2.flip(frame, -1))
#         key = cv2.waitKey(1) & 0xFF
#
#         # if the `q` key was pressed, break from the loop
#         if key == ord("q"):
#             break
#
#     cv2.destroyAllWindows()
#     return frame


if __name__ == '__main__':
    print('detecting qrcode')
    camera_ = camera_pi()
    get_qrcode(camera_)
    print('detecting face')
    face_detect(camera_)

