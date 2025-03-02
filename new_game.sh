#!/bin/bash

# Check if the correct number of arguments is provided
if [ $# -ne 1 ]; then
  echo "Usage: $0 <project-name>"
  exit 1
fi

# Get the new directory name from the argument
new_directory="$1"

# Create the new directory and its parent directories if they don't exist
mkdir -p "$new_directory"

# Copy the contents of the template folder into the new directory
cp -R ./template/* "$new_directory"

# Remove .git and __pycache__ folders if they exist
rm -rf "$new_directory/.git" "$new_directory/.gitignore"
find "$new_directory" -type d -name "__pycache__" -exec rm -rf {} +

# Run render.py to generate the templated files
python ./file-templates/render.py "$new_directory"

# Extract the processed project name (same logic as render.py)
project_words=$(echo "$new_directory" | grep -oE '[a-zA-Z]+')
processed_name=""
for word in $project_words; do
    processed_name+=$(echo "$word" | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2))}')
done
processed_name_lower=$(echo "$processed_name" | awk '{print tolower($0)}')

# Move generated files into the new directory
mv "./file-templates/${processed_name_lower}.py" "$new_directory/core/display/${processed_name_lower}.py"
rm "$new_directory/core/display/blank.py"
mv "./file-templates/starter.py" "$new_directory/core/game/starter.py"
cp "Pipfile" "$new_directory"
mv "$new_directory" "../$new_directory"

echo "Project '$new_directory' successfully set up!"

echo "Press any key to continue..."
read -n 1 -s
