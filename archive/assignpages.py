import re
import urllib.parse

# Open the HTML file to read
with open('dokkanpages.html', 'r') as file:
    html_content = file.read()

# Function to generate URL-safe format for the subname (before the colon)
def generate_url(subname):
    # URL encode the subname (this will be the part before the colon)
    url_safe_name = urllib.parse.quote(subname)
    return f"characters.html?character={url_safe_name}"

# Function to process each link and replace the old links
def process_links(html_content):
    # Find all links in the format "Character-Ability.html" and capture the character name and ability
    pattern = r'href="generated_pages/([^"]+)\.html">([^<]+)</a>'
    matches = re.findall(pattern, html_content)

    updated_links = []

    for match in matches:
        link_name = match[0]  # Example: Aeos-Space-Time_Selector
        link_text = match[1]  # Example: Space-Time Selector : Aeos

        # Split the link text into subname (before colon) and character name (after colon)
        subname, character_name = link_text.split(' : ')

        # Generate the new URL with the subname (before the colon)
        new_url = generate_url(subname)
        
        # Generate the updated link with the new URL containing only the subname
        updated_link = f'<a class="hidelink" href="{new_url}">{link_text}</a>'
        updated_links.append(updated_link)

    # Replace the old links with the new updated links in the HTML content
    updated_html = re.sub(pattern, lambda match: updated_links.pop(0), html_content)

    return updated_html

# Process the HTML content and generate the updated links
updated_html_content = process_links(html_content)

# Write the updated HTML content to a new file
with open('updated_dokkanpages.html', 'w') as file:
    file.write(updated_html_content)

print("Links have been successfully updated.")
