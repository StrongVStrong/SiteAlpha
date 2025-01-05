import csv
from jinja2 import Environment, FileSystemLoader
import os
import re
print(os.getcwd())  # Print the current working directory to debug

# Set up Jinja2 environment to load the template
env = Environment(loader=FileSystemLoader(r'C:\Users\Megas\Documents\GitHub\SiteAlpha'))
template = env.get_template('template.html')

# Function to read data from the CSV file
def read_data(filename):
    data = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Function to generate unique filenames by combining Name and Subname
def generate_unique_filename(character):
    # Combine Name and Subname to create a unique filename
    filename = f"{character['Name']}-{character['Subname']}".replace(" ", "_").replace(":", "").replace("/", "_")\
    # Use regex to remove any special characters that are not valid in filenames
    filename = re.sub(r'[^\w\s-]', '', filename)  # Remove special characters
    return filename

# Function to generate the HTML pages
def generate_html_pages(data, template):
    # Create a folder to store the generated HTML files (if it doesn't exist)
    output_folder = 'dokkanpages/generated_pages'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for character in data:
        # Generate a unique filename
        filename = generate_unique_filename(character)

        # Render the HTML with the character's data
        html_content = template.render(
            Name=character['Name'],
            Subname=character['Subname'],
            HP_55=character['HP 55%'],
            HP_100=character['HP 100%'],
            ATK_55=character['ATK 55%'],
            ATK_100=character['ATK 100%'],
            DEF_55=character['DEF 55%'],
            DEF_100=character['DEF 100%'],
            Leader_Skill=character['Leader Skill'],
            Passive_Skill=character['Passive Skill'],
            Active_Skill=character['Active Skill'],
            Super_Attack_12_Ki_Name=character['Super Attack (12 Ki) Name'],
            Super_Attack_12_Ki_Effect=character['Super Attack (12 Ki) Effect'],
            Ultra_Super_Attack_18_Ki_Name=character['Ultra Super Attack (18 Ki) Name'],
            Ultra_Super_Attack_18_Ki_Effect=character['Ultra Super Attack (18 Ki) Effect'],
            Links=character['Links'],
            Categories=character['Categories'],
            Transformation_Condition=character['Transformation Condition'],
            Release_Date=character['Release Date'],
            Ki_Multiplier=character['Ki Multiplier'],
            Highest_DMG_Multiplier=character['Highest DMG Multiplier'],
            LR_12_Ki_DMG_Multiplier=character['LR 12 Ki DMG Multiplier']
        )

        # Write the generated HTML to a new file in the generated_pages folder
        with open(f"{output_folder}/{filename}.html", 'w', encoding='utf-8') as output_file:
            output_file.write(html_content)

# Read the data from your CSV file inside the dokkan_data folder
data = read_data('dokkanpages/final_data.csv')  # Path to the CSV file

# Generate the HTML pages
generate_html_pages(data, template)

print("HTML pages generated successfully in 'dokkan_data/generated_pages' folder.")
