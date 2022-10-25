from datetime import datetime
import re

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams

import csv


def parse_date(date):
    return datetime.strptime(date, "%Y-%m-%d")


def parse_int(temp):
    return int(temp) if temp != "" else None


def parse_float(prcp):
    return float(prcp) if prcp != "" else None


def build_data_structure(datatypes):
    data = {}
    for datatype in datatypes:
        data[datatype] = {"column_index": None, "datapoints": []}

    if "DATE" in data:
        data["DATE"]["parse"] = parse_date

    if "TMAX" in data:
        data["TMAX"]["parse"] = parse_int

    if "TMIN" in data:
        data["TMIN"]["parse"] = parse_int

    if "PRCP" in data:
        data["PRCP"]["parse"] = parse_float

    return data


def get_column_indices(header_row, data):
    """
    Update `data` object with column index information for the file or
    raise a ValueError if the column is not found.
    """
    for datatype in data:
        try:
            column_index = header_row.index(datatype)
        except ValueError:
            print(f"Data missing from file: {datatype}")
            exit()
        else:
            data[datatype]["column_index"] = column_index


def get_data(row, data):
    """
    Update `data` object with data from a given `row`.
    """
    dataset = []
    for datatype in data:
        data_string = row[data[datatype]["column_index"]]
        datapoint = data[datatype]["parse"](data_string)
        dataset.append((datatype, datapoint))

    if len([datapoint for (datatype, datapoint) in dataset if datapoint is None]) == 0:
        for (datatype, datapoint) in dataset:
            data[datatype]["datapoints"].append(datapoint)
    else:
        date = [datapoint for (datatype, datapoint) in dataset if datatype == "DATE"][0]
        missing_data = [
            datatype for (datatype, datapoint) in dataset if datapoint is None
        ]
        for datatype in missing_data:
            print(f"Missing {datatype} value for {date}")


def format_location(location_data_string):
    location_parsed = re.findall("([A-Z ]+), ([A-Z]+)", location_data_string)[0]
    city = location_parsed[0].title()
    state = location_parsed[1]
    location_formatted = f"{city}, {state}"
    return location_formatted
