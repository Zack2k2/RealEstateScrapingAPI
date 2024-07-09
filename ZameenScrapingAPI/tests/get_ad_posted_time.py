import requests
from bs4 import BeautifulSoup

url = "https://www.zameen.com/Property/emaar_crescent_bay_emaar_reef_towers_2_bed_brand_new_apartment_for_sale_in_emaar_reef_tower-49842390-10720-1.html"  # Replace with your URL
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

creation_date_spans = soup.find_all('span', attrs={'aria-label': 'Creation date'})

for span in creation_date_spans:
    print(span.text)
