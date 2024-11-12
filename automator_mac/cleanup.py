#!/usr/bin/env python3

import argparse
import os
import fnmatch

def find_files(directory, patterns):
    """Yield file paths matching the given patterns."""
    for root, dirs, files in os.walk(directory):
        for pattern in patterns:
            for filename in fnmatch.filter(files, pattern):
                yield os.path.join(root, filename)

def delete_files(file_paths):
    """Delete the files at the given paths."""
    for path in file_paths:
        try:
            os.remove(path)
            print(f"Deleted {path}")
        except PermissionError:
            print(f"Error: Permission denied for {path}. Skipping.")
        except FileNotFoundError:
            print(f"Error: File {path} not found. Skipping.")
        except OSError:
            print(f"Error: Failed to delete {path}. Skipping.")

def flatenize(directory):
    """Flatten the directory structure by moving all files to the root."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            old_path = os.path.join(root, file)
            new_path = os.path.join(directory, file)
            try:
                os.rename(old_path, new_path)
                print(f"Moved {old_path} to {new_path}")
            except FileExistsError:
                print(f"Error: File {new_path} already exists. Skipping.")
            except PermissionError:
                print(f"Error: Permission denied for {old_path}. Skipping.")

def cleanup(directory, file_types, flatten, dry_run=False):
    """Cleanup files of specified types and empty directories."""
    patterns = {
        'mac': ['._*', '.DS_Store'],
        'temp': ['*.tmp', '*.temp'],
        'log': ['*.log'],
        # Add more predefined patterns here
    }

    # Gather patterns to use
    selected_patterns = []
    for file_type in file_types:
        if file_type in patterns:
            selected_patterns.extend(patterns[file_type])
        else:
            print(f"Warning: No predefined patterns for '{file_type}'. Ignoring.")
    
    # Find and delete files
    files_to_delete = find_files(directory, selected_patterns)
    if dry_run:
        for path in files_to_delete:
            print(f"Would delete {path}")
    else:
        delete_files(files_to_delete)

    # Find and remove empty directories
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            dirpath = os.path.join(root, dir)
            if not os.listdir(dirpath):  # Check if directory is empty
                if dry_run:
                    print(f"DRY RUN: Removed empty directory {dirpath}")
                else:
                    os.rmdir(dirpath)
                    print(f"Removed empty directory {dirpath}")
    
    # Flatten the directory structure
    if flatten:
        flatenize(directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleanup directories by removing specified types of files.")
    parser.add_argument("dir", nargs="?", default=".", help="Directory to cleanup. Defaults to current directory.")
    parser.add_argument("-t", "--types", nargs="+", default='mac',required=True, help="Types of files to delete (e.g., mac, temp, log)")
    parser.add_argument("--dry-run", action="store_true", help="Print files to delete without deleting them.")
    parser.add_argument("--flatten", action="store_true", default=False, help="Flatten the directory structure.")
    
    args = parser.parse_args()

    cleanup(args.dir, args.types, args.flatten ,args.dry_run)

