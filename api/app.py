from flask import Flask, render_template, request
from detect import detect_trees

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    image_path = None
    if request.method == 'POST':
        file = request.files['image']
        if file:
            result = detect_trees(file)
            image_path = "static/detected_trees.png"  # Path to the saved visualization
    return render_template('index.html', result=result, image_path=image_path)

if __name__ == "__main__":
    app.run(debug=True)