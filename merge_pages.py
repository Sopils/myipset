import os
import json
import requests
from bs4 import BeautifulSoup

# Function to extract text from a webpage
def extract_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

# Load configuration from config.json
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

# Ensure output directory exists
os.makedirs('output', exist_ok=True)

# Process each entry in the config
for entry in config:
    output_file = entry['output_file']
    urls = entry['urls']

    combined_text = ""
    for url in urls:
        combined_text += extract_text(url) + "\n"

    # Save the combined text to the specified output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(combined_text)
