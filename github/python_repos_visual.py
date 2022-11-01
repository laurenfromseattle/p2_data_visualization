# This package allows program to request info from website and examine the response.
import requests
import textwrap

from plotly.graph_objects import Bar
from plotly import offline

# Make an API call and store the response.
url = "https://api.github.com/search/repositories?q=language:python+stars:>1000&sort=stars"
headers = {"Accept": "application/vnd.github.v3+json"}
r = requests.get(url, headers=headers)
print(f"Status code: {r.status_code}")

# Process results.
response_dict = r.json()
repo_dicts = response_dict["items"]
repo_links, stars, hovertexts = [], [], []
for repo_dict in repo_dicts:
    repo_name = repo_dict["name"]
    repo_url = repo_dict["html_url"]
    repo_link = f"<a href='{repo_url}' target='_blank'>{repo_name}</a>"
    repo_links.append(repo_link)

    stars.append(repo_dict["stargazers_count"])

    owner = repo_dict["owner"]["login"]
    description = repo_dict["description"]
    if len(description) > 75:
        lines = textwrap.wrap(description, width=75, max_lines=3)
        description = "<br>".join(lines)

    hovertext = [repo_name, owner, description]
    hovertexts.append(hovertext)

# Make visualiation.
data = [
    {
        "type": "bar",
        "x": repo_links,
        "y": stars,
        "customdata": hovertexts,
        "hovertemplate": "<b>%{customdata[0]}</b>" + "<br>" + "Stars: %{y}"
        "<br>"
        + "Author: %{customdata[1]}"
        + "<br><br>"
        + "<i>%{customdata[2]}</i>"
        + "<extra></extra>",
        "marker": {
            "color": "rgb(60, 100, 150)",
            "line": {"width": 1.5, "color": "rgb(25, 25, 25)"},
        },
        "opacity": 0.6,
    }
]

layout = {
    "title": {"text": "Most-Starred Python Projects on GitHub", "x": 0.5},
    "titlefont": {"size": 28},
    "xaxis": {
        "title": "Repository",
        "titlefont": {
            "size": 24,
        },
        "tickfont": {"size": 14},
    },
    "yaxis": {"title": "Stars", "titlefont": {"size": 24}, "tickfont": {"size": 14}},
}

fig = {"data": data, "layout": layout}
offline.plot(fig, filename="python_repos.html")
