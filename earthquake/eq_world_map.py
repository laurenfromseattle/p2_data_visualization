import json
import datetime as dt

from plotly.graph_objs import Scattergeo, Layout
from plotly import offline

# Load data.
filename = "data/significant_eq_data_month.json"
with open(filename) as f:
    all_eq_data = json.load(f)

# Create list of earthquakes and extract relevant data for each.
all_eq_dicts = all_eq_data["features"]
mags, lons, lats, customdata = [], [], [], []
for eq_dict in all_eq_dicts:

    mags.append(eq_dict["properties"]["mag"])
    lons.append(eq_dict["geometry"]["coordinates"][0])
    lats.append(eq_dict["geometry"]["coordinates"][1])

    place = eq_dict["properties"]["place"]

    # Times are reported in ms since the epoch, so divide by 1000.
    timestamp = eq_dict["properties"]["time"]
    time_obj = dt.datetime.fromtimestamp(timestamp / 1000, dt.timezone.utc)
    time_str = time_obj.strftime("%B %-d, %Y at %H:%M %Z")

    # Place and time tuple are going into customdata list so that I can
    # use them in the hovertemplate.
    customdata.append((place, time_str))

# Extract plot title.
plot_title = all_eq_data["metadata"]["title"]

# Map the earthquakes.
data = [
    {
        "type": "scattergeo",
        "lon": lons,
        "lat": lats,
        "customdata": customdata,
        "hovertemplate": "<b>%{customdata[0]}</b>"
        + "<br><br>"
        + "Magnitude: %{marker.color}"
        + "<br>"
        + "%{customdata[1]}"
        + "<br>"
        + "Coords: (%{lat}, %{lon})"
        + "<extra></extra>",
        "marker": {
            "size": [5 * mag for mag in mags],
            "color": mags,
            "colorscale": "Viridis",
            "reversescale": True,
            "colorbar": {"title": "Magnitude"},
        },
    }
]

my_layout = Layout(
    title=dict(font_color="black", font_size=24, text=plot_title, x=0.5),
    margin=dict(l=20, r=20, t=60, b=20),
)

fig = {"data": data, "layout": my_layout}
offline.plot(fig, filename="global_earthquakes.html")
