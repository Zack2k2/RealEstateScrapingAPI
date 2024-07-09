import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the webpage content
url = 'https://www.zameen.com/Property/emaar_crescent_bay_emaar_reef_towers_2_bed_brand_new_apartment_for_sale_in_emaar_reef_tower-49842390-10720-1.html'  # Replace with your target URL

response = requests.get(url)
webpage_content = response.text

# Step 2: Parse the HTML content with Beautiful Soup
soup = BeautifulSoup(webpage_content, 'html.parser')

# Step 3: Locate the <div><h3>Amenities</h3> tag
amenities_div = None
for div in soup.find_all('div'):
    h3 = div.find('h3')
    if h3 and h3.text == 'Amenities':
        amenities_div = div
        break

# Step 4: Extract the inner HTML
if amenities_div:
    inner_html = str(amenities_div)
    soup2 = BeautifulSoup(inner_html,'html.parser').find_all('li')

    for v in soup2:
        print(v.text)
else:
    print("No <div><h3>Amenities</h3> section found.")

