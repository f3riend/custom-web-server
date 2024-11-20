import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from pyngrok import ngrok


public_url = ngrok.connect(5000)
print(public_url.public_url)





app = Flask(__name__)



ALLOWED_EXTENSIONS = {
    'mp4': {'mp4', 'mov', 'avi', 'mkv', 'flv', 'wmv', 'webm', 'mpeg', '3gp'},
    'mp3': {'mp3', 'wav', 'aac', 'ogg', 'flac', 'm4a'},
    'img': {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp', 'tiff'}
}


app.config['UPLOAD_FOLDER'] = 'static'


def allowed_file(filename, file_type):
    extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return extension in ALLOWED_EXTENSIONS.get(file_type, set())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        
        filename = secure_filename(file.filename)
        
        
        if allowed_file(filename, 'mp4'):
            folder = 'mp4'
        elif allowed_file(filename, 'mp3'):
            folder = 'mp3'
        elif allowed_file(filename, 'img'):
            folder = 'img'
        else:
            return "Invalid file type", 400  
        
        
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
        os.makedirs(folder_path, exist_ok=True)
        
        
        file.save(os.path.join(folder_path, filename))
        return redirect(url_for('index'))
    
    
    mp4_files = [f for f in os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'mp4')) if f.endswith('.mp4')]
    mp3_files = [f for f in os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'mp3')) if f.endswith('.mp3')]
    img_files = [f for f in os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'img')) if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    return render_template('index.html', mp4_files=mp4_files, mp3_files=mp3_files, img_files=img_files)

if __name__ == '__main__':
    app.run(port=5000)
