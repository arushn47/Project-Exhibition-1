from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import subprocess
import shutil

app = Flask(__name__, static_folder='static', template_folder='templates')

UPLOAD_FOLDER = 'static/images/uploads/'
RESULTS_FOLDER = 'static/images/results/exp'
YOLO_SCRIPT = 'yolo/detect.py'
ARCHIVE_FOLDER = 'static/images/archive'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            try:
                subprocess.run(
                    ['python', YOLO_SCRIPT], check=True
                )

                archive_file_path = os.path.join(ARCHIVE_FOLDER, filename)
                shutil.move(file_path, archive_file_path)

                result_image_path = os.path.join(RESULTS_FOLDER, 'exp', filename)
                image_path = f"images/results/exp/{filename}"

                return redirect(url_for('result', image_path=image_path))

            except Exception as e:
                return f"Error processing image: {str(e)}"

    return render_template('index.html')

@app.route('/images/result')
def result():
    image_path = request.args.get('image_path')
    return render_template('result.html', image_path=image_path)

@app.route('/cleanup', methods=['POST'])
def cleanup():
    try:
        results_folder = app.config['RESULTS_FOLDER']

        if os.path.exists(results_folder):
            shutil.rmtree(results_folder)

        return "Cleanup complete", 200
    except Exception as e:
        return f"Error during cleanup: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)