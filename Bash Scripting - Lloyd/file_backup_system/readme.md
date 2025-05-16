# File Backup Utility

A robust Python-based command-line tool for performing **full** or **partial** backups of directories, with options for compression and scheduled automation.

## Features

- Full or partial backups
- Optional ZIP compression
- Scheduled backups (hourly, daily, weekly)
- Filters for file extensions and modified time (partial backups)
- Intelligent directory structure preservation
- Logs all activity to `backup.log`

---

## Requirements

- Python 3.6+
- [schedule](https://pypi.org/project/schedule/) library (install via `pip install schedule`)

---

## Usage

```bash
python backup_manager.py SOURCE DESTINATION [OPTIONS]
```

## Required arguments

**SOURCE**: The source directory to back up.
**DESTINATION**: The directory where backups will be stored.

| Option                               | Description                                                    |
| ------------------------------------ | -------------------------------------------------------------- |
| `--type {full, partial}`             | Type of backup to perform (default: `full`)                    |
| `--compress`                         | Create a ZIP archive instead of copying files                  |
| `--extensions .ext1 .ext2 ...`       | Only back up files with these extensions (for partial backups) |
| `--schedule {hourly, daily, weekly}` | Schedule automatic recurring backups                           |

## Logging

- All operations and errors are recorded in a backup.log file in the script’s directory. This includes:
- Start and completion of backups
- Paths created
- Any errors or skipped files

## Error Handling

- The tool gracefully handles:
- Missing source directories
- Permission errors
- Zip file write failures
- Destination path issues

## Development Notes

- This utility is ideal for:
- Backing up user files
- Automating backups for critical data folders
- Selective backup of recent or relevant files

## Future enhancements could include

- Time-based filtering (e.g., last modified within N days)
- Email alerts for failures
- Backup restore capabilities
