import requests

from bs4 import BeautifulSoup

import json

from pprint import pprint

import csv


def save_to_csv(data: dict):
    with open('domain_history.csv', 'a') as f:
        w = csv.DictWriter(f, data.keys())
        w.writerow(data)


with open("all_suburbs.json", 'r', encoding='utf-8') as f:
        suburbs = json.load(f)

for suburb in suburbs:
    try:
        suburb_name = str(suburb['suburb_name']).lower()
        suburb_name = suburb_name.replace("'", "-")
        suburb_name = suburb_name.replace(" ", "-")

        state = str(suburb['state']).lower()

        postcode = str(suburb['postcode']).lower()

        url = f"https://www.domain.com.au/suburb-profile/{suburb_name}-{state}-{postcode}"

        headers = {
            'authority': 'www.domain.com.au',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/83.0.4103.61 Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9'
        }

        req = requests.get(url, headers=headers).content

        soup = BeautifulSoup(req, 'html.parser')

        data = json.loads(
            soup.find("script", id="__NEXT_DATA__").text
        )

        houses = data['props']['pageProps']['details']['marketInsights']

        for house in houses:

            sales_growth_list = house.get("salesGrowthList", [])

            for sale in sales_growth_list:

                ag = sale.get("annualGrowth", "")
                if ag and ag != "":
                    ag = ag * 100

                data = {
                    "type": house.get("propertyType", ""),
                    "bedrooms": house.get("beds", ""),
                    "suburb_id": suburb["suburb_id"],
                    "year": sale.get("year", ""),
                    "median_sold_price": sale.get("medianSoldPrice", ""),
                    "annual_growth": ag,
                }
                save_to_csv(data)

        with open("domain_history_success.txt", 'a', encoding='utf-8') as f2:
            f2.write(f"state: {state} suburb: {suburb_name} postcode: {postcode}\n")
            f2.close()

    except:
        suburb_name = str(suburb['suburb_name']).lower()
        state = str(suburb['state']).lower()
        postcode = str(suburb['postcode']).lower()

        with open("domain_history_errors.txt", 'a', encoding='utf-8') as f2:
            f2.write(f"state: {state} suburb: {suburb_name} postcode: {postcode}\n")
            f2.close()

        continue
