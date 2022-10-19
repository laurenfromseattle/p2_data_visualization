import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


x_values = range(1, 1001)
y_values = [x**2 for x in x_values]

plt.style.use("seaborn-v0_8")
fig, ax = plt.subplots()
# ax.scatter(x_values, y_values, color=(1, 0.5, 0), s=10)
ax.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Oranges, s=10)

# Set chart title and label axes.
ax.set_title("Square Numbers", fontsize=18)
ax.set_xlabel("Value", fontsize=14)
ax.set_ylabel("Square of Value", fontsize=14)

# Set size of tick labels.
ax.tick_params(axis="both", labelsize=14)
fmt = "{x:,.0f}"
tick = mtick.StrMethodFormatter(fmt)
ax.yaxis.set_major_formatter(tick)

# Set the range for each axis.
ax.axis([0, 1_100, 0, 1_100_000])

# plt.show()
plt.savefig("squares_plot.png", bbox_inches="tight")
