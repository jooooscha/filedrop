from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from PIL.ExifTags import TAGS
import os
import time

app = Flask(__name__)

# Specify the directory where uploaded files will be saved
UPLOAD_FOLDER = '/mnt/deponia/photoview/media/Pictures/TabeaUpload'
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
    if 'files' not in request.files:
        return "No file part"

    files = request.files.getlist('files')

    if not files or all(f.filename == '' for f in files):
        return "No selected files"

    for file in files:
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

if __name__ == '__main__':
    app.run(debug=True, port=8115)
