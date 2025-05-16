import os
import argparse
from datetime import datetime
import re

def parse_arguments():
    """Parse command-line arguments for the file renaming tool."""
    parser = argparse.ArgumentParser(description="Batch rename files using patterns")
    parser.add_argument("directory", help="Directory containing files to rename")
    parser.add_argument("--prefix", default="", help="Prefix to add to filenames")
    parser.add_argument("--suffix", default="", help="Suffix to add to filenames")
    parser.add_argument("--counter", action="store_true", help="Include a counter in filenames")
    parser.add_argument("--counter-start", type=int, default=1, help="Starting number for counter")
    parser.add_argument("--counter-step", type=int, default=1, help="Step increment for counter")
    parser.add_argument("--date", action="store_true", help="Include current date in filenames")
    parser.add_argument("--date-format", default="%Y-%m-%d", help="Date format (e.g., %%Y-%%m-%%d)")
    parser.add_argument("--pattern", help="Custom naming pattern (e.g., '{prefix}_{name}_{counter}')")
    parser.add_argument("--extension", help="Filter files by extension (e.g., .txt)")
    parser.add_argument("--preview", action="store_true", help="Preview changes without renaming")
    return parser.parse_args()

def get_files(directory, extension=None):
    """Get list of files in directory, optionally filtered by extension."""
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if extension:
            extension = extension.lstrip(".").lower()
            files = [f for f in files if f.lower().endswith(f".{extension}")]
        return sorted(files)
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied for directory '{directory}'.")
        return []

def generate_new_filename(args, original_name, counter):
    """Generate new filename based on provided rules or pattern."""
    # Extract base name and extension
    base_name, ext = os.path.splitext(original_name)

    # If a custom pattern is provided, use it
    if args.pattern:
        new_name = args.pattern
        new_name = new_name.replace("{prefix}", args.prefix)
        new_name = new_name.replace("{suffix}", args.suffix)
        new_name = new_name.replace("{name}", base_name)
        new_name = new_name.replace("{counter}", f"{counter:04d}")
        if args.date:
            new_name = new_name.replace("{date}", datetime.now().strftime(args.date_format))
        return new_name + ext

    # Otherwise, build name using prefix, suffix, counter, and date
    components = []
    if args.prefix:
        components.append(args.prefix)
    components.append(base_name)
    if args.date:
        components.append(datetime.now().strftime(args.date_format))
    if args.counter:
        components.append(f"{counter:04d}")
    if args.suffix:
        components.append(args.suffix)

    return "_".join(components) + ext

def rename_files(args):
    """Rename files in the directory based on specified rules."""
    files = get_files(args.directory, args.extension)
    if not files:
        print("No files found to rename.")
        return

    # Generate new filenames and check for conflicts
    new_names = {}
    counter = args.counter_start
    for original_name in files:
        new_name = generate_new_filename(args, original_name, counter)
        new_path = os.path.join(args.directory, new_name)
        if new_name in new_names.values() or os.path.exists(new_path):
            print(f"Warning: Name conflict for '{new_name}'. Skipping.")
            continue
        new_names[original_name] = new_name
        if args.counter:
            counter += args.counter_step

    # Preview or execute renaming
    if args.preview:
        print("\nPreview of changes:")
        for old, new in new_names.items():
            print(f"{old} -> {new}")
    else:
        for old, new in new_names.items():
            try:
                os.rename(
                    os.path.join(args.directory, old),
                    os.path.join(args.directory, new)
                )
                print(f"Renamed: {old} -> {new}")
            except OSError as e:
                print(f"Error renaming '{old}' to '{new}': {e}")

def main():
    args = parse_arguments()
    rename_files(args)

if __name__ == "__main__":
    main()