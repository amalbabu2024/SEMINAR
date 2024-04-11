from flask import Flask, render_template, request
from PIL import Image
from io import BytesIO
import base64
import subprocess
import os
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded file
    file = request.files['file']

    # Save the file to a temporary location
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Run YOLOv5 detection
    weights_path = 'yolov5/runs/train/exp13/weights/best.pt'
    output_dir = 'yolov5/runs/detect'
    command = f"python yolov5/detect.py --weights {weights_path} --img 640 --conf 0.25 --source {file_path} --save-txt --project {output_dir}"
    subprocess.run(command, shell=True)

    # Find the latest folder containing the output image
    exp_folders = [f for f in os.listdir(output_dir) if
                   os.path.isdir(os.path.join(output_dir, f)) and f.startswith("exp")]
    if exp_folders:
        latest_exp_folder = max(exp_folders, key=lambda x: int(x[3:]) if x[3:].isdigit() else -1)
        output_image_folder = os.path.join(output_dir, latest_exp_folder)

        # Wait for the output image to be created
        while not any(file.endswith(".jpg") for file in os.listdir(output_image_folder)):
            time.sleep(1)

        # Find the output image file
        output_image_files = [file for file in os.listdir(output_image_folder) if file.endswith(".jpg")]
        if output_image_files:
            output_image_path = os.path.join(output_image_folder, output_image_files[0])

            # Open the output image
            with open(output_image_path, 'rb') as f:
                image_data = f.read()
                encoded_image = base64.b64encode(image_data).decode('utf-8')

            # Convert the output image to base64 for display in HTML
            return render_template('result.html', image=encoded_image)

    return "Error processing image"


if __name__ == '__main__':
    app.run(debug=True)
