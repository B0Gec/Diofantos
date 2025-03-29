import numpy as np
import matplotlib.pyplot as plt


with open('../../../relevant_seqs.txt', 'r') as file:  # Use.
    text = file.read()

seqs = [int(seq) for seq in text[1:-1].split(",")]




# Make a random dataset:
# height = [3, 12, 5, 18, 45]
height = per_orders
# bars = ['A', 'B', 'C', 'D', 'Z']
bars = orders
y_pos = np.arange(len(bars))
# plt.ylabel =

# Create bars
# plt.bar(y_pos, height, label='num seq', zorder=0)




# plt.grid(linestyle='--', axis='y', alpha=0.7)
# minor_ticks = np.arange(0, 6000, 20)
# plt.set_yticks(minor_ticks, minor=True)
plt.grid(visible=True, which='both', axis='both', zorder=3)
threshold = 100
sporadity = 2
# def sparse(l: list): return l[:threshold]+l[threshold::sporadity]
# height = sparse(height)
# bars = sparse(bars)
# y_pos = sparse(y_pos)


plt.bar(y_pos, height, label='num seq', zorder=0)
# a.grid(visible=True, which='both', axis='both', zorder=3)

# Create names on the x-axis
plt.xticks(y_pos, bars, rotation='vertical')

plt.ylabel('number of sequences')
plt.xlabel('order')
plt.title('number of sequences per order')

# Show graphic
plt.show()
plt.clf()
