import os
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(r'C:\Users\Megas\Documents\GitHub\SiteAlpha'))  # Adjust this to your template folder path
template = env.get_template('dokkanpages.html')

# Get all HTML file names from the generated_pages folder
directory = 'generated_pages'  # Folder where your character HTML files are stored
characters = []

# Loop through each HTML file in the generated_pages directory
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        # Extract the display name from the <h1> tag inside the HTML
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            h1_tag = soup.find('h1')
            if h1_tag:
                display_name = h1_tag.text.strip()  # Get text inside <h1> and clean it
                characters.append((display_name, filename.replace('.html', '')))  # Save display_name and filename without extension

# Render the template with the list of character display names and filenames
output = template.render(characters=characters)

# Write the output to a file (e.g., dokkanpages.html)
with open('dokkanpages.html', 'w', encoding='utf-8') as f:
    f.write(output)

print("Home page with character links generated successfully.")
