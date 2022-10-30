import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class WeatherPlot:
    def __init__(self, station, stations_to_compare=[]):
        self.name = station.name
        self.dates = station.dates
        self.highs = station.temps["highs"]
        self.lows = station.temps["lows"]
        self.avgs = station.temps["avgs"]
        self.prcp = station.prcp
        self.stations_to_compare = stations_to_compare

    def plot(self):

        plt.style.use("seaborn-v0_8")

        # Plot data.
        start_date = self.dates[0]
        end_date = self.dates[-1]

        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(8.5, 11))

        ax1.plot(self.dates, self.highs, "r-", linewidth=1.5, label="Highs", alpha=0.5)
        ax1.plot(self.dates, self.lows, "b-", linewidth=1.5, label="Lows", alpha=0.5)
        ax1.fill_between(self.dates, self.highs, self.lows, facecolor="blue", alpha=0.1)

        ax2.plot(self.dates, self.prcp, "g-", linewidth=1.5, alpha=0.5)
        ax2.fill_between(self.dates, 0, self.prcp, facecolor="green", alpha=0.1)

        # Prepare display.

        # rect: tuple(left, bottom, right, top), default is (0, 0, 1, 1)
        fig.tight_layout(rect=(0.03, 0.03, 1, 0.93), w_pad=8.0)

        fig.suptitle(
            f"Weather Data for {self.name}\n{start_date:%b %d, %Y} to {end_date:%b %d, %Y}",
            fontsize=16,
            fontweight="bold",
        )

        ax1.tick_params(axis="both", labelsize=12)
        ax1.set_ylabel("Temperature (F)", labelpad=10, fontsize=14)
        ax1.legend(fontsize=12)

        locator = mdates.MonthLocator()
        format = mdates.DateFormatter("%b '%y")
        ax1.xaxis.set_major_locator(locator)
        ax1.xaxis.set_major_formatter(format)

        ax2.tick_params(axis="both", labelsize=12)
        ax2.tick_params(axis="x", labelrotation=45)
        ax2.set_ylabel("Precipitation (inches)", labelpad=10, fontsize=14)

        # Loop through comparison stations, if any.
        if self.stations_to_compare:
            for station in self.stations_to_compare:
                name = station.name
                dates = station.dates
                avgs = station.temps["avgs"]
                prcp = station.prcp

                # Plot data.
                start_date = dates[0]
                end_date = dates[-1]

                fig, (ax1, ax2) = plt.subplots(
                    nrows=2, ncols=1, sharex=True, figsize=(8.5, 11)
                )

                ax1.plot(dates, avgs, "m-", linewidth=1.5, label=name, alpha=0.5)
                ax1.plot(
                    self.dates,
                    self.avgs,
                    "k-",
                    linewidth=1.5,
                    label=self.name,
                    alpha=0.5,
                )

                ax2.plot(dates, prcp, "m-", linewidth=1.5, label=name, alpha=0.5)
                ax2.plot(
                    self.dates,
                    self.prcp,
                    "k-",
                    linewidth=1.5,
                    label=self.name,
                    alpha=0.5,
                )

                # Prepare display.
                fig.tight_layout(rect=(0.03, 0.03, 1, 0.93), w_pad=8.0)

                fig.suptitle(
                    f"Weather Data Comparison\n{name} and {self.name}",
                    fontsize=16,
                    fontweight="bold",
                )

                ax1.tick_params(axis="both", labelsize=12)
                ax1.set_ylabel("Average Temperature (F)", labelpad=10, fontsize=14)
                ax1.legend(fontsize=12)

                locator = mdates.MonthLocator()
                format = mdates.DateFormatter("%b '%y")
                ax1.xaxis.set_major_locator(locator)
                ax1.xaxis.set_major_formatter(format)

                ax2.tick_params(axis="both", labelsize=12)
                ax2.tick_params(axis="x", labelrotation=45)
                ax2.set_ylabel("Precipitation (inches)", labelpad=10, fontsize=14)
                ax2.legend(fontsize=12)

        # Display.
        plt.show()
