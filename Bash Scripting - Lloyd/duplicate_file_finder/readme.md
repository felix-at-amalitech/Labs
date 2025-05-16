# Duplicate File Finder

A Python utility to scan a directory for duplicate files based on file size and MD5 hash. Optionally, users can delete or move duplicates to a separate folder.

## Features

- Detects duplicate files by comparing content using MD5 hashing
- Efficient initial filtering by file size
- Options to:
  - Delete duplicate files (keeping the first copy)
  - Move duplicates to a designated folder
- Displays total size of duplicates
- Handles permission and I/O errors gracefully

## Requirements

- Python 3.6 or higher
- No external dependencies are required.

## Usage

Run the script from the terminal in the duplicate_finder.py directory:

```bash
python duplicate_finder.py
```

## Example output

```code
Enter the directory path to scan: /path/to/folder
Scanning directory: /path/to/folder

Duplicate files found:

Hash: d41d8cd98f00b204e9800998ecf8427e
  1. /path/to/folder/file1.txt (1.20 KB)
  2. /path/to/folder/subdir/file1_copy.txt (1.20 KB)

Total size of duplicates: 0.00 MB

Options:
1. Delete duplicates (keep first file)
2. Move duplicates to a folder
3. Exit
Select an option (1-3):
```

## Notes

Only files (not directories) are scanned.

Hash comparison is only done for files with the same size, optimizing performance.

Duplicate detection is case-sensitive and includes all file types.

When moving duplicates, file name conflicts are automatically resolved by appending suffixes.

## Limitations

Symbolic links are not specially handled.

Duplicate detection is based strictly on content, not metadata.
