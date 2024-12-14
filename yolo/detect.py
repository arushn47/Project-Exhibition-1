from ultralytics import YOLO
import os
from PIL import Image, ImageDraw

def remove_labels_and_save(image_path, boxes, save_path):
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    for box in boxes.xyxy:
        x1, y1, x2, y2 = map(int, box[:4])
        draw.rectangle([x1, y1, x2, y2], outline="lime", width=2)

    image.save(save_path)

model = YOLO('yolo/tree-detection-model.pt') 
input_dir = 'static/images/uploads'
output_dir = 'static/images/results'
os.makedirs(output_dir, exist_ok=True)

tree_count = 0  # Initialize tree count variable

for image_name in os.listdir(input_dir):
    image_path = os.path.join(input_dir, image_name)
    if os.path.isfile(image_path):
        results = model.predict(source=image_path, conf=0.05, iou=0.1, max_det=100, amp=True)

        for result in results:
            boxes = result.boxes
            tree_count += len(boxes)

            save_path = os.path.join(output_dir, image_name)
            remove_labels_and_save(image_path, boxes, save_path)

        print(f"Processed {image_name}: {tree_count} trees detected.")
        # Save tree_count to a file for later retrieval
        with open(f"{output_dir}/{image_name}_tree_count.txt", "w") as f:
            f.write(str(tree_count))
