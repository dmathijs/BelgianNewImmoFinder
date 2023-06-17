# GLOBAL CONFIG
QUERY_URL = "https://www.immoweb.be/nl/map/huis/te-koop?countries=BE&geoSearchAreas=iimuHuaiSmj@lfAiz@bbA}YgDwcAecBccAm`Egn@gnAkNejB_[}dB{`A_fC{Bi_DhSigAvb@cYz`ArUtQdRjkAlwCp[frCjtD|sN&page=1&orderBy=relevance" # this can be a url generated from a drawed area
MAX_PRICE = 450000

# IMPORTS
import requests
import html
import json
import webbrowser
from bs4 import BeautifulSoup

# SCRIPT
response = requests.get(QUERY_URL)

# Create a BeautifulSoup object from the response content
soup = BeautifulSoup(response.content, "html.parser")

map_container = soup.find('iw-search-map-container')

results_encoded = map_container[':results']
results_decoded = html.unescape(results_encoded)

json_object = json.loads(results_decoded)

new_houses = list(filter(lambda x: x["flags"]["main"] == 'new', json_object))

for i in range(len(new_houses)):
    current_house = new_houses[i]
    
    if(current_house["price"]["mainValue"] > MAX_PRICE):
        continue
    
    webbrowser.open_new_tab(f'https://www.immoweb.be/nl/zoekertje/huis/te-koop/{current_house["property"]["location"]["locality"]}/{current_house["property"]["location"]["postalCode"]}/{current_house["id"]}')
