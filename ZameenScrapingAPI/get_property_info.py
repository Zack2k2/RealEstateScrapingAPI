import requests
from bs4 import BeautifulSoup
import json
import re

# Step 1: Fetch the webpage content
url = 'https://www.zameen.com/Property/emaar_crescent_bay_emaar_coral_towers_emaar_luxury_apartments_for_sale-45888507-10721-1.html'  # Replace with your target URL

def getAdInfo(url):
    response = requests.get(url)
    webpage_content = response.text

    # Step 2: Parse the HTML content with Beautiful Soup
    soup = BeautifulSoup(webpage_content, 'html.parser')

    # Step 3: Locate the <script> tag containing the JSON data
    script_tag = soup.find('script', string=re.compile(r'window\[\'dataLayer\'\]\.push\(\{.*\}\);', re.DOTALL))

    if script_tag:
        # Extract the JavaScript code
        script_content = script_tag.string
        
        # Use regex to extract the JSON part from the JavaScript code
        json_data_match = re.search(r'window\[\'dataLayer\'\]\.push\((\{.*\})\);', script_content, re.DOTALL)
        if json_data_match:
            json_data_str = json_data_match.group(1)
            
            # Step 4: Parse the JSON data
            try:
                json_data = json.loads(json_data_str)
                print(json.dumps(json_data, indent=4))
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
        else:
            print("No JSON data found in the script tag.")
    else:
        print("No matching <script> tag found.")

