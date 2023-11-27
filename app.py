


import argparse
from PIL import Image
import datetime

import torch
import cv2
import numpy as np
import tensorflow as tf
from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, url_for, Response, send_file
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
from subprocess import Popen
import re
import requests
import shutil
import time
import glob


from ultralytics import YOLO

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html', image_path=None, video_feed=None)

@app.route("/", methods=["POST"])
def predict_img():
    image_path = None
    video_feed = None

    if 'file' in request.files:
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, 'uploads', f.filename)
        print("upload folder is ", filepath)
        f.save(filepath)

        file_extension = f.filename.rsplit('.', 1)[1].lower()

        valid_extension = ['jpg', 'jpeg', 'png']

        if file_extension in valid_extension:
            img = cv2.imread(filepath)
            frame = cv2.imencode('.jpg',cv2.UMat(img))[1].tobytes()

            image = Image.open(io.BytesIO(frame))

            # detection
            yolo = YOLO('best.pt')
            detection = yolo.predict(image,save=True, source = '/runs/detect')

            folder_path = '/runs/detect'
            subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
            latest_subfolder = max(subfolders, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
            image_path = folder_path + '/' + latest_subfolder + '/' + f.filename



    return render_template('index.html', image_path=image_path, video_feed=video_feed)


@app.route('/<path:filename>')
def display(filename):
    folder_path = '/runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    latest_subfolder = max(subfolders, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
    directory = folder_path+'/'+latest_subfolder
    print("printing the directory", directory)
    files = os.listdir(directory)
    latest_file = files[0]

    print(latest_file)

    filename = os.path.join(folder_path, latest_subfolder, latest_file)

    file_extension = filename.rsplit('.', 1)[1].lower()

    environ = request.environ

    if file_extension == valid_extension:
        return send_from_directory(directory, latest_file,environ)
    else:
        return "Formate Your File in jpg or jpeg or png"

def get_frame():
    folder_path = os.getcwd()
    mp4_files = 'output.mp4'
    video = cv2.VideoCapture(mp4_files)
    while True:
        success, image = video.read()
        if not success:
            break
        ret, jpeg = video.read()

        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

        time.sleep(0.1)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Koala Detection using YOLOv8')
    parser.add_argument('--port', type=int, default=5000, help='port number')
    args = parser.parse_args()
    model = YOLO('best.pt')
    app.run(host = "0.0.0.0", port = args.port)
    