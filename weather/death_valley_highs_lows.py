from datetime import datetime
import re

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams

import csv

filename = "data/death_valley_2018_simple.csv"
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    # Get the high temperatures `highs`, low temperatures `lows`
    # and dates from the file.
    dates, highs, lows = [], [], []
    dates_column = header_row.index("DATE")
    highs_column = header_row.index("TMAX")
    lows_column = header_row.index("TMIN")

    for row in reader:
        date = datetime.strptime(row[dates_column], "%Y-%m-%d")

        try:
            high = int(row[highs_column])
            low = int(row[lows_column])
        except ValueError:
            print(f"Missing value for {date}")
        else:
            dates.append(date)
            highs.append(high)
            lows.append(low)

    # Get station name from the file to use in chart title.
    location_column = header_row.index("NAME")
    location_raw = row[location_column]
    location_parsed = re.findall("([A-Z ]+), ([A-Z]+)", location_raw)[0]
    city = location_parsed[0].title()
    state = location_parsed[1]
    location_formatted = f"{city}, {state}"

    # Get year from dates to use in chart title.
    year = dates[0].year

    # Plot the high temperatures.
    plt.style.use("seaborn-v0_8")
    fig, ax = plt.subplots(figsize=(10, 6))

    highs_plot = ax.plot(
        dates, highs, "r-", linewidth=1.5, markersize=6, label="Highs", alpha=0.5
    )
    lows_plot = ax.plot(
        dates, lows, "b-", linewidth=1.5, markersize=6, label="Lows", alpha=0.5
    )
    fill = ax.fill_between(dates, highs, lows, facecolor="blue", alpha=0.1)

    # Set the chart title.
    ax.set_title(
        f"Daily High and Low Temperatures, {year}\n{location_formatted}",
        fontsize=16,
        fontweight="bold",
        pad=10,
    )
    # The x and y axes labels.
    ax.tick_params(axis="both", labelsize=12)
    ax.set_xlabel("", labelpad=10, fontsize=14)
    ax.set_ylabel("Temperature (F)", labelpad=10, fontsize=14)

    # X axis tick marks.
    locator = mdates.MonthLocator()
    format = mdates.DateFormatter("%b")
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(format)
    ax.tick_params(axis="x", color="darkgray", length=5, direction="out")

    # Enable the legend.
    ax.legend()

    plt.show()
