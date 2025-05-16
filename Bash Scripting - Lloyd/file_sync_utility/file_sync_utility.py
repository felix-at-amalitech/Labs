import os
import time
import hashlib
import json
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Setup logging config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class SyncHandler(FileSystemEventHandler):
    def __init__(self, folder_a, folder_b, metadata_file="sync_metadata.json"):
        self.folder_a = os.path.abspath(folder_a)
        self.folder_b = os.path.abspath(folder_b)
        self.metadata_file = metadata_file
        self.metadata = self._load_metadata()

    def _load_metadata(self):
        try:
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"a": {}, "b": {}}

    def _save_metadata(self):
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=4)

    def _get_file_metadata(self, filepath):
        try:
            timestamp = os.path.getmtime(filepath)
            size = os.path.getsize(filepath)
            with open(filepath, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            return {"timestamp": timestamp, "size": size, "hash": file_hash}
        except FileNotFoundError:
            return None

    def _sync_file(self, src_path, dest_path):
        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
            logger.info(f"Synced: {src_path} -> {dest_path}")
        except Exception as e:
            logger.error(f"Error syncing {src_path} to {dest_path}: {e}")

    def on_created(self, event):
        if event.is_directory:
            return
        src_path = os.path.abspath(event.src_path)
        if src_path.startswith(self.folder_a):
            rel_path = os.path.relpath(src_path, self.folder_a)
            dest_path = os.path.join(self.folder_b, rel_path)
            self._sync_file(src_path, dest_path)
            self.metadata['b'][rel_path] = self._get_file_metadata(dest_path)
        elif src_path.startswith(self.folder_b):
            rel_path = os.path.relpath(src_path, self.folder_b)
            dest_path = os.path.join(self.folder_a, rel_path)
            self._sync_file(src_path, dest_path)
            self.metadata['a'][rel_path] = self._get_file_metadata(dest_path)
        self._save_metadata()

    def on_deleted(self, event):
        if event.is_directory:
            return
        src_path = os.path.abspath(event.src_path)
        if src_path.startswith(self.folder_a):
            rel_path = os.path.relpath(src_path, self.folder_a)
            if rel_path in self.metadata['a']:
                dest_path = os.path.join(self.folder_b, rel_path)
                try:
                    os.remove(dest_path)
                    logger.info(f"Deleted: {dest_path}")
                except FileNotFoundError:
                    pass
                except Exception as e:
                    logger.error(f"Error deleting {dest_path}: {e}")
                self.metadata['b'].pop(rel_path, None)
                self.metadata['a'].pop(rel_path, None)
        elif src_path.startswith(self.folder_b):
            rel_path = os.path.relpath(src_path, self.folder_b)
            if rel_path in self.metadata['b']:
                dest_path = os.path.join(self.folder_a, rel_path)
                try:
                    os.remove(dest_path)
                    logger.info(f"Deleted: {dest_path}")
                except FileNotFoundError:
                    pass
                except Exception as e:
                    logger.error(f"Error deleting {dest_path}: {e}")
                self.metadata['a'].pop(rel_path, None)
                self.metadata['b'].pop(rel_path, None)
        self._save_metadata()

    def on_modified(self, event):
        if event.is_directory:
            return
        src_path = os.path.abspath(event.src_path)
        if src_path.startswith(self.folder_a):
            rel_path = os.path.relpath(src_path, self.folder_a)
            dest_path = os.path.join(self.folder_b, rel_path)
            current_meta_a = self._get_file_metadata(src_path)
            stored_meta_b = self.metadata['b'].get(rel_path)
            if stored_meta_b:
                if current_meta_a and current_meta_a['hash'] != stored_meta_b['hash']:
                    current_meta_b = self._get_file_metadata(dest_path)
                    if current_meta_b and current_meta_a['timestamp'] > current_meta_b['timestamp']:
                        self._sync_file(src_path, dest_path)
                        self.metadata['b'][rel_path] = current_meta_a
                    elif current_meta_b and current_meta_b['timestamp'] > current_meta_a['timestamp']:
                        self._sync_file(dest_path, src_path)
                        self.metadata['a'][rel_path] = current_meta_b
                    else:
                        self._handle_conflict(src_path, dest_path)
            elif current_meta_a:
                self._sync_file(src_path, dest_path)
                self.metadata['b'][rel_path] = current_meta_a
        elif src_path.startswith(self.folder_b):
            rel_path = os.path.relpath(src_path, self.folder_b)
            dest_path = os.path.join(self.folder_a, rel_path)
            current_meta_b = self._get_file_metadata(src_path)
            stored_meta_a = self.metadata['a'].get(rel_path)
            if stored_meta_a:
                if current_meta_b and current_meta_b['hash'] != stored_meta_a['hash']:
                    current_meta_a = self._get_file_metadata(dest_path)
                    if current_meta_b and current_meta_b['timestamp'] > current_meta_a['timestamp']:
                        self._sync_file(src_path, dest_path)
                        self.metadata['a'][rel_path] = current_meta_b
                    elif current_meta_a and current_meta_a['timestamp'] > current_meta_b['timestamp']:
                        self._sync_file(dest_path, src_path)
                        self.metadata['b'][rel_path] = current_meta_a
                    else:
                        self._handle_conflict(dest_path, src_path)
            elif current_meta_b:
                self._sync_file(src_path, dest_path)
                self.metadata['a'][rel_path] = current_meta_b
        self._save_metadata()

    def _handle_conflict(self, file_a, file_b):
        logger.warning(f"Conflict detected for: {os.path.basename(file_a)}")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(file_b)
        name, ext = os.path.splitext(base_name)
        new_name = f"{name}_conflict_{timestamp}{ext}"
        new_path = os.path.join(os.path.dirname(file_b), new_name)
        try:
            shutil.copy2(file_b, new_path)
            logger.info(f"Conflict resolved by keeping both. '{base_name}' saved as '{new_name}'")
            rel_new_path = os.path.relpath(new_path, self.folder_b)
            self.metadata['b'][rel_new_path] = self._get_file_metadata(new_path)
        except Exception as e:
            logger.error(f"Error handling conflict for {file_b}: {e}")


def initial_sync(folder_a, folder_b, handler):
    logger.info("Performing initial synchronization...")

    for root, _, files in os.walk(folder_a):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, folder_a)
            dest_path = os.path.join(folder_b, rel_path)

            meta_src = handler._get_file_metadata(src_path)
            meta_dest = handler.metadata['b'].get(rel_path)

            if meta_dest != meta_src:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)
                handler.metadata['b'][rel_path] = handler._get_file_metadata(dest_path)
                logger.info(f"Initial sync: {src_path} -> {dest_path}")
            handler.metadata['a'][rel_path] = meta_src

    for root, _, files in os.walk(folder_b):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, folder_b)
            dest_path = os.path.join(folder_a, rel_path)

            meta_src = handler._get_file_metadata(src_path)
            meta_dest = handler.metadata['a'].get(rel_path)

            if meta_dest != meta_src:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)
                handler.metadata['a'][rel_path] = handler._get_file_metadata(dest_path)
                logger.info(f"Initial sync: {src_path} -> {dest_path}")
            handler.metadata['b'][rel_path] = meta_src

    handler._save_metadata()
    logger.info("Initial synchronization complete.")


if __name__ == "__main__":
    folder_a = "folder_a"  # Replace with your first folder path
    folder_b = "folder_b"  # Replace with your second folder path

    os.makedirs(folder_a, exist_ok=True)
    os.makedirs(folder_b, exist_ok=True)

    handler = SyncHandler(folder_a, folder_b)
    initial_sync(folder_a, folder_b, handler)

    observer_a = Observer()
    observer_a.schedule(handler, folder_a, recursive=True)
    observer_a.start()

    observer_b = Observer()
    observer_b.schedule(handler, folder_b, recursive=True)
    observer_b.start()

    logger.info(f"Monitoring changes in '{folder_a}' and '{folder_b}'... Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping observers...")
        observer_a.stop()
        observer_b.stop()

    observer_a.join()
    observer_b.join()
