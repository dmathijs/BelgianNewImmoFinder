# GLOBAL CONFIG
QUERY_URL = "https://www.zimmo.be/nl/zoeken/?search=eyJmaWx0ZXIiOnsic3RhdHVzIjp7ImluIjpbIkZPUl9TQUxFIiwiVEFLRV9PVkVSIl19LCJwb2x5Z29uIjp7ImluIjpbeyJwYXRoIjoicXdtdUhzeGxTP2JqQVV6S19Bdkl3WGZ9QHdDdElrQnBGcUxwVmFDP29hQHtLYUVrRGNFbUV3Q2tEZWJAc2VAbUZxR3VBZUJhQ2tEVWFAdVhzc0BtW2VuQHlJaVJhQW1FY0dfa0BnUXNiQXdac3RAd0djT2FBaUNpQGVCYUFtRWtAbUVpQHVIX1ZrX0FrQGtEYUNxVnlJd2RBbUZfa0A%2FYUB5YEBzc0BjYEBxc0BVY0FpQHNHP21UaEBtRWRNdWNBVGVCbEZ9S3ZBZ0N2XnFkQHpiQF9cXHRBY0FgQ2NBYEVlQWJgQD92QWRBfkBiQWxGYk92Q3ZKZGJAZm5AdEFoQ2pAZEJqQnBHbERmUWBFeFk%2FfltVbkZhRXh2QHZafnlAfGhAaGBAakJmQ3RBdEhgQW5GVGRCUmZCVGhDP2RuQGlAakRqRGBpQX5VYnxAZF52dUBgRXhKbER0SXZDdklgRWBOYEN0SXRBckd4XnJ0QGBDbkYifV19LCJwcmljZSI6eyJ1bmtub3duIjp0cnVlLCJyYW5nZSI6eyJtYXgiOjUwMDAwMH19LCJjYXRlZ29yeSI6eyJpbiI6WyJIT1VTRSJdfX19#map"
WINDOW_WIDTH = 1920;
WINDOW_HEIGHT = 1080;

# IMPORTS
import requests
import json
import re
import asyncio
import webbrowser
import datetime
from pyppeteer import launch

# SCRIPT
async def main():
    browser = await launch(headless = False, args = ['--start-maximized', '-size={},{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT)])
    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    await page.goto(QUERY_URL, {'waitUntil' : 'domcontentloaded'})
    data = await page.evaluate('''() => {document.querySelector('*').outerHTML}''');
    content = await page.content();
    
    result = re.search(r"properties: ([.\n\S\s]+?),\n.*?save_search", content)

    json_object = json.loads(result.group(1))
    
    new_houses = list(filter(lambda x: datetime.datetime.fromtimestamp(float(x['toegevoegd'])) > datetime.datetime.now() - datetime.timedelta(days=2), json_object))

    for i in range(len(new_houses)):
        current_house = new_houses[i]
		
        webbrowser.open_new_tab(f'https://www.zimmo.be{current_house["pand_url"]}')

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())


# Create a BeautifulSoup object from the response content



