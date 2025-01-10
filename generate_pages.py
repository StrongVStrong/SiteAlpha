import csv
import os
import re
import json

# Set up a folder for the output
output_folder = 'dokkanpages/generated_pages'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

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
    filename = f"{character['Name']}-{character['Subname']}".replace(" ", "_").replace(":", "").replace("/", "_")
    # Use regex to remove any special characters that are not valid in filenames
    filename = re.sub(r'[^\w\s-]', '', filename)  # Remove special characters
    return filename

# Function to generate the JavaScript file with all character data
def generate_js_file(data):
    # Prepare a list to hold the character data objects
    characters_data = []

    for character in data:
        character_data = {
            "name": character['Name'],
            "subname": character['Subname'],
            "stats": {
                "HP_55": character['HP 55%'],
                "HP_100": character['HP 100%'],
                "ATK_55": character['ATK 55%'],
                "ATK_100": character['ATK 100%'],
                "DEF_55": character['DEF 55%'],
                "DEF_100": character['DEF 100%']
            },
            "leaderSkill": character['Leader Skill'],
            "passiveSkill": {
                "name": character['Passive Name'],
                "effect": character['Passive Skill']
            },
            "activeSkill": {
                "name": character['Active Name'],
                "effect": character['Active Skill']
            },
            "superAttack12Ki": {
                "name": character['Super Attack (12 Ki) Name'],
                "effect": character['Super Attack (12 Ki) Effect']
            },
            "ultraSuperAttack18Ki": {
                "name": character['Ultra Super Attack (18 Ki) Name'],
                "effect": character['Ultra Super Attack (18 Ki) Effect']
            },
            "links": character['Links'],
            "categories": character['Categories'],
            "transformationCondition": character['Transformation Condition'],
            "releaseDate": character['Release Date'],
            "kiMultiplier": character['Ki Multiplier'],
            "highestDmgMultiplier": character['Highest DMG Multiplier'],
            "lr12KiDmgMultiplier": character['LR 12 Ki DMG Multiplier']
        }
        characters_data.append(character_data)

    # Convert the data to JSON format
    data_json = json.dumps(characters_data, indent=4)

    # Write the data into the data.js file
    with open(f"{output_folder}/data.js", 'w', encoding='utf-8') as js_file:
        js_file.write(f"const characterData = {data_json};\n")
        js_file.write("export default characterData;")

# Read the data from your CSV file inside the dokkan_data folder
data = read_data('dokkanpages/final_data.csv')  # Path to the CSV file

# Generate the JavaScript file
generate_js_file(data)

print("data.js file generated successfully in 'dokkanpages/generated_pages' folder.")
