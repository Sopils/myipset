import os
import json
import requests
from bs4 import BeautifulSoup

# Function to extract text from a webpage
def extract_text(url):
    try:
        response = requests.get(url)
        # Check if the response was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text(), None
        else:
            # Return an error message with the URL and status code
            return None, f"Error {response.status_code} at {url}"
    except requests.exceptions.RequestException as e:
        # Handle other request exceptions
        return None, f"Request exception at {url}: {e}"

# Load configuration from config.json
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

# Ensure output directory exists
os.makedirs('output', exist_ok=True)

# Track error URLs
error_urls = []

# Process each entry in the config
for entry in config:
    output_file = entry['output_file']
    urls = entry['urls']

    combined_text = ""
    for url in urls:
        text, error = extract_text(url)
        if error:
            error_urls.append(error)  # Add error to the list
        else:
            combined_text += text + "\n"

    # Save the combined text to the specified output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(combined_text)

# Write all error URLs to a log file
if error_urls:
    with open('output/errorurls.log', 'w', encoding='utf-8') as error_file:
        error_file.write("\n".join(error_urls))
