from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from PIL.ExifTags import TAGS
import os
import time
import logging
import sys
from waitress import serve
import logging

app = Flask(__name__, root_path="app/")

# Specify the directory where uploaded files will be saved
if len(sys.argv) != 2:
    exit("Please specify the upload directory using the first argument")


UPLOAD_FOLDER = sys.argv[1]
print(f"Writing uploads to '{UPLOAD_FOLDER}'")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_photo_taken_time(image):
    exif = image._getexif()
    if exif:
        for tag, value in exif.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'DateTimeOriginal':
                return value
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    app.logger.debug(f"Reqeust: {request}")
    app.logger.debug(f"Reqeust: {request.files}")

    for name, file in request.files.items():
        app.logger.info(f"File: {file}")
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Open the image and extract EXIF data
            image = Image.open(filepath)
            photo_taken_time = get_photo_taken_time(image)

            if photo_taken_time:
                # Convert photo_taken_time to a timestamp and set it as the file's last modified time
                struct_time = time.strptime(photo_taken_time, "%Y:%m:%d %H:%M:%S")
                timestamp = time.mktime(struct_time)
                os.utime(filepath, (timestamp, timestamp))

    return render_template('upload_success.html')

def main():
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.DEBUG)
    serve(app, host="127.0.0.1", port=8115)

if __name__ == '__main__':
    main()
