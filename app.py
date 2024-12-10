from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import shutil

app = Flask(__name__, static_folder='static', template_folder='templates')

# Using Vercel's temporary directory for uploads
UPLOAD_FOLDER = '/tmp/uploads/'
RESULTS_FOLDER = '/tmp/results/'

# Ensure that the results folder exists
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Allowed file extensions for image upload
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Simulated tree detection (replace with actual processing logic)
def detect_trees(image_path):
    # Simulate processing by copying the uploaded image to a new result
    result_image_path = os.path.join(RESULTS_FOLDER, "detected_trees.png")
    
    # For now, we'll just copy the file (replace with real detection logic)
    shutil.copy(image_path, result_image_path)
    
    return result_image_path

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    image_path = None

    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Save the file temporarily
            file.save(file_path)

            try:
                # Perform tree detection
                result_image_path = detect_trees(file_path)
                print(f"Result: {result_image_path}")

                # After processing, set the path to the result image
                image_path = f"/static/results/{os.path.basename(result_image_path)}"

                # Optional: Clean up the uploaded image after processing
                os.remove(file_path)
            except Exception as e:
                result = f"Error processing image: {str(e)}"
                print(f"Error: {str(e)}")
                image_path = None

    return render_template('index.html', result=result, image_path=image_path)


if __name__ == "__main__":
    app.run(debug=True)
