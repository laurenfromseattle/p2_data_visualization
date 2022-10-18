import matplotlib.pyplot as plt
from die import Die


# Create two D6 dice.
die_1 = Die()
die_2 = Die()

# Make some rolls, and store results in a list.
results = [die_1.roll() + die_2.roll() for roll_num in range(10_000)]

# Analyze the results.
max_result = die_1.num_sides + die_2.num_sides
frequencies = [results.count(value) for value in range(2, max_result + 1)]

# Plot the results.
fig, ax = plt.subplots(figsize=(15, 9))
x_values = list(range(2, max_result + 1))
ax.bar(x_values, frequencies, width=1, edgecolor="white", linewidth=2)

# Set chart title and label axes.
ax.set_title("Results of rolling two D6s 10,000 times", fontsize=18)
ax.set_xlabel("Result of Roll", fontsize=14)
ax.set_ylabel("Frequency", fontsize=14)

# Set size of tick labels.
ax.tick_params(axis="both", labelsize=14)
ax.set_xticks(x_values)

plt.show()
