import numpy as np
import matplotlib.pyplot as plt

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
    gr.corrected_non_manual,
    gr.all_fails,
    ]

sub_pie = [
    gr.id_oeis,
    gr.non_id,
    gr.corrected_non_manual,
    gr.fail,
    gr.jobs_fail,
    ]




# Creating dataset
# labels = ['AUDI', 'BMW', 'FORD', 'TESLA', 'JAGUAR', 'MERCEDES']
labels = pie1_labels

# data = [23, 17, 35, 29, 12, 41]
data = pie1

if len(data) != len(labels):
    raise IndexError

# Creating autocpt arguments
def func(pct, allvalues):
    absolute = int(pct / 100. * np.sum(allvalues))
    return "{:d}\n({:1.1f} %)".format(absolute, pct)

# Creating plot
fig, ax = plt.subplots(figsize=(14, 5))

wedges, texts, autotexts = ax.pie(data,
                      autopct=lambda pct: func(pct, data),
                      labels=labels,
                      startangle=90,
                      counterclock=False,
                      textprops=dict(color="white"),
                      wedgeprops=dict(edgecolor="white"),
                      )

# Adding legend
ax.legend(wedges, labels,
          title="Cases",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1),
          )

plt.setp(autotexts,
         # size=8,
         size=10,
         weight="bold",
         )

ax.set_title("Results oeis")
fig.tight_layout()
fig.savefig("results_oeis_overwritten.png")  # , bbox_inches='tight', pad_inches=0)
# show plot
plt.show()

