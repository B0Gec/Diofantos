from urlquice import plot_fews, pre_plot_largs, plot_largs
import numpy as np
from save_new_bfiles import bseqs

def maxsf(seqs):
    return [max([abs(term) for term in seq]) for _id, seq in seqs.items()]
def lensf(seqs):
    return [len(seq) for _, seq in seqs.items()]

def pre_plot_fews(seqs):
    """Plot number of seqs with less than threshold 
    terms using seqs.
    """

    lens = lensf(seqs)
    thresholds = range(max(lens)+2)
    xs = np.array(thresholds)
    fewers = list(map(lambda thr: sum(np.array(lens)>=thr), xs))
    return xs, fewers

xs_few, fewers = pre_plot_fews(bseqs)
# plot_fews(xs, fewers)
plot_fews(xs_few, fewers, is_save=True)

xs, largs = pre_plot_largs(bseqs)
# plot_largs(xs, largs)
plot_largs(xs, largs, is_save=True)
