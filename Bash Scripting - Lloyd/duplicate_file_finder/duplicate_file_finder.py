import os
import hashlib
import shutil
from collections import defaultdict

def calculate_md5(file_path, block_size=65536):
    """Calculate MD5 hash of a file."""
    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                md5.update(block)
        return md5.hexdigest()
    except (IOError, PermissionError) as e:
        print(f"Error reading {file_path}: {e}")
        return None

def find_duplicates(directory):
    """Find duplicate files based on size and MD5 hash."""
    # Dictionary to store size -> list of files
    size_dict = defaultdict(list)
    # Dictionary to store hash -> list of files
    hash_dict = defaultdict(list)

    print(f"Scanning directory: {directory}")
    
    # Step 1: Group files by size
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                file_size = os.path.getsize(file_path)
                size_dict[file_size].append(file_path)
            except (OSError, PermissionError) as e:
                print(f"Error accessing {file_path}: {e}")

    # Step 2: Calculate hashes for files with same size
    for file_size, file_list in size_dict.items():
        if len(file_list) > 1:  # Only process if multiple files have same size
            for file_path in file_list:
                file_hash = calculate_md5(file_path)
                if file_hash:
                    hash_dict[file_hash].append(file_path)

    # Step 3: Collect duplicates (files with same hash)
    duplicates = {hash_val: files for hash_val, files in hash_dict.items() if len(files) > 1}
    return duplicates

def display_duplicates(duplicates):
    """Display duplicate files and return total size of duplicates."""
    if not duplicates:
        print("No duplicate files found.")
        return 0

    total_size = 0
    print("\nDuplicate files found:")
    for hash_val, file_list in duplicates.items():
        print(f"\nHash: {hash_val}")
        for i, file_path in enumerate(file_list, 1):
            file_size = os.path.getsize(file_path)
            total_size += file_size
            print(f"  {i}. {file_path} ({file_size / 1024:.2f} KB)")
    print(f"\nTotal size of duplicates: {total_size / 1024 / 1024:.2f} MB")
    return total_size

def handle_duplicates(duplicates, directory):
    """Provide options to delete or move duplicate files."""
    if not duplicates:
        return

    while True:
        print("\nOptions:")
        print("1. Delete duplicates (keep first file)")
        print("2. Move duplicates to a folder")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()

        if choice == '1':
            for hash_val, file_list in duplicates.items():
                # Keep the first file, delete the rest
                for file_path in file_list[1:]:
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except (OSError, PermissionError) as e:
                        print(f"Error deleting {file_path}: {e}")
            print("Deletion complete.")
            break

        elif choice == '2':
            # Create a folder for duplicates
            dup_folder = os.path.join(directory, "Duplicate_Files")
            os.makedirs(dup_folder, exist_ok=True)

            for hash_val, file_list in duplicates.items():
                # Keep the first file, move the rest
                for file_path in file_list[1:]:
                    try:
                        dest_path = os.path.join(dup_folder, os.path.basename(file_path))
                        # Handle filename conflicts
                        base, ext = os.path.splitext(dest_path)
                        counter = 1
                        while os.path.exists(dest_path):
                            dest_path = f"{base}_{counter}{ext}"
                            counter += 1
                        shutil.move(file_path, dest_path)
                        print(f"Moved: {file_path} -> {dest_path}")
                    except (OSError, PermissionError) as e:
                        print(f"Error moving {file_path}: {e}")
            print(f"Moved duplicates to: {dup_folder}")
            break

        elif choice == '3':
            print("Exiting without changes.")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

def main():
    """Main function to run the duplicate file finder."""
    directory = input("Enter the directory path to scan: ").strip()
    
    if not os.path.isdir(directory):
        print("Invalid directory path.")
        return

    duplicates = find_duplicates(directory)
    total_size = display_duplicates(duplicates)
    if total_size > 0:
        handle_duplicates(duplicates, directory)

if __name__ == "__main__":
    main()