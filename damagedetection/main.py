from tkinter import Tk, Button, Label
from tkinter import filedialog
import tkinter as tk
import subprocess
import os
import time
from PIL import Image, ImageTk

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        detect_image(file_path)

def detect_image(file_path):
    weights_path = 'yolov5/runs/train/exp13/weights/best.pt'
    output_dir = 'yolov5/runs/detect'

    command = f"python yolov5/detect.py --weights {weights_path} --img 640 --conf 0.25 --source {file_path} --save-txt --project {output_dir}"
    subprocess.run(command, shell=True)

    # Find the latest folder containing the output image
    exp_folders = [f for f in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, f)) and f.startswith("exp")]
    if exp_folders:
        latest_exp_folder = max(exp_folders, key=lambda x: int(x[3:]) if x[3:].isdigit() else -1)
        output_image_folder = os.path.join(output_dir, latest_exp_folder)

        # Wait for the output image to be created
        while not any(file.endswith(".jpg") for file in os.listdir(output_image_folder)):
            time.sleep(1)

        # Add a delay to ensure file writing is complete
        time.sleep(1)

        # Find the output image file
        output_image_files = [file for file in os.listdir(output_image_folder) if file.endswith(".jpg")]
        if output_image_files:
            output_image_path = os.path.join(output_image_folder, output_image_files[0])

            # Open the image with PIL and convert it to a format that PhotoImage can handle
            pil_image = Image.open(output_image_path)
            output_image = ImageTk.PhotoImage(pil_image.resize((640, 480)))  # Resize the image to fit the label

            # Display the output image
            output_label.config(image=output_image)
            output_label.image = output_image
        else:
            print("No output image files found")
    else:
        print("No output folders found or folders do not match expected format")

# Create the main window
root = tk.Tk()
root.title("YOLOv5 Image Detector")
root.geometry("800x600")  # Set the initial size of the window

# Create a button to upload an image
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack()

# Create a label to display the output image
output_label = tk.Label(root, width=640, height=480)
output_label.pack()

# Start the tkinter main loop
root.mainloop()
