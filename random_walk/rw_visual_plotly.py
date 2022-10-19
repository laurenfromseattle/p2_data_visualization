from plotly.graph_objects import Scatter, Layout
from plotly import offline

from p2_data_visualization.dice.random_walk.random_walk import RandomWalk

# Keep making new walks, as long as the program is active.
while True:
    # Make a random walk.
    rw = RandomWalk(5_000)
    rw.fill_walk()

    # Set up the data
    line_config = {"color": "darkgoldenrod"}
    min_xvalue = min(rw.x_values)
    max_xvalue = max(rw.x_values)
    data = [Scatter(x=rw.x_values, y=rw.y_values, name="Path", line=line_config)]

    # Add trace for start point
    start_marker_config = {"color": "springgreen", "size": 10}
    data += [
        Scatter(
            x=(0,), y=(0,), name="Start", mode="markers", marker=start_marker_config
        )
    ]

    # Add trace for end point
    start_marker_config = {"color": "firebrick", "size": 10}
    data += [
        Scatter(
            x=(rw.x_values[-1],),
            y=(rw.y_values[-1],),
            name="End",
            mode="markers",
            marker=start_marker_config,
        )
    ]

    # Configure the layout
    title_config = {
        "text": "Simulated Path Taken by a Grain of Pollen on the Surface of Water",
        "xanchor": "center",
        "x": 0.5,
        "xref": "paper",
        "font": {"size": 24},
    }
    xaxis_config = {
        "showticklabels": False,
        "showgrid": False,
        "visible": False,
        "range": [min_xvalue - 10, max_xvalue + 10],
    }
    yaxis_config = {"showticklabels": False, "showgrid": False, "visible": False}
    layout = Layout(
        title=title_config,
        xaxis=xaxis_config,
        yaxis=yaxis_config,
        plot_bgcolor="cornflowerblue",
    )

    # Plot the graph
    offline.plot({"data": data, "layout": layout}, filename="random_walk.html")

    keep_running = input("Run another simulation? (y/n): ")
    if keep_running == "n":
        break
