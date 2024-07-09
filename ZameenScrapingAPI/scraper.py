import json
import requests as req
import bs4
import json
import requests
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import sys

# Some initial things
base_url = 'https://www.zameen.com/'


#
# get_past_date - takes a relative time reference like `3 hours ago` or `4 months` ago
# and translates that into a date.
# @time_str : string relative time like "3 hours ago", "4 days ago", "1 month" ago 
#
def get_past_date(time_str):
    # Regular expression to parse the input string
    pattern = re.compile(r'(\d+)\s*(seconds?|minutes?|days?|weeks?|hours?|months?|years?)\s*ago')
    match = pattern.match(time_str)
    
    if not match:
        print(time_str)    
        raise ValueError("Input string is not in the correct format")

    # Extract the quantity and unit from the input string
    quantity = int(match.group(1))
    unit = match.group(2).lower()
    
    # Get the current date and time
    now = datetime.now()
    
    if 'day' in unit:
        past_date = now - timedelta(days=quantity)
    elif 'hour' in unit:
        past_date = now - timedelta(hours=quantity)
    elif 'month' in unit:
        past_date = now - relativedelta(months=quantity)
    elif 'year' in unit:
        past_date = now - relativedelta(years=quantity)
    elif 'second' in unit:
        past_date = now - timedelta(seconds=quantity)
    elif 'minute' in unit:
        past_date = now - timedelta(minutes=quantity)
    elif 'week' in unit:
        past_date = now - timedelta(weeks=quantity)
    else:
        raise ValueError("Unknown time unit")
    
    return past_date

#
# getAdsUrlLists - takes a url of ad page and 
# returns all the a href links with Property in it.
# @url : ad page url
#
def getAdsUrlLists(page_url):

    response = req.get(page_url)
    if not response.ok:
        return "{\"Error\":\"Error in response of requests to get HTML{0}\"}".format(__file__)
    
    soup = bs4.BeautifulSoup(response.text,'html.parser')

    properties_list = ['https://www.zameen.com'+a['href'] for a in soup.find_all("a",href=True) if a['href'].startswith('/Property/')] 

    return json.dumps(properties_list)


#
# getAdInfo - takes a property url and returns a JSON string 
# @url : url of the zameen ad
#
def getAdInfo(url):
    response = req.get(url)
    if not response.ok:
        return "{\"Error\":\"Error in response of requests to get HTML{0}\"}".format(__file__)
    webpage_content = response.text

    # Step 2: Parse the HTML content with Beautiful Soup
    soup = bs4.BeautifulSoup(webpage_content, 'html.parser')

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
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
        else:
            print("No JSON data found in the script tag.")
    else:
        print("No matching <script> tag found.")

    #step 5: find the damn time posted
    creation_date_spans = soup.find_all('span', attrs={'aria-label': 'Creation date'})
    #print(creation_date_spans[0].text)
    json_data.update({"ad_creation_date":str(get_past_date(creation_date_spans[0].text))})

    # Step 3: Locate the <div><h3>Amenities</h3> tag
    amenities_list = []
    amenities_div = None
    for div in soup.find_all('div'):
        h3 = div.find('h3')
        if h3 and h3.text == 'Amenities':
            amenities_div = div
            break

    # Step 4: Extract the inner HTML
    if amenities_div:
        inner_html = str(amenities_div)
        soup2 = bs4.BeautifulSoup(inner_html,'html.parser').find_all('li')

        for v in soup2:
            amenities_list.append(v.text)
    else:
        print("No <div><h3>Amenities</h3> section found.")

    agency_info_div = soup.find('div', {'aria-label':'Agency info'}) 
    agency_page = base_url + agency_info_div.find('a').attrs['href']
    json_data.update({"website":agency_page})

    logo_link = agency_info_div.find_all('img',attrs={'aria-label':'Agency logo'})[0].attrs['data-src'] 
    imageSrc = soup.find('div',attrs={'class':'image-gallery-swipe'}).find('img')['src']
    agency_title = agency_info_div.find('div').text
    json_data.update({"imageSrc":imageSrc})
    json_data.update({"logo":logo_link})
    json_data.update({"company":agency_title})
    json_data.update({"amenities":amenities_list});

    
    description_div = soup.find_all('div', attrs={'aria-label':"Property description"})

    json_data.update({"description":description_div[0].text})
    json_data.update({"area_unit":"Sq. M."})
    return json.dumps(json_data)




# transform the json data fetched in to certain format
def transform_data(data_json):
    json_obj = json.loads(data_json)

    correct_format_data = {"id":len(json_obj)}
    correct_format_data.update({"name":json_obj["listing_title"]})
    correct_format_data.update({"center":{"lat":json_obj["latitude"],"lng":json_obj["longitude"]}})
    sq_m_to_sq_ft_const = 10.764
    correct_format_data.update({"lat":json_obj["latitude"], "lng":json_obj["longitude"]})
    correct_format_data.update({"area_from":(json_obj["property_area"]*sq_m_to_sq_ft_const)})
    correct_format_data.update({"prop_type":json_obj["property_type"]})
    correct_format_data.update({"ad_creation_date":json_obj["ad_creation_date"]})
    correct_format_data.update({"area_unit":"Sq. ft."})
    correct_format_data.update({"currency":json_obj["currency_unit"]})
    correct_format_data.update({"logo":json_obj["logo"]})
    correct_format_data.update({"price_from":json_obj["price"]})
    correct_format_data.update({"imageSrc":json_obj["imageSrc"]})
    correct_format_data.update({"website":json_obj["website"]})
    correct_format_data.update({"company":json_obj["company"]})
    correct_format_data.update({"amenities":json_obj["amenities"]})
    correct_format_data.update({"location":json_obj["loc_neighbourhood_name"]+", "+json_obj["loc_city_name"]+", "+json_obj["loc_region_name"].strip(';')})
    correct_format_data.update({"about":json_obj["description"]})

    return json.dumps(correct_format_data)

#
# getUrbanization - gets urbanization data.
# @lat, @long, @radius: meters
#
def getUrbanization(latitude, longitude, radius):
    url_template = "https://www.zameen.com/api/places?latitude={lat}&longitude={lon}&radius={rad}"
    url = url_template.format(lat=latitude, lon=longitude, rad=radius)

    res = req.get(url)

    if not res.ok:
        urban_data = ["Error"]
    else:
        urban_data = res.text

    return urban_data



if __name__ == '__main__':
    print(transform_data(getAdInfo("https://www.zameen.com/Property/dha_defence_dha_phase_8_120_yards_brand_new_bungalow_architect_designed_west_open-50141455-1485-1.html")))
