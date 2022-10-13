import matplotlib.pyplot as plt

from random_walk import RandomWalk

# Keep making new walks, as long as the program is active.
while True:
    # Make a random walk.
    rw = RandomWalk(50_000)
    rw.fill_walk()

    # Plot the points in the walk.
    plt.style.use("classic")
    fig, ax = plt.subplots(figsize=(25.6, 14.4))
    point_numbers = range(rw.num_points)
    ax.scatter(
        rw.x_values,
        rw.y_values,
        c=point_numbers,
        cmap=plt.cm.Greens,
        edgecolors="none",
        s=5,
    )

    # Emphasize the first and last points.
    ax.scatter(0, 0, c="black", edgecolors="none", s=50)
    ax.scatter(rw.x_values[-1], rw.y_values[-1], c="red", edgecolors="none", s=50)

    # Set chart title.
    ax.set_title("A Random Walk", fontsize=18)

    # Remove tthe axes.
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    plt.show()

    keep_running = input("Make another walk? (y/n): ")
    if keep_running == "n":
        break
