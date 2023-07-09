#!/bin/bash

# Check if the correct number of arguments is provided
if [ $# -ne 1 ]; then
  echo "Usage: $0 <new-directory>"
  exit 1
fi

# Get the new directory name from the argument
new_directory="$1"

# Create the new directory and its parent directories if they don't exist
mkdir -p "$new_directory"

# Copy the contents of the current directory to the new directory
cp -R ./template/* "$new_directory"

# Remove the .git folder and .gitignore file from the new directory
rm -rf "$new_directory/.git" "$new_directory/.gitignore"

find "$new_directory" -type d -name "__pycache__" -exec rm -rf {} +
