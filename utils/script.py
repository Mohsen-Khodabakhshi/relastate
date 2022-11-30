import csv


def domain_history():

    file_name = './domain_history20221124.csv'

    points = []
    result = {}
    final = []

    with open(file_name) as f:
        reader = csv.DictReader(f)

        for r in reader:
            if r.get("year", None) == 2021 or r.get("year", None) == "2021":
                points.append(r)

        f.close()


    for point in points:
        suburb = point.get("suburb_id", None)

        if not result.get(suburb, None):

            ad = [
                {
                    **point
                }
            ]

            result[point.get("suburb_id", None)] = ad

        else:
            result[point.get("suburb_id", None)].append(
                {
                    **point
                }
            )

    for k, v in result.items():
        houses_median_price = []
        houses_growth = []

        units_median_price = []
        units_growth = []

        for d in v:
            type_ = d.get("type", None) 

            if type_ == "House":
                median_price = d.get("median_sold_price", 0)
                annual_growth = d.get("annual_growth", 0.0)

                if median_price and int(median_price) != 0:
                    houses_median_price.append(int(median_price))

                if annual_growth and float(annual_growth) != 0.0:
                    houses_growth.append(float(annual_growth))

            if type_ == "Unit":
                median_price = d.get("median_sold_price", 0)
                annual_growth = d.get("annual_growth", 0.0)

                if median_price and int(median_price) != 0:
                    units_median_price.append(int(median_price))

                if annual_growth and float(annual_growth) != 0.0:
                    units_growth.append(float(annual_growth))

        data = {
            "index": 0,
            "suburb_id": k,
            "year": "2021",
        }

        try:

            final.append(
                {
                    **data,
                    "type": "House",
                    "median_sold_price": int(sum(houses_median_price) / len(houses_median_price)),
                    "annual_growth": float(sum(houses_growth) / len(houses_growth)),
                }
            )

            final.append(
                {
                    **data,
                    "type": "Unit",
                    "median_sold_price": int(sum(units_median_price) / len(units_median_price)),
                    "annual_growth": float(sum(units_growth) / len(units_growth)),
                }
            )

        except ZeroDivisionError:
            continue

    keys = final[0].keys()
    with open('domain_history_s.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(final)


def final_data():
    final_result = []
    all_fms = {}
    all_fdsh = {}
    all_fdsu = {}
    all_suburbs = []

    fm_file = open('./mag.csv')
    fd_file = open('./domain_history_s.csv')

    fm_reader = csv.DictReader(fm_file)
    fd_reader = csv.DictReader(fd_file)

    for fm in fm_reader:
        suburb_id = fm.pop("suburb_id")
        all_fms[suburb_id] = {**fm}
        all_suburbs.append(suburb_id)

    for fd in fd_reader:
        suburb_id = fd.pop("suburb_id")
        if fd["type"] == "House":
            all_fdsh[suburb_id] = {**fd}
        else:
            all_fdsu[suburb_id] = {**fd}

    for s in all_suburbs:
        try:
            fm = all_fms.get(s, None)
            fdh = all_fdsh.get(s, None)
            fdu = all_fdsu.get(s, None)

            if fdh:
                fdh.pop("index")
                annual_growth = (float(fdh.pop("annual_growth", 0)) + float(fm.get("house_average_annual_growth", 0))) / 2
                final_result.append(
                    {
                        **fdh,
                        "suburb_id": s,
                        "annual_growth": annual_growth,
                        "date_time": "2022-11-30 11:00:00",
                        "id": "0",
                        "column1": "0"
                    }
                )

            if fdu:
                fdu.pop("index")
                annual_growth = (float(fdu.pop("annual_growth", 0)) + float(fm.get("unit_average_annual_growth", 0))) / 2
                final_result.append(
                    {
                        **fdu,
                        "suburb_id": s,
                        "annual_growth": annual_growth,
                        "date_time": "2022-11-30 11:00:00",
                        "id": "0",
                        "column1": "0"
                    }
                )

            continue

        except:
            continue

    fm_file.close()
    fd_file.close()

    keys = final_result[0].keys()
    with open('final_domain_history.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(final_result)

final_data()
# domain_history()
