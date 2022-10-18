from plotly.graph_objs import Bar, Layout
from plotly import offline

from die import Die

# Create two D6 dice.
die_1 = Die()
die_2 = Die()

# Make some rolls, and store results in a list.
results = [die_1.roll() + die_2.roll() for roll_num in range(10_000)]

# Analyze the results.
max_result = die_1.num_sides + die_2.num_sides
frequencies = [results.count(value) for value in range(2, max_result + 1)]

# Visualize the results.
x_values = list(range(2, max_result + 1))
data = [Bar(x=x_values, y=frequencies)]

x_axis_config = {
    "title": {
        "text": "Result of Roll",
        "font_family": "Raleway",
        "font_size": 18,
    },
    "tickfont": {
        "size": 16,
        "family": "Raleway",
    },
    "dtick": 1,
}
y_axis_config = {
    "title": {
        "text": "Frequency of Result",
        "font_family": "Raleway",
        "font_size": 18,
    },
    "tickfont": {
        "size": 16,
        "family": "Raleway",
    },
}
title_config = {
    "text": "Results of rolling two D6s 10,000 times",
    "xanchor": "center",
    "x": 0.5,
    "xref": "paper",
    "font_family": "Raleway",
    "font_size": 24,
}
layout = Layout(
    title=title_config,
    xaxis=x_axis_config,
    yaxis=y_axis_config,
)

offline.plot({"data": data, "layout": layout}, filename="d6_d6.html")
