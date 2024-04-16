# from flask import Flask, render_template, request
# from PIL import Image
# from io import BytesIO
# import base64
# import subprocess
# import os
# import time
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/upload', methods=['POST'])
# def upload():
#     # Get the uploaded file
#     file = request.files['file']
#
#     # Save the file to a temporary location
#     file_path = os.path.join('uploads', file.filename)
#     file.save(file_path)
#
#     # Run YOLOv5 detection
#     weights_path = 'yolov5/runs/train/exp13/weights/best.pt'
#     output_dir = 'yolov5/runs/detect'
#     command = f"python yolov5/detect.py --weights {weights_path} --img 640 --conf 0.25 --source {file_path} --save-txt --project {output_dir}"
#     subprocess.run(command, shell=True)
#
#     # Find the latest folder containing the output image
#     exp_folders = [f for f in os.listdir(output_dir) if
#                    os.path.isdir(os.path.join(output_dir, f)) and f.startswith("exp")]
#     if exp_folders:
#         latest_exp_folder = max(exp_folders, key=lambda x: int(x[3:]) if x[3:].isdigit() else -1)
#         output_image_folder = os.path.join(output_dir, latest_exp_folder)
#
#         # Wait for the output image to be created
#         while not any(file.endswith(".jpg") for file in os.listdir(output_image_folder)):
#             time.sleep(1)
#
#         # Find the output image file
#         output_image_files = [file for file in os.listdir(output_image_folder) if file.endswith(".jpg")]
#         if output_image_files:
#             output_image_path = os.path.join(output_image_folder, output_image_files[0])
#
#             # Open the output image
#             with open(output_image_path, 'rb') as f:
#                 image_data = f.read()
#                 encoded_image = base64.b64encode(image_data).decode('utf-8')
#
#             # Convert the output image to base64 for display in HTML
#             return render_template('result.html', image=encoded_image)
#
#     return "Error processing image"
#
#
# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, render_template, request, redirect, url_for
# from werkzeug.utils import secure_filename
# import os
# import subprocess
# import time
#
# app = Flask(__name__)
#
# # Specify the allowed file extensions
# ALLOWED_EXTENSIONS = {'mp4'}
#
# # Define the upload folder
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
#
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return redirect(request.url)
#
#     file = request.files['file']
#
#     if file.filename == '':
#         return redirect(request.url)
#
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
#
#         # Run YOLOv5 detection
#         weights_path = 'yolov5/runs/train/exp13/weights/best.pt'
#         output_dir = 'yolov5/runs/detect'
#         command = f"python yolov5/detect.py --weights {weights_path} --img 640 --conf 0.25 --source {file_path} --save-txt --project {output_dir}"
#         subprocess.run(command, shell=True)
#
#         # Find the latest folder containing the output video
#         exp_folders = [f for f in os.listdir(output_dir) if
#                        os.path.isdir(os.path.join(output_dir, f)) and f.startswith("exp")]
#         if exp_folders:
#             latest_exp_folder = max(exp_folders, key=lambda x: int(x[3:]) if x[3:].isdigit() else -1)
#             output_video_folder = os.path.join(output_dir, latest_exp_folder)
#
#             # Wait for the output video to be created
#             while not any(file.endswith(".mp4") for file in os.listdir(output_video_folder)):
#                 time.sleep(1)
#
#             # Find the output video file
#             output_video_files = [file for file in os.listdir(output_video_folder) if file.endswith(".mp4")]
#             if output_video_files:
#                 output_video_path = os.path.join(output_video_folder, output_video_files[0])
#
#                 # Render the result page with the video
#                 return render_template('result.html', video=output_video_path)
#
#     return "Error processing file"
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

















from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import subprocess
import time
import base64

app = Flask(__name__)

# Specify the allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'mp4'}

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Run YOLOv5 detection
        weights_path = 'yolov5/runs/train/exp13/weights/best.pt'
        output_dir = 'yolov5/runs/detect'
        command = f"python yolov5/detect.py --weights {weights_path} --img 640 --conf 0.25 --source {file_path} --save-txt --project {output_dir}"
        subprocess.run(command, shell=True)

        # Find the latest folder containing the output video or image
        exp_folders = [f for f in os.listdir(output_dir) if
                       os.path.isdir(os.path.join(output_dir, f)) and f.startswith("exp")]
        if exp_folders:
            latest_exp_folder = max(exp_folders, key=lambda x: int(x[3:]) if x[3:].isdigit() else -1)
            output_folder = os.path.join(output_dir, latest_exp_folder)

            # Wait for the output file to be created
            while not any(file.endswith((".jpg", ".mp4")) for file in os.listdir(output_folder)):
                time.sleep(1)

            # Find the output file
            output_files = [file for file in os.listdir(output_folder) if file.endswith((".jpg", ".mp4"))]
            if output_files:
                output_file = output_files[0]
                output_file_path = os.path.join(output_folder, output_file)

                # Determine if it's an image or video
                if output_file.endswith(".jpg"):
                    with open(output_file_path, 'rb') as f:
                        image_data = f.read()
                        encoded_image = base64.b64encode(image_data).decode('utf-8')

                    # Return image result
                    return render_template('result.html', file=output_file, image=encoded_image)
                elif output_file.endswith(".mp4"):
                    video_url = url_for('static', filename=f'yolov5/runs/detect/{latest_exp_folder}/{output_file}')
                    return render_template('result.html', file=output_file, video=video_url)

    return "Error processing file"



if __name__ == '__main__':
    app.run(debug=True)
