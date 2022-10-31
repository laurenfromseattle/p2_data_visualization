import csv
import datetime as dt

from plotly.graph_objs import Scattergeo, Layout
from plotly import offline

filename = "data/world_fires_7_day.csv"

try:
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        lats, lons, brights, dates = [], [], [], []
        lat_col = header_row.index("latitude")
        lon_col = header_row.index("longitude")
        bright_col = (
            header_row.index("brightness")
            if "brightness" in header_row
            else header_row.index("bright_ti4")
        )
        date_col = header_row.index("acq_date")
        time_col = header_row.index("acq_time")

        line_num = 1

        for row in reader:

            line_num += 1

            try:
                date_time = dt.datetime.strptime(
                    f"{row[date_col]} {row[time_col]}", "%Y-%m-%d %H%M"
                )
                date_time = date_time.replace(tzinfo=dt.timezone.utc)
                lat = float(row[lat_col])
                lon = float(row[lon_col])
                brightness = float(row[bright_col])
            except:
                print(f"Missing value on line {line_num}: {row}")
            else:
                dates.append(date_time)
                lats.append(lat)
                lons.append(lon)
                brights.append(brightness)

        # Build plot title.
        start_time = f"{dates[0]:%b %d, %Y at %H:%M %Z}"
        end_time = f"{dates[-1]:%b %d, %Y at %H:%M %Z}"
        plot_title = f"World Fire Data<br>From {start_time} to {end_time}"

        # Map the fires.
        data = [
            {
                "type": "scattergeo",
                "lat": lats,
                "lon": lons,
                "customdata": [f"{date:%b %d at %H:%M %Z}" for date in dates],
                "hovertemplate": "Brightness: %{marker.color}K"
                + "<br>"
                + "Coords: (%{lat}, %{lon})"
                + "<br>"
                + "Time acquired: %{customdata}"
                + "<extra></extra>",
                "marker": {
                    "size": 3,
                    "color": brights,
                    "colorscale": "Reds",
                    "reversescale": False,
                    "colorbar": {"title": "Brightness"},
                },
            }
        ]

        my_layout = Layout(
            title=dict(font_color="black", font_size=24, text=plot_title, x=0.5),
            margin=dict(l=20, r=20, t=80, b=20),
        )

        fig = {"data": data, "layout": my_layout}
        offline.plot(fig, filename="global_fires.html")


except FileNotFoundError:
    print("File cannot be found:", filename)
    exit()
