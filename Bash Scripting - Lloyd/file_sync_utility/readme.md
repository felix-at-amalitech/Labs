# Folder Sync with Watchdog

This Python script synchronizes two folders bidirectionally in real-time. It monitors changes such as file creation, modification, and deletion in both folders and keeps them in sync. The script also handles basic conflict resolution by keeping both conflicting versions.

---

## Features

- Real-time synchronization between two folders using `watchdog`.
- Detects and syncs created, modified, and deleted files.
- Maintains metadata (file hash, size, modification time) for efficient sync.
- Basic conflict resolution by renaming conflicting files with a timestamp.
- Logging implemented for informative output and error handling.

---

## Requirements

- Python 3.6+
- Required Python packages:
  - watchdog

Install dependencies using pip:

```bash
pip install watchdog
```

## Usage

1. Update the folder paths in the script or run as-is to sync folder_a and folder_b in the current directory.

2. Run the script:

    ```bash
    python sync_folders.py
    ```

3. The script performs an initial sync between the two folders.

4. It then monitors both folders for any changes and synchronizes them in real-time.

5. To stop the script, press Ctrl+C.

## Notes

- The script assumes both folders are on the same filesystem and accessible.
- For large files or frequent changes, performance may vary.
- The conflict resolution is basic and can be extended as needed.
