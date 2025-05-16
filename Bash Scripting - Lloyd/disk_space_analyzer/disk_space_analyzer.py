import os
import argparse
from typing import List, Tuple
from pathlib import Path

class DiskUsageTree:
    def __init__(self, path: str, sort_by: str = 'size', reverse: bool = True, 
                 min_size_mb: float = 0, max_depth: int = -1):
        self.path = os.path.abspath(path)
        self.sort_by = sort_by  # 'size', 'name', or 'mtime'
        self.reverse = reverse
        self.min_size_mb = min_size_mb
        self.max_depth = max_depth
        self.total_size = 0

    def human_readable_size(self, size: int) -> str:
        """Convert bytes to human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size = 1024
        return f"{size:.2f} PB"

    def get_file_info(self, path: str) -> Tuple[int, float]:
        """Get size and modification time of a file or directory."""
        try:
            stat = os.stat(path)
            if os.path.isdir(path):
                size = 0
                for root, _, files in os.walk(path):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            size += os.path.getsize(file_path)
                        except (OSError, PermissionError):
                            continue
            else:
                size = stat.st_size
            return size, stat.st_mtime
        except (OSError, PermissionError):
            return 0, 0

    def collect_tree(self, path: str, depth: int = 0) -> List[dict]:
        """Recursively collect directory and file information."""
        if self.max_depth >= 0 and depth > self.max_depth:
            return []

        items = []
        try:
            for entry in os.scandir(path):
                try:
                    size, mtime = self.get_file_info(entry.path)
                    if size / (1024 * 1024) < self.min_size_mb:
                        continue
                    items.append({
                        'name': entry.name,
                        'path': entry.path,
                        'size': size,
                        'mtime': mtime,
                        'is_dir': entry.is_dir(),
                        'children': [] if entry.is_dir() else None
                    })
                except (OSError, PermissionError):
                    continue
        except (OSError, PermissionError):
            return []

        for item in items:
            if item['is_dir']:
                item['children'] = self.collect_tree(item['path'], depth + 1)
                item['size'] = sum(child['size'] for child in item['children'])

        # Sort items
        if self.sort_by == 'size':
            items.sort(key=lambda x: x['size'], reverse=self.reverse)
        elif self.sort_by == 'name':
            items.sort(key=lambda x: x['name'].lower(), reverse=self.reverse)
        elif self.sort_by == 'mtime':
            items.sort(key=lambda x: x['mtime'], reverse=self.reverse)

        return items

    def print_tree(self, items: List[dict], prefix: str = '', depth: int = 0):
        """Print the tree structure."""
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            connector = '└── ' if is_last else '├── '
            print(f"{prefix}{connector}{item['name']} ({self.human_readable_size(item['size'])})")
            if item['children']:
                new_prefix = prefix + ('    ' if is_last else '│   ')
                self.print_tree(item['children'], new_prefix, depth + 1)

    def run(self):
        """Run the disk usage analysis."""
        if not os.path.exists(self.path):
            print(f"Error: Path '{self.path}' does not exist")
            return

        print(f"Disk usage for: {self.path}")
        items = self.collect_tree(self.path)
        self.total_size = sum(item['size'] for item in items)
        print(f"Total size: {self.human_readable_size(self.total_size)}")
        print("\nDirectory tree:")
        self.print_tree(items)

def main():
    parser = argparse.ArgumentParser(description="Display disk usage in a tree structure")
    parser.add_argument('path', default='.', nargs='?', help="Directory to analyze (default: current)")
    parser.add_argument('--sort', choices=['size', 'name', 'mtime'], default='size',
                        help="Sort by: size, name, or modification time")
    parser.add_argument('--reverse', action='store_true', help="Reverse sort order")
    parser.add_argument('--min-size', type=float, default=0,
                        help="Minimum size in MB to display")
    parser.add_argument('--max-depth', type=int, default=-1,
                        help="Maximum depth to display (-1 for unlimited)")

    args = parser.parse_args()
    
    tree = DiskUsageTree(
        path=args.path,
        sort_by=args.sort,
        reverse=args.reverse,
        min_size_mb=args.min_size,
        max_depth=args.max_depth
    )
    tree.run()

if __name__ == "__main__":
    main()