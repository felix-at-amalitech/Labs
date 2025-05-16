import os
import shutil
import zipfile
import schedule
import time
import datetime
import logging
from pathlib import Path
import argparse

# Set up logging
logging.basicConfig(
    filename='backup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BackupManager:
    def __init__(self, source_dir, dest_dir, compress=False):
        self.source_dir = Path(source_dir)
        self.dest_dir = Path(dest_dir)
        self.compress = compress
        self.backup_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def validate_paths(self):
        """Validate source and destination paths."""
        if not self.source_dir.exists():
            logging.error(f"Source directory {self.source_dir} does not exist.")
            raise ValueError(f"Source directory {self.source_dir} does not exist.")
        if not self.dest_dir.exists():
            logging.info(f"Creating destination directory {self.dest_dir}")
            self.dest_dir.mkdir(parents=True)

    def full_backup(self):
        """Perform a full backup of the source directory."""
        self.validate_paths()
        backup_path = self.dest_dir / f"full_backup_{self.backup_time}"
        
        try:
            if self.compress:
                backup_zip = backup_path.with_suffix('.zip')
                logging.info(f"Creating compressed full backup: {backup_zip}")
                with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for root, _, files in os.walk(self.source_dir):
                        for file in files:
                            file_path = Path(root) / file
                            rel_path = file_path.relative_to(self.source_dir)
                            zf.write(file_path, rel_path)
                logging.info(f"Full compressed backup completed: {backup_zip}")
            else:
                shutil.copytree(self.source_dir, backup_path)
                logging.info(f"Full backup completed: {backup_path}")
        except Exception as e:
            logging.error(f"Full backup failed: {str(e)}")
            raise

    def partial_backup(self, file_extensions=None, modified_after=None):
        """Perform a partial backup based on file extensions or modification time."""
        self.validate_paths()
        backup_path = self.dest_dir / f"partial_backup_{self.backup_time}"
        
        try:
            if self.compress:
                backup_zip = backup_path.with_suffix('.zip')
                logging.info(f"Creating compressed partial backup: {backup_zip}")
                with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for root, _, files in os.walk(self.source_dir):
                        for file in files:
                            file_path = Path(root) / file
                            if self._should_backup_file(file_path, file_extensions, modified_after):
                                rel_path = file_path.relative_to(self.source_dir)
                                zf.write(file_path, rel_path)
                logging.info(f"Partial compressed backup completed: {backup_zip}")
            else:
                backup_path.mkdir()
                for root, _, files in os.walk(self.source_dir):
                    for file in files:
                        file_path = Path(root) / file
                        if self._should_backup_file(file_path, file_extensions, modified_after):
                            rel_path = file_path.relative_to(self.source_dir)
                            dest_file = backup_path / rel_path
                            dest_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(file_path, dest_file)
                logging.info(f"Partial backup completed: {backup_path}")
        except Exception as e:
            logging.error(f"Partial backup failed: {str(e)}")
            raise

    def _should_backup_file(self, file_path, file_extensions, modified_after):
        """Determine if a file should be backed up based on criteria."""
        if file_extensions and file_path.suffix.lower() not in [ext.lower() for ext in file_extensions]:
            return False
        if modified_after:
            file_mtime = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
            if file_mtime < modified_after:
                return False
        return True

    @staticmethod
    def schedule_backup(backup_type, source_dir, dest_dir, compress, interval, file_extensions=None):
        """Schedule a backup to run at specified intervals."""
        def job():
            backup = BackupManager(source_dir, dest_dir, compress)
            if backup_type == "full":
                backup.full_backup()
            else:
                backup.partial_backup(file_extensions=file_extensions)
        
        if interval == "daily":
            schedule.every().day.at("02:00").do(job)
        elif interval == "weekly":
            schedule.every().monday.at("02:00").do(job)
        elif interval == "hourly":
            schedule.every().hour.do(job)
        
        logging.info(f"Scheduled {backup_type} backup with {interval} interval")
        while True:
            schedule.run_pending()
            time.sleep(60)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="File Backup Utility")
    parser.add_argument("source", help="Source directory to back up")
    parser.add_argument("destination", help="Destination directory for backups")
    parser.add_argument("--type", choices=["full", "partial"], default="full", 
                       help="Backup type (full or partial)")
    parser.add_argument("--compress", action="store_true", help="Compress backup")
    parser.add_argument("--extensions", nargs="*", help="File extensions for partial backup (e.g., .txt .doc)")
    parser.add_argument("--schedule", choices=["hourly", "daily", "weekly"], 
                       help="Schedule backup interval")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    try:
        if args.schedule:
            BackupManager.schedule_backup(
                backup_type=args.type,
                source_dir=args.source,
                dest_dir=args.destination,
                compress=args.compress,
                interval=args.schedule,
                file_extensions=args.extensions
            )
        else:
            backup = BackupManager(args.source, args.destination, args.compress)
            if args.type == "full":
                backup.full_backup()
            else:
                backup.partial_backup(file_extensions=args.extensions)
    except Exception as e:
        logging.error(f"Backup operation failed: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()