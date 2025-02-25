# import matplotlib.pyplot as plt
#
# # Pie chart data
# labels = ['Group 1', 'Group 2', 'Group 3', 'Group 4']
# sizes = [25, 25, 25, 25]
#
# # Plot pie chart
# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
# ax1.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
# # Write me a python code for ploting stunningly beuatiful and professional pie chart.
#
# plt.show()
#

# # Import matplotlib.pyplot module
# import matplotlib.pyplot as plt
#
# # Define the labels and sizes of the pie slices
# labels = ["Apple", "Banana", "Cherry", "Durian"]
# sizes = [15, 30, 45, 10]
#
# # Define the colors and explode parameters of the pie slices
# colors = ["red", "yellow", "pink", "green"]
# explode = (0.1, 0, 0.1, 0) # only explode the first and third slices
#
# # Plot the pie chart with some customizations
# plt.pie(sizes,
#         explode=explode,
#         labels=labels,
#         colors=colors,
#         autopct="%1.1f%%", # show percentage with one decimal place
#         shadow=True, # add a shadow effect
#         startangle=90) # start from 90 degrees angle
#
# # Set the aspect ratio to be equal so that the pie is circular
# plt.axis("equal")
#
# # Add a title to the plot
# plt.title("A Stunningly Beautiful and Professional Pie Chart")
#
# # Show the plot
# plt.show()


# import matplotlib
# import matplotlib.pyplot as plt
#
# values = [60, 80, 90, 55, 10, 30]
# colors = ['b', 'g', 'r', 'c', 'm', 'y']
# labels = ['US', 'UK', 'India', 'Germany', 'Australia', 'South Korea']
# explode = (0.2, 0, 0, 0, 0, 0)
#
# plt.pie(values,
#         colors=colors,
#         labels=values,
#         explode=explode,
#         counterclock=False,
#         shadow=True)
#
# plt.title('Population Density Index')
#
# # Create a list of handles for the legend
# handles = []
# for i, l in enumerate(labels):
#     handles.append(matplotlib.patches.Patch(color=plt.cm.Set3((i)/8.), label=l))
#
# # Add the legend with custom handles
# plt.legend(handles,
#            labels,
#            bbox_to_anchor=(0.85,1.025),
#            loc="upper left")
#
# plt.show()


# import matplotlib.pyplot as plt
#
# values = [60, 80, 90, 55, 10, 30]
# colors = ['b', 'g', 'r', 'c', 'm', 'y']
# labels = ['US', 'UK', 'India', 'Germany', 'Australia', 'South Korea']
# explode = (0.2, 0, 0, 0, 0, 0)
#
# # Add autopct argument with a format string
# plt.pie(values,
#         colors=colors,
#         labels=labels,
#         explode=explode,
#         counterclock=False,
#         shadow=True,
#         # autopct=' (%d)',
#         # autopct='%1.1f%% (%d)',
#         # autopct='%1.1f% (%d)%',
#         ) # show percentage and number
#
# plt.title('Population Density Index')
#
# plt.show()

# import sys
# import matplotlib
# print(sys.version)
# print(matplotlib.__version__)


# nested:


import matplotlib.pyplot as plt
import seaborn as sns

import gather_results as gr

# printout = f"""
#     {id_oeis: >5} = {id_oeis / n_of_seqs * 100:0.3} % - (is oeis) - successfully found equations that are identical to the recursive equations written in OEIS (hereinafter - OEIS equation)
#     {non_id: >5} = {non_id / n_of_seqs * 100:0.3} % - (non_id) - successfully found equations that are more complex than the OEIS equation
#     {non_manual: >5} = {non_manual / n_of_seqs * 100:0.3} % - (non_manual) - successfully found equations that do not apply do not apply to test cases
#     {fail: >5} = {fail / n_of_seqs * 100:0.3} % - (fail) - failure, no equation found. (but program finished smoothly, no runtime error)
#     {reconst_non_manual: >5} = {reconst_non_manual / n_of_seqs * 100:0.3} % - (reconst_non_manual) - fail in program, specifically: reconstructed oeis and wrong on test cases.
#
#     {jobs_fail: >5} = {jobs_fail / n_of_seqs * 100:0.3} % - runtime errors - jobs failed
#     {fail + jobs_fail: >5} = {(fail + jobs_fail) / n_of_seqs * 100:0.3} % - all fails  <--- (look this) ---
#     {n_of_seqs: >5} - all sequences in our dataset
#
#
#     {official_success: >5} = {official_success / n_of_seqs * 100:0.3} % - official success (id_oeis + non_id)
#     """

