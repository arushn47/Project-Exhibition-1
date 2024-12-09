from deepforest import main
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image

# Initialize DeepForest model
model = main.deepforest()
model.use_release()

def detect_trees(file):
    try:
        # Convert uploaded file to an image array
        image = np.array(Image.open(file))

        # Convert image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Make predictions
        predictions = model.predict_image(image_rgb)

        if predictions is None or len(predictions) == 0:
            return "No trees detected."

        # Count trees
        tree_count = len(predictions)

        # Visualize detections and save as output image
        for prediction in predictions:
            x_min, y_min, x_max, y_max = prediction['bbox']
            plt.gca().add_patch(plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, 
                                              linewidth=2, edgecolor='r', facecolor='none'))
        plt.imshow(image_rgb)
        output_path = "static/detected_trees.png"  # Save the detection output
        plt.savefig(output_path)
        plt.close()

        return f"Detected {tree_count} trees. Visualization saved to {output_path}."

    except Exception as e:
        return f"Error during tree detection: {e}"
