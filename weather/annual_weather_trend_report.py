from datetime import datetime
import re
import csv

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams

import annual_weather_trend_functions as awt


def process_data(filename="data/sitka_2018_simple.csv"):

    try:

        with open(filename) as fhand:
            reader = csv.reader(fhand)
            header_row = next(reader)

            # Set up data object to collect desired datapoints from file.
            datatypes = ["DATE", "TMAX", "TMIN", "PRCP"]
            data = awt.build_data_structure(datatypes)

            # Check that all datatypes are in the file and update data object
            # with column indices.
            awt.get_column_indices(header_row, data)

            # Loop through every row in the file and collect desired data.
            for row in reader:
                awt.get_data(row, data)

            # Get location name from the file and add to `data` object.
            location_column = header_row.index("NAME")
            location_raw = row[location_column]
            location_formatted = awt.format_location(location_raw)
            data["LOCATION"] = location_formatted

        return data

    except FileNotFoundError:
        print("File cannot be found:", filename)
        return None


def plot_data(data, data2=None):
    plt.style.use("seaborn-v0_8")
    # Get location and year for chart title.
    location = data["LOCATION"]
    year = data["DATE"]["datapoints"][0].year
    if data2:
        location2 = data2["LOCATION"]
        year2 = data2["DATE"]["datapoints"][0].year

    # Set up the figure.
    if data2:
        fig, ((ax1, ax3), (ax2, ax4)) = plt.subplots(
            nrows=2,
            ncols=2,
            sharex="col",
            sharey="row",
            figsize=(17, 11),
        )
        fig.suptitle(
            f"Annual Weather Trends:\n{location} ({year}) vs. {location2} ({year2})",
            fontsize=16,
            fontweight="bold",
        )
    else:
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(8.5, 11))

        fig.suptitle(
            f"Annual Weather Trends: {year}\n{location}",
            fontsize=16,
            fontweight="bold",
        )

    fig.tight_layout(rect=(0.03, 0, 1, 0.95), w_pad=8.0)

    # Plot the high and low temperatures.
    dates = data["DATE"]["datapoints"]
    highs = data["TMAX"]["datapoints"]
    lows = data["TMIN"]["datapoints"]
    ax1.plot(dates, highs, "r-", linewidth=1.5, label="Highs", alpha=0.5)
    ax1.plot(dates, lows, "b-", linewidth=1.5, label="Lows", alpha=0.5)
    ax1.fill_between(dates, highs, lows, facecolor="blue", alpha=0.1)
    if data2:
        dates2 = data2["DATE"]["datapoints"]
        highs2 = data2["TMAX"]["datapoints"]
        lows2 = data2["TMIN"]["datapoints"]
        ax3.plot(dates2, highs2, "r-", linewidth=1.5, label="Highs", alpha=0.5)
        ax3.plot(dates2, lows2, "b-", linewidth=1.5, label="Lows", alpha=0.5)
        ax3.fill_between(dates2, highs2, lows2, facecolor="blue", alpha=0.1)

    # Plot the precipitation.
    precipitation = data["PRCP"]["datapoints"]
    ax2.plot(dates, precipitation, "g-", linewidth=1.5, alpha=0.5)
    ax2.fill_between(dates, 0, precipitation, facecolor="green", alpha=0.1)
    if data2:
        precipitation2 = data2["PRCP"]["datapoints"]
        ax4.plot(dates2, precipitation2, "g-", linewidth=1.5, alpha=0.5)
        ax4.fill_between(dates2, 0, precipitation2, facecolor="green", alpha=0.1)

    # Set the chart titles.
    if data2:
        ax1.set_title(
            f"{location}", fontsize=14, fontweight="bold", pad=10, loc="center"
        )
        ax3.set_title(
            f"{location2}", fontsize=14, fontweight="bold", pad=10, loc="center"
        )

    # The x and y axes labels.
    ax1.tick_params(axis="both", labelsize=12)
    ax1.set_xlabel("", labelpad=10, fontsize=14)
    ax1.set_ylabel("Temperature (F)", labelpad=10, fontsize=14)
    ax2.tick_params(
        axis="both",
        labelsize=12,
    )
    ax2.set_xlabel("", labelpad=10, fontsize=14)
    ax2.set_ylabel("Precipitation (inches)", labelpad=10, fontsize=14)
    if data2:
        ax3.tick_params(axis="both", labelsize=12, labelleft=True)
        ax3.set_xlabel("", labelpad=10, fontsize=14)
        ax3.set_ylabel("Temperature (F)", labelpad=10, fontsize=14)
        ax4.tick_params(axis="both", labelsize=12, labelleft=True)
        ax4.set_xlabel("", labelpad=10, fontsize=14)
        ax4.set_ylabel("Precipitation (inches)", labelpad=10, fontsize=14)

    # X axis tick marks.
    locator = mdates.MonthLocator()
    format = mdates.DateFormatter("%b")
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(format)
    if data2:
        ax3.xaxis.set_major_locator(locator)
        ax3.xaxis.set_major_formatter(format)

    # Enable the legend.
    ax1.legend(fontsize=12)
    if data2:
        ax3.legend(fontsize=12)

    print(f"Now showing plot for {location}")
    plt.show()


filename = input(
    "Enter the filename where the location's annual weather data can be found: "
)
location_data = process_data(filename) if filename != "" else process_data()

locations_to_compare = []
comparison = input(
    "Would you like to compare the weather data from this location with other locations? Y or N: "
)
if comparison.strip().lower() == "y" or comparison.strip().lower() == "yes":

    while True:
        filename = input("Enter the filename to compare: ")
        comparison_data = process_data(filename)
        if comparison_data:
            locations_to_compare.append(comparison_data)
        add_location = input(
            "Would you like to add another location to compare? Y or N: "
        )
        if add_location.strip().lower() == "y" or add_location.strip().lower() == "yes":
            continue
        else:
            break


if locations_to_compare:
    for comparison_data in locations_to_compare:
        plot_data(location_data, comparison_data)
else:
    plot_data(location_data)
