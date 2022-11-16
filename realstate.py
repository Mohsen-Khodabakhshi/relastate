from utils.crawler import ChromeCrawler

import time

from realstate.xpaths import real_state_xpaths
from realstate.processor import processor, collect

from pprint import pprint

import json


print("Loading...")

my_driver = ChromeCrawler(debug=True)


with open("suburbs.json", 'r', encoding='utf-8') as f:
    suburbs = json.load(f)


for suburb in suburbs:
    try:
        suburb_name = str(suburb['suburb_name']).lower()
        suburb_name = suburb_name.replace("'", "-")

        state = str(suburb['state']).lower()

        postcode = str(suburb['postcode']).lower()

        print("Crawling...")
        print(f"state: {state} suburb: {suburb_name} postcode: {postcode}")

        my_driver.selenium_driver.get(f"https://www.realestate.com.au/{state}/{suburb_name}-{postcode}/")

        time.sleep(2)

        buy_houses = my_driver.get_by_xpath(real_state_xpaths.get("houses"))
        buy_houses = processor(buy_houses)

        my_driver.selenium_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)

        try:

            rent_button = my_driver.get_by_xpath(real_state_xpaths.get("rent_button"))
            rent_button[1].click()

        except:
            rent_button = my_driver.get_by_xpath(real_state_xpaths.get("rent_button2"))
            rent_button[1].click()

        rent_houses = my_driver.get_by_xpath(real_state_xpaths.get("houses"))
        rent_houses = processor(rent_houses)

        collects = collect(buy_houses, rent_houses)

        for c in collects:
            c["suburb_id"] = suburb.get("suburb_id", "")
            my_driver.save_to_csv(c)
        
        print("")

    except:
        continue
