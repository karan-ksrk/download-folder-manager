import sys
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import shutil
from pathlib import Path
from logging.handlers import RotatingFileHandler
import threading

from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

# Setup Rotating Logs
log_handler = RotatingFileHandler(
    'created_file_log.txt',
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=3
)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
log_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

DOWNLOAD_FOLDER_PATH = 'C:\\Users\\Karan\\Downloads'

extension_mapping = {
    'Image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'],
    'Video': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', ".mpg"],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
    'Text': ['.txt', '.doc', '.docx', '.pdf', '.csv', '.xls', '.xlsx', '.ppt', '.pptx'],
    'Zip': ['.zip', '.rar', '.tar', '.gz', '.7z'],
    'Executable': ['.exe', '.msi', '.bat', '.sh']
}

FOLDER_PATHS = {
    'Image': Path(DOWNLOAD_FOLDER_PATH) / 'Images',
    'Video': Path(DOWNLOAD_FOLDER_PATH) / 'Videos',
    'Audio': Path(DOWNLOAD_FOLDER_PATH) / 'Audios',
    'Text': Path(DOWNLOAD_FOLDER_PATH) / 'Text',
    'Zip': Path(DOWNLOAD_FOLDER_PATH) / 'Zips',
    'Executable': Path(DOWNLOAD_FOLDER_PATH) / 'Executables',
    'Other': Path(DOWNLOAD_FOLDER_PATH) / 'Others'
}

# Create destination folders
for folder in FOLDER_PATHS.values():
    os.makedirs(folder, exist_ok=True)

# Watchdog Handler
class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        for folder in FOLDER_PATHS.values():
            try:
                if folder in file_path.parents:
                    return
            except Exception as e:
                logger.error(f"Error checking folder exclusion: {e}")
                return

        file_name = file_path.name
        file_extension = file_path.suffix.lower()
        file_type = 'Other'

        for key, extensions in extension_mapping.items():
            if file_extension in extensions:
                file_type = key
                break

        destination = FOLDER_PATHS[file_type] / file_name

        try:
            shutil.move(str(file_path), str(destination))
            logger.info(f'New {file_type} file created: {destination}')
        except Exception as e:
            logger.error(f"Failed to move {file_path} to {destination}: {e}")

# Threaded Watcher
def start_observer():
    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOAD_FOLDER_PATH, recursive=False)
    observer.start()
    logger.info("Download organizer started.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# System Tray Icon
def create_image():
    # Simple black square icon
    image = Image.new('RGB', (64, 64), 'black')
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill='white')
    return image

def on_quit(icon, item):
    logger.info("Exiting download organizer.")
    icon.stop()
    os._exit(0)

def main():
    threading.Thread(target=start_observer, daemon=True).start()

    icon = Icon(
        "DownloadOrganizer",
        create_image(),
        menu=Menu(MenuItem("Quit", on_quit))
    )
    icon.run()

if __name__ == "__main__":
    main()
