from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import csv

filename = "data/sitka_weather_2021_simple.csv"
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    # Get the high temperatures `highs`, low temperatures `lows`
    # and dates from the file.
    highs, lows, dates = [], [], []
    highs_column = header_row.index("TMAX")
    lows_column = header_row.index("TMIN")
    dates_column = header_row.index("DATE")

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

    # Plot the high temperatures.
    plt.style.use("seaborn-v0_8")
    fig, ax = plt.subplots()
    highs_plot = ax.plot(
        dates, highs, "r-", linewidth=1.5, markersize=6, label="Highs", alpha=0.5
    )
    lows_plot = ax.plot(
        dates, lows, "b-", linewidth=1.5, markersize=6, label="Lows", alpha=0.5
    )
    fill = ax.fill_between(dates, highs, lows, facecolor="blue", alpha=0.1)

    # Set the chart title.
    ax.set_title(
        "Daily High and Low Temperatures in Sitka, AK - 2021",
        fontsize=18,
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
