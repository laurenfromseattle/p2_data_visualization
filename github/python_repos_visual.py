# This package allows program to request info from website and examine the response.
import requests

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
repo_names, stars = [], []
for repo_dict in repo_dicts:
    repo_names.append(repo_dict["name"])
    stars.append(repo_dict["stargazers_count"])

# Make visualiation.
data = [
    {
        "type": "bar",
        "x": repo_names,
        "y": stars,
    }
]

layout = {
    "title": "Most-Starred Python Projects on GitHub",
    "xaxis": {"title": "Repository"},
    "yaxis": {"title": "Stars"},
}

fig = {"data": data, "layout": layout}
offline.plot(fig, filename="python_repos.html")
