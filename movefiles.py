import os
import shutil
import threading
from pathlib import Path

def move_files(file_extension, source_folder, target_folder):
    """
    Moves files with the specified extension from the source folder to the target folder.
    """
    for file in Path(source_folder).glob(f'*{file_extension}'):
        shutil.move(str(file), target_folder)

def move_jpg_files(source_folder, target_folder):
    """
    Thread function to move JPG files.
    """
    move_files('.jpg', source_folder, target_folder)

def move_txt_files(source_folder, target_folder):
    """
    Thread function to move TXT files.
    """
    move_files('.txt', source_folder, target_folder)

# Example usage
source_folder = 'A:/dataset_yolo/images/val'  # Replace with the path to your source folder
images_folder = 'A:/dataset_yolo/images/val/images'  # Replace with the path to your images folder
labels_folder = 'A:/dataset_yolo/images/val/labels'  # Replace with the path to your labels folder

# Create threads
jpg_thread = threading.Thread(target=move_jpg_files, args=(source_folder, images_folder))
txt_thread = threading.Thread(target=move_txt_files, args=(source_folder, labels_folder))

# Start threads
jpg_thread.start()
txt_thread.start()

# Wait for threads to finish
jpg_thread.join()
txt_thread.join()

"Threads have been started to move JPG and TXT files. Please check the target folders after the process completes."