from datetime import datetime
import re

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams

import csv


def get_column_indices(header_row, data):
    """
    Update `data` object with column index information for the file or
    raise a ValueError if the column is not found.
    """
    for col_name in data:
        try:
            col_index = header_row.index(col_name)
        except ValueError:
            print(f"Data column missing from file: {col_name}")
            exit()
        else:
            data[col_name]["col_index"] = col_index


def get_data(row, data):
    # Get the data points for the given `row`.
    for col_name in data:
        col_index = data[col_name]["col_index"]
        if col_name == "DATE":
            date = datetime.strptime(row[col_index], "%Y-%m-%d")
        if col_name == "TMAX":
            tmax = int(row[col_index]) if row[col_index] != "" else None
        if col_name == "TMIN":
            tmin = int(row[col_index]) if row[col_index] != "" else None
        if col_name == "PRCP":
            prcp = float(row[col_index]) if row[col_index] != "" else None

    # Append date and its data points to data object if all values exist.
    if tmax is not None and tmin is not None and prcp is not None:
        data["DATE"]["values"].append(date)
        data["TMAX"]["values"].append(tmax)
        data["TMIN"]["values"].append(tmin)
        data["PRCP"]["values"].append(prcp)
    else:
        print(f"Missing value for {date}")


filename = input("Enter the file name for csv: ")
try:
    # Default file for quick testing.
    if filename == "":
        filename = "data/sitka_2021_simple.csv"

    with open(filename) as fhand:
        reader = csv.reader(fhand)
        header_row = next(reader)

        # Set up data object to collect desired data from file: high
        # temperatures `highs`, low temperatures `lows` and
        # `precipitation`.
        data = {"DATE": {}, "TMAX": {}, "TMIN": {}, "PRCP": {}}

        # Update data object with index information, i.e., where each
        # desired data point is located in the file.
        get_column_indices(header_row, data)

        # Create empty lists to collect the data points.
        for col_name in data:
            data[col_name]["values"] = []

        # Loop through every row in the file and collect desired data.
        for row in reader:
            get_data(row, data)

        # Get station name from the file to use in chart title.
        location_column = header_row.index("NAME")
        location_raw = row[location_column]
        location_parsed = re.findall("([A-Z ]+), ([A-Z]+)", location_raw)[0]
        city = location_parsed[0].title()
        state = location_parsed[1]
        location_formatted = f"{city}, {state}"

        # Get year from dates to use in chart title.
        year = data["DATE"]["values"][0].year

        # Set up the figure.
        plt.style.use("seaborn-v0_8")
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(8.5, 11))
        fig.tight_layout(rect=(0.05, 0, 1, 0.95), h_pad=0)
        fig.suptitle(
            f"Annual Weather Trends: {year}\n{location_formatted}",
            fontsize=16,
            fontweight="bold",
        )

        # Plot the high and low temperatures.
        dates = data["DATE"]["values"]
        highs = data["TMAX"]["values"]
        lows = data["TMIN"]["values"]
        ax1.plot(dates, highs, "r-", linewidth=1.5, label="Highs", alpha=0.5)
        ax1.plot(dates, lows, "b-", linewidth=1.5, label="Lows", alpha=0.5)
        ax1.fill_between(dates, highs, lows, facecolor="blue", alpha=0.1)

        # Plot the precipitation.
        precipitation = data["PRCP"]["values"]
        ax2.plot(dates, precipitation, "g-", linewidth=1.5, alpha=0.5)
        ax2.fill_between(dates, 0, precipitation, facecolor="green", alpha=0.1)

        # Set the chart titles.
        # ax1.set_title("Daily High and Low Temperatures", fontsize=14, pad=10, loc="left")
        # ax2.set_title(f"Daily Precipitation", fontsize=14, pad=10, loc="left")
        # The x and y axes labels.
        ax1.tick_params(axis="both", labelsize=12)
        ax1.set_xlabel("", labelpad=10, fontsize=14)
        ax1.set_ylabel("Temperature (F)", labelpad=10, fontsize=14)
        ax2.tick_params(axis="both", labelsize=12)
        ax2.set_xlabel("", labelpad=10, fontsize=14)
        ax2.set_ylabel("Precipitation (inches)", labelpad=10, fontsize=14)

        # X axis tick marks.
        locator = mdates.MonthLocator()
        format = mdates.DateFormatter("%b")
        ax1.xaxis.set_major_locator(locator)
        ax1.xaxis.set_major_formatter(format)
        # ax1.tick_params(axis="x", color="darkgray", length=5, direction="out")
        # ax2.xaxis.set_major_locator(locator)
        # ax2.xaxis.set_major_formatter(format)
        # ax2.tick_params(axis="x", color="darkgray", length=5, direction="out")

        # Enable the legend.
        ax1.legend(fontsize=12)

        plt.show()

except FileNotFoundError:
    print("File cannot be found:", filename)
    exit()
