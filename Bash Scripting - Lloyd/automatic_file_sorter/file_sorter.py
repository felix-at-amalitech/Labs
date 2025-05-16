#!/usr/bin/env python3

import os
import shutil
import sys
from ..utils import custom_logging_config
from datetime import datetime

# Set up logging
log_file = f"file_sorter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging = custom_logging_config(log_file=log_file)


SOURCE_DIR = sys.argv[1] or os.path.expanduser("~/Downloads")  # source directory is either either the first argument or the Downloads folder

if not os.path.exists(SOURCE_DIR):
    logging.error(f"Invalid source directory: {SOURCE_DIR}")
CATEGORIES = {
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.odt', '.rtf'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv'],
    'Music': ['.mp3', '.wav', '.flac', '.aac'],
    'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
    'Scripts': ['.py', '.sh', '.js', '.java', '.cpp'],
    'Others': []  # handles files that don't match any of the above categories 
}

def create_subfolders(base_dir):
    """Create subfolders for each category if they don't exist."""
    for category in CATEGORIES:
        folder_path = os.path.join(base_dir, category)
        try:
            os.makedirs(folder_path, exist_ok=True)# make directories if they don't exit and ignore if they do, no error will be raised.
            logging.info(f"Verified folder exists: {folder_path}")
        except Exception as e:
            logging.error(f"Failed to create folder {folder_path}: {e}")

def get_category(extension):
    """Return the category for a given file extension."""
    for category, extensions in CATEGORIES.items():
        if extension.lower() in extensions:
            return category
    return 'Others'

def sort_files(source_dir):
    """Scan the source directory and sort files into subfolders."""
    if not os.path.exists(source_dir):
        logging.error(f"Source directory {source_dir} does not exist.")
        return

    create_subfolders(source_dir)
    moved_files = 0
    skipped_files = 0

    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)

        # Skip directories and this script
        if os.path.isdir(file_path) or filename == os.path.basename(__file__):
            continue

        try:
            # Get file extension
            _, extension = os.path.splitext(filename)
            category = get_category(extension)
            destination_folder = os.path.join(source_dir, category)
            destination_path = os.path.join(destination_folder, filename)

            # Handle duplicate filenames
            if os.path.exists(destination_path):
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(destination_path):
                    new_filename = f"{base}_{counter}{ext}"
                    destination_path = os.path.join(destination_folder, new_filename)
                    counter += 1

            # Move the file
            shutil.move(file_path, destination_path)
            logging.info(f"Moved {filename} to {category}/{os.path.basename(destination_path)}")
            moved_files += 1

        except Exception as e:
            logging.error(f"Failed to move {filename}: {e}")
            skipped_files += 1

    logging.info(f"Sorting complete. Moved: {moved_files}, Skipped: {skipped_files}")

if __name__ == "__main__":
    logging.info("Starting file sorting script...")
    sort_files(SOURCE_DIR)
    logging.info("File sorting script finished.")