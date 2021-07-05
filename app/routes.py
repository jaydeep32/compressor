from app import app
from flask import render_template, request, send_file
from werkzeug.utils import secure_filename
from PIL import Image
from app.compress import compress_video
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_file/<path:filename>')
def download_file(filename):
    print("Heer")
    return send_file(app.config['upload_folder'] / 'images' / filename, as_attachment=True)


def save_image(image):
    data = request.form
    try:
        quality = int(data.get('quality')) if data.get('quality') else 75
    except ValueError:
        quality = 75
    else:
        img = Image.open(image)
        filename = secure_filename(image.filename)
        path = app.config['upload_folder'] / 'images' / filename
        img.save(path, optimize = True, quality = quality)
        msg = 'File saved!'
        label = 'success'
    return {'label': label, 'error': msg, 'filename': filename}


def save_pdf(pdf):
    print(dir(pdf))
    print(pdf)


def save_video(video):
    filename = secure_filename(video.filename)
    path = app.config['upload_folder'] / 'videos' / filename
    video.save(path)

    old_f_size = path.stat().st_size
    new_file = compress_video(path)
    new_f_size = new_file.stat().st_size
    os.remove(path)
    diff = 100 - ((new_f_size * 100) / old_f_size)
    return {'diffrence': diff,'filename': new_file.name}


@app.route('/file_upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        file = request.files['file']
        if any(map(file.filename.endswith, app.config['image_extention'])):
            return save_image(file)
        elif file.filename.endswith('pdf'):
            filename = secure_filename(file.filename)
            return save_pdf(file)
        elif any(map(file.filename.endswith, app.config['video_extention'])):
            return save_video(file)
        else:
            res = {'label': 'danger', 'error': 'Not a imgae!'}
    else:
        res = {}
    return render_template('file_upload.html', message=res)

