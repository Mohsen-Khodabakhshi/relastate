from datetime import datetime


def processor(inputs: list):
    all_data = []
    
    for i in inputs:
        data = {}

        text = i.text.split(" ")

        data["bedrooms"] = text[0]
        
        if text[2][0:5] == "house":
            data["type"] = "house"
        else:
            data["type"] = "unit"

        data["price"] = text[2][text[2].index("\n") + len("\n"):]
        if data["price"] == "Unavailable":
            data["price"] = ""

        all_data.append(data)

    return all_data

def collect(buys: list, rents: list):
    final = []

    for i, buy in enumerate(buys):
        for j, rent in enumerate(rents):
            if buy.get("bedrooms", None) == rent.get("bedrooms", None):
                if buy.get("type", None) == rent.get("type", None):
                    data = {**buy}
                              
                    data["median_solid_price"] = buy.get("price", None)
                    data["median_rental_price"] = rent.get("price", None)
                    data["date_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    data.pop("price", None)  

                    final.append(data)

    return final
