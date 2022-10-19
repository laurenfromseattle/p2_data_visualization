import matplotlib.pyplot as plt

from p2_data_visualization.dice.random_walk.random_walk import RandomWalk

# Keep making new walks, as long as the program is active.
while True:
    # Make a random walk.
    rw = RandomWalk(5_000)
    rw.fill_walk()

    # Plot the points in the walk.
    plt.style.use("classic")
    fig, ax = plt.subplots(figsize=(15, 9))
    point_numbers = range(rw.num_points)
    ax.plot(rw.x_values, rw.y_values, color="goldenrod", linewidth=2, zorder=0)
    # ax.scatter(
    #     rw.x_values,
    #     rw.y_values,
    #     c=point_numbers,
    #     cmap=plt.cm.Greens,
    #     edgecolors="none",
    #     s=2,
    # )

    # Emphasize and label the first and last points.
    ax.scatter(0, 0, c="green", edgecolors="none", s=100, zorder=1)
    ax.text(
        2,
        4,
        "Start",
        color="green",
        fontsize=12,
        fontweight=700,
    )
    ax.scatter(
        rw.x_values[-1], rw.y_values[-1], c="black", edgecolors="none", s=100, zorder=1
    )
    ax.text(
        (rw.x_values[-1] + 2),
        (rw.y_values[-1] + 4),
        "End",
        fontsize=12,
        fontweight=700,
        color="black",
    )

    # Set chart title.
    ax.set_title("Simulated Path of a Pollen Grain on Water Surface", fontsize=18)

    # Remove the axes.
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    plt.show()

    keep_running = input("Run another simulation? (y/n): ")
    if keep_running == "n":
        break
