import os
from jinja2 import Environment, FileSystemLoader

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(r'C:\Users\Megas\Documents\GitHub\SiteAlpha'))  # Adjust this to your template folder path
template = env.get_template('dokkanpages.html')

# Get all HTML file names from the generated_pages folder
directory = 'generated_pages'  # Folder where your character HTML files are stored
characters = [f.replace('.html', '') for f in os.listdir(directory) if f.endswith('.html')]

# Modify characters list for display name: Replace first '-' with ':'
modified_characters = [character.replace('-', ' : ', 1) for character in characters]

# Render the template with the modified display names
output = template.render(characters=zip(modified_characters, characters))

# Write the output to a file (e.g., dokkanpages.html)
with open('dokkanpages.html', 'w') as f:  # Adjust the output path as needed
    f.write(output)

print("Home page with character links generated successfully.")
