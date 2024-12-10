from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

# Define both static and template folders
app = Flask(__name__, static_folder='static', template_folder='templates')

# Define folder paths
UPLOAD_FOLDER = 'static/uploads/'
RESULTS_FOLDER = 'static/results/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Check if file is allowed (based on extension)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Define a dummy tree detection function
def detect_trees(image_path):
    # Your image processing logic for detecting trees goes here
    # For now, just return a dummy result.
    return "Detected trees in the image."

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    image_path = None
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            result = detect_trees(file_path)
            print(f"Result: {result}") 

            image_path = "/static/results/detected_trees.png"

    return render_template('index.html', result=result, image_path=image_path)


if __name__ == "__main__":
    app.run(debug=True)