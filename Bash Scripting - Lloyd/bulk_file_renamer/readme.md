# Bulk File Renamer

This program allows you to rename files using prefixes, suffixes, counters, dates, and custom naming patterns.

## Features

- Add prefixes or suffixes to filenames
- Insert date with customizable format
- Include auto-incrementing counters
- Use custom filename patterns ({prefix}, {name}, {suffix}, {counter}, {date})
- Filter by file extension
- Preview changes before applying them

### Requirements

Python 3.6+

### Usage

```code
python renamer.py <directory> [options]
```

### Positional Argument

_directory_: Path to the directory containing the files to rename

### Optional Arguments

| Option    |Description                                                                  |
|-----------|-----------------------------------------------------------------------------|
| `--prefix`       | Add a prefix to filenames                                                   |
| `--suffix`       | Add a suffix to filenames                                                   |
| `--counter`      | Include a counter in filenames                                              |
| `--counter-start`| Starting number for counter (default: 1)                                   |
| `--counter-step` | Step increment for counter (default: 1)                                     |
| `--date`         | Include current date in filenames                                           |
| `--date-format`  | Format for date (default: `%Y-%m-%d`)                                       |
| `--pattern`      | Custom naming pattern using `{prefix}`, `{name}`, `{suffix}`, `{counter}`, `{date}` |
| `--extension`    | Filter files by extension (e.g., `.txt`)                |
| `--preview`      | Preview the renaming without applying change              |

### Notes

- Files that would cause a name conflict are skipped with a warning.
- Extensions are preserved unless modified in the custom pattern.
