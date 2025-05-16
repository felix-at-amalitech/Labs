# Disk Usage Tree

A Python command-line tool that displays disk usage statistics in a structured, tree-like format, similar to the Unix `du` command, but more visual and flexible.

## Features

- Recursively analyzes directories and files
- Sorts by size, name, or modification time
- Supports human-readable file sizes
- Filters by minimum file size (in MB)
- Limits tree depth to a specified level
- Gracefully handles permission and access errors

## Requirements

- Python 3.6+

## Usage

python disk_usage_tree.py [path] [options]

## Positional Argument

path --> Directory to analyze (default: current directory)

## Options

|Option | Description |
|--------|--------------|
|--sort|Sort by size, name, or mtime (default: size)|
|--reverse|Reverse the sort order|
|--min-size|Minimum size (in MB) for files/directories to be displayed|
|--max-depth|Limit recursion depth (-1 for no limit)|

