from app import app
from flask import render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
from app.pdf_compressor import compress

@app.route('/')
def index():
    return render_template('index.html')


def save_image(image):
    data = request.form
    try:
        quality = int(data['quality']) if data['quality'] else 40
    except ValueError:
        quality = 40
    else:
        img = Image.open(image)
        filename = secure_filename(image.filename)
        img.save(app.config['upload_folder'] / 'images' / filename, optimize = True, quality = quality)
        msg = 'File saved!'
        label = 'success'
    return {'label': label, 'error': msg}


def save_pdf(pdf):
    print(dir(pdf))
    print(pdf)


@app.route('/file_upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        file = request.files['file']
        if any(map(file.filename.endswith, app.config['image_extention'])):
            res = save_image(file)
        elif file.filename.endswith('pdf'):
            print("pdf")
            filename = secure_filename(file.filename)
            # compress('static/'+file.filename, app.config['upload_folder'] / 'pdf' / filename)
            save_pdf(file)
            res = {'label': 'success', 'error': 'PDF!'}
        else:
            res = {'label': 'danger', 'error': 'Not a imgae!'}
    else:
        res = {}
    return render_template('file_upload.html', message=res)


