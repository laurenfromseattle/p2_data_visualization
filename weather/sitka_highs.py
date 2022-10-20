from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import csv

filename = "data/sitka_weather_07-2022_simple.csv"
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    for index, column_header in enumerate(header_row):
        print(f"{index}: {column_header}")

    # Get the high temperatures `highs` from the file.
    highs_column = header_row.index("TMAX")
    highs = []
    for row in reader:
        high = int(row[highs_column])
        highs.append(high)

    # Plot the high temperatures.
    plt.style.use("seaborn-v0_8")

    calendar_days_in_month = list(range(1, len(highs) + 1))
    fig, ax = plt.subplots()
    highs_plot = ax.plot(
        calendar_days_in_month, highs, "r^:", linewidth=1.5, markersize=6, label="Highs"
    )

    # Set the chart title.
    ax.set_title(
        "Daily Temperatures in Sitka, AK, for July 2022",
        fontsize=18,
        fontweight="bold",
        pad=10,
    )
    # Label the x and y axes.
    ax.set_xlabel("Day of month", labelpad=10, fontsize=14)
    ax.set_ylabel("Temperature in degrees Fahrenheit", labelpad=10, fontsize=14)
    ax.tick_params(axis="both", labelsize=12)

    # Set and style the major tick marks on the x axis.
    ax.set_xticks([day for day in calendar_days_in_month if day % 2 == 0])
    ax.tick_params(
        axis="x", labelrotation=45, color="darkgray", length=10, direction="inout"
    )

    # Set and style the minor tick marks on the x axis.
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.set_xticks([day for day in calendar_days_in_month if day % 2 == 1], minor=True)
    ax.tick_params(
        axis="x", which="minor", color="darkgray", length=5, direction="inout"
    )

    # Enable the legend.
    ax.legend()

    plt.show()
