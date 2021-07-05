from flask import Flask
from pathlib import Path

app = Flask(__name__)

from app import routes

UPLOAD_FOLDER = Path.cwd() / 'app' / 'static'
app.config['upload_folder'] = UPLOAD_FOLDER

IMAGE_EXTENTION = {'png', 'jpg', 'jpeg'}
app.config['image_extention'] = IMAGE_EXTENTION

VIDEO_EXTENTION = {'mp4', 'mov', 'wmv', 'flv', 'avi', 'avchd', 'webm', 'mkv'}
app.config['video_extention'] = VIDEO_EXTENTION