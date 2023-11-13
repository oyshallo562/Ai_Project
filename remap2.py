import os
import threading
from PIL import Image

def normalize_coordinates(txt_file, image_file):
    try:
        with Image.open(image_file) as img:
            img_width, img_height = img.size
    except IOError:
        print(f"Could not read image: {image_file}")
        return

    with open(txt_file, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 5:
            class_id, x_center, y_center, width, height = parts
            # Normalize coordinates
            x_center = float(x_center) / img_width
            y_center = float(y_center) / img_height
            width = float(width) / img_width
            height = float(height) / img_height
            new_line = f"{class_id} {x_center} {y_center} {width} {height}\n"
            new_lines.append(new_line)

    # Write the normalized coordinates back to the file
    with open(txt_file, 'w') as file:
        file.writelines(new_lines)

def process_file(txt_file, images_directory):
    image_file = os.path.join(images_directory, os.path.splitext(os.path.basename(txt_file))[0] + '.jpg')
    if os.path.exists(image_file):
        normalize_coordinates(txt_file, image_file)

def process_directory(directory, images_directory, num_threads=10):
    threads = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                txt_file = os.path.join(root, file)
                thread = threading.Thread(target=process_file, args=(txt_file, images_directory))
                threads.append(thread)
                thread.start()

                while threading.active_count() > num_threads:
                    pass

    for thread in threads:
        thread.join()

# Example usage
txt_directory = 'A:/dataset_yolo/images/val/labels'  # Update with your path
images_directory = 'A:/dataset_yolo/images/val/images'  # Path to the corresponding images
process_directory(txt_directory, images_directory)
