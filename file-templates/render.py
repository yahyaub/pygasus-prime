import re, sys
from jinja2 import Environment, FileSystemLoader

# Load Jinja2 environment
env = Environment(loader=FileSystemLoader("./file-templates"))
blank_template = env.get_template("blank_template.py.j2")
starter_template = env.get_template("starter_template.py.j2")

# Read command-line arguments (passed from the Bash script)
project_words = re.findall(r'[a-zA-Z]+', sys.argv[1])
project_name = ''.join(word.capitalize() for word in project_words)

# Default parameters for the constructor
init_params = ["Sample"]

# Render the template
blank_output = blank_template.render(class_display=project_name+"Display",class_layer=project_name+"Layer",class_item=project_name+"Item")
starter_output = starter_template.render(class_name=project_name.lower(),class_display=project_name+"Display")

# Save to a new file
blank_output_file = f"./file-templates/{project_name.lower()}.py"
with open(blank_output_file, "w") as f:
    f.write(blank_output)
print(f"Generated {blank_output_file} successfully!")

starter_output_file = f"./file-templates/starter.py"
with open(starter_output_file, "w") as f:
    f.write(starter_output)
print(f"Generated {starter_output_file} successfully!")
