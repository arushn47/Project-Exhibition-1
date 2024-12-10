from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

UPLOAD_FOLDER = 'static/uploads/'
RESULTS_FOLDER = 'static/results/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def detect_trees(image_path):
    # Replace with your actual tree detection logic
    result_image_path = os.path.join(RESULTS_FOLDER, "detected_trees.png")
    # Assuming you process the image and save the result here
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
            file.save(file_path)

            try:
                # Perform tree detection
                result_image_path = detect_trees(file_path)
                print(f"Result: {result_image_path}")

                # After processing, you can set the path to the generated result image
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