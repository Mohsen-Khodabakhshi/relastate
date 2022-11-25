import requests

from bs4 import BeautifulSoup

import json

from pprint import pprint

import csv


def save_to_csv(data: dict):
    with open('mag.csv', 'a') as f:
        w = csv.DictWriter(f, data.keys())
        w.writerow(data)

with open("all_suburbs2.json", 'r', encoding='utf-8') as f:
        suburbs = json.load(f)

for suburb in suburbs:

    try:

        suburb_name = str(suburb['suburb_name']).lower()
        suburb_name = suburb_name.replace("'", "-")
        suburb_name = suburb_name.replace(" ", "-")

        state = str(suburb['state']).lower()

        postcode = str(suburb['postcode']).lower()

        headers = {
            'authority': 'www.yourinvestmentpropertymag.com.au',
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

        req = requests.get(f"https://www.yourinvestmentpropertymag.com.au/top-suburbs/{state}/{postcode}-{suburb_name}", headers=headers).content

        soup = BeautifulSoup(req, 'html.parser')

        data = soup.find("div", class_="key-table-reports")

        d = data.find("div", class_="key-table-report").find("table").find("tbody")
        trs = d.findAll("tr")

        data = {
            "house_quarterly": None,
            "house_twelve": None,
            "house_average": None,
            "house_sales": None,
            "unit_quarterly": None,
            "unit_twelve": None,
            "unit_average": None,
            "unit_sales": None,
            "suburb_id": suburb["suburb_id"],
        }

        for tr in trs:
            label = tr.find("td").text

            if label == "Quarterly growth":
                quarterlies = tr.findAll("td", class_="table-value")
                data["house_quarterly"] = quarterlies[0].text[:-2]
                data["unit_quarterly"] = quarterlies[1].text[:-2]

            elif label == "12-month growth":
                twelve = tr.findAll("td", class_="table-value")
                data["house_twelve"] = twelve[0].text[:-2]
                data["unit_twelve"] = twelve[1].text[:-2]


            elif label == "Average annual growth":
                average = tr.findAll("td", class_="table-value")
                data["house_average"] = average[0].text[:-2]
                data["unit_average"] = average[1].text[:-2]


            elif label == "Number of Sales (12m)":
                sales = tr.findAll("td", class_="table-value")
                data["house_sales"] = sales[0].text[:-1]
                data["unit_sales"] = sales[1].text[:-1]

        save_to_csv(data)

    except:
        continue