pie1_labels = [
    'equations identical to the ones in the OEIS were found',
    'equations found differ to those in the OEIS',
    'equations found fail on test cases',
    'failure, no equation found (including failed jobs)',
]

sub_pie_labels = [
    'equations identical to the ones in the OEIS were found',
    'equations found differ to those in the OEIS',
    'equations found fail on test cases',
    'failure, jobs finished smoothly',
    'failure, jobs failed',
]


results = [
    gr.id_oeis,
    gr.non_id,
    gr.non_manual,
    gr.fail,
    gr.reconst_non_manual,
    gr.jobs_fail,
    gr.fail + gr.jobs_fail,
    gr.n_of_seqs,
    gr.official_success,
    ]

pie1 = [
    gr.id_oeis,
    gr.non_id,
    gr.non_manual,
    gr.fail + gr.jobs_fail,
    ]

sub_pie = [
    gr.id_oeis,
    gr.non_id,
    gr.non_manual,
    gr.fail,
    gr.jobs_fail,
]


#define data
data = [15, 25, 25, 30, 5]
labels = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5']

#define Seaborn color palette to use
colors = sns.color_palette('bright')[0:len(labels)]
#
# #create pie chart
# plt.pie(data, labels = labels, colors = colors, autopct='%.0f%%')
# plt.show()

import numpy as np
import matplotlib.pyplot as plt


# Creating dataset
cars = ['AUDI', 'BMW', 'FORD',
        'TESLA', 'JAGUAR', 'MERCEDES']
cars = pie1_labels
# cars.reverse()
# print(cars)

data = [23, 17, 35, 29, 12, 41]
data = pie1
# data.reverse()
# print(data)

if len(data) != len(cars):
    raise IndexError

# Creating autocpt arguments
def func(pct, allvalues):
    absolute = int(pct / 100. * np.sum(allvalues))
    return "{:d}\n({:1.1f} %)".format(absolute, pct)


size = 0.3

# Creating plot
fig, ax = plt.subplots(figsize=(14, 5))

sub_colors = plt.rcParams['axes.prop_cycle'].by_key()['color'][:4]
sub_colors = sub_colors[:]
print(sub_colors)

cmap = plt.get_cmap("tab20c")
cmap = plt.get_cmap("tab20b")
# cmap = plt.get_cmap("tab20")
outer_colors = cmap(np.arange(len(pie1))*4)
at = 3
print(at*4+1, at*4+2)
# 0, 4, 8, 12
inner_colors = np.vstack((outer_colors[:at], cmap(np.array([(at)*4 + 1, at*4 + 2]))))
# inner_colors = np.vstack((outer_colors[:at], cmap(np.array([11, 12]))))
print(outer_colors)
print(cmap(np.arange(4)*4))
# inner_colors = np.vstack((outer_colors[:at], cmap(np.array([(at-0)*4 + 1-1, at*4 + 2]))))
print(outer_colors)

print('inner', inner_colors)
# print(cmap([0,4,8,12]))

# inner_colors = cmap(np.array([0, 4, 8, 3, 11]))
#                              0, 4, 8

wedges, texts, = ax.pie(data,
                        # autopct=lambda pct: func(pct, data),
                        labels=cars,
                        colors=outer_colors,
                        startangle=90,
                        # startangle=30,
                        # startangle=0,
                        counterclock=False,
                        textprops=dict(color="white"),
                        wedgeprops=dict(width=size, edgecolor="white"),
                        radius=1,
                        # center=(12, 5),
                        )

wedges, texts, aut2, = ax.pie(sub_pie,
                              autopct=lambda pct: func(pct, sub_pie),
                              # labels=sub_pie_labels,
                              colors=inner_colors,
                              startangle=90,
                              # startangle=30,
                              # startangle=0,
                              counterclock=False,
                              textprops=dict(color="white"),
                              radius=1-size,
                              wedgeprops=dict(width=size, edgecolor="white"),
                              # center=(12, 5),
                              )


# Adding legend
ax.legend(wedges, sub_pie_labels,
          # ax.legend(wedges, pie1_labels,
          title="Cases",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1),
          )

# plt.setp(autotexts,
plt.setp(aut2,
         # size=8,
         size=10,
         weight="bold",
         )

# plt.setp(autotexts + aut2,
#          # size=8,
#          size=10,
#          weight="bold",
#          )
ax.set_title("Results oeis")

# show plot
plt.show()
