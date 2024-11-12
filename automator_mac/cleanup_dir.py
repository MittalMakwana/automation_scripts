#!/usr/bin/env python3
import os
import argparse
import fnmatch

DEFAULT_PATTERN = ["._*", ".DS_Store"]

def find_files(directory, patterns):
    for root, dirs, files in os.walk(directory):
        for pattern in patterns:
            for filename in fnmatch.filter(files, pattern):
                yield os.path.join(root, filename)

def delete_files(files, dry_run, interactive, verbose):
    for file in files:
        if interactive:
            response = input(f"Do you want to delete {file}? [y/N]: ")
            if response.lower() != 'y':
                continue
        if verbose or dry_run:
            print(f"Deleting file: {file}")
        if not dry_run:
            os.remove(file)

def delete_empty_dirs(directory, dry_run, interactive, verbose):
    for root, dirs, files in os.walk(directory, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            if not os.listdir(dir_path):
                if interactive:
                    response = input(f"Do you want to delete empty directory {dir_path}? [y/N]: ")
                    if response.lower() != 'y':
                        continue
                if verbose or dry_run:
                    print(f"Deleting empty directory: {dir_path}")
                if not dry_run:
                    os.rmdir(dir_path)

def main():
    parser = argparse.ArgumentParser(description="Cleanup directory by deleting specified file types and empty directories.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("-i", "--interactive", action="store_true", help="Enable interactive mode")
    parser.add_argument("-d", "--dry-run", action="store_true", help="Perform a dry run without deleting anything")
    parser.add_argument("-p", "--patterns", nargs="+", default=DEFAULT_PATTERN, help="File patterns to delete")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to clean up")

    args = parser.parse_args()

    files_to_delete = list(find_files(args.directory, args.patterns))
    delete_files(files_to_delete, args.dry_run, args.interactive, args.verbose)
    delete_empty_dirs(args.directory, args.dry_run, args.interactive, args.verbose)

if __name__ == "__main__":
    main()
