from datetime import datetime
import re

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams

import csv

filename = "data/sitka_2021_simple.csv"
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    # Get the `dates`, high temperatures `highs`, low temperatures `lows`
    # and `precipitation` from the file.
    dates, highs, lows, precipitations = [], [], [], []
    dates_column = header_row.index("DATE")
    highs_column = header_row.index("TMAX")
    lows_column = header_row.index("TMIN")
    precipitation_column = header_row.index("PRCP")

    for row in reader:
        date = datetime.strptime(row[dates_column], "%Y-%m-%d")

        try:
            high = int(row[highs_column])
            low = int(row[lows_column])
            precipitation = float(row[precipitation_column])
        except ValueError:
            print(f"Missing value for {date}")
        else:
            dates.append(date)
            highs.append(high)
            lows.append(low)
            precipitations.append(precipitation)

    # Get station name from the file to use in chart title.
    location_column = header_row.index("NAME")
    location_raw = row[location_column]
    location_parsed = re.findall("([A-Z ]+), ([A-Z]+)", location_raw)[0]
    city = location_parsed[0].title()
    state = location_parsed[1]
    location_formatted = f"{city}, {state}"

    # Get year from dates to use in chart title.
    year = dates[0].year

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
    ax1.plot(dates, highs, "r-", linewidth=1.5, label="Highs", alpha=0.5)
    ax1.plot(dates, lows, "b-", linewidth=1.5, label="Lows", alpha=0.5)
    ax1.fill_between(dates, highs, lows, facecolor="blue", alpha=0.1)

    # Plot the precipitation.
    ax2.plot(dates, precipitations, "g-", linewidth=1.5, alpha=0.5)
    ax2.fill_between(dates, 0, precipitations, facecolor="green", alpha=0.1)

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
