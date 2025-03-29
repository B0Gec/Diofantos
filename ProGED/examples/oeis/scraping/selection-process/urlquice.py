import matplotlib.pyplot as plt

import saved_core
# import saved_core110up as saved_core
seqs = saved_core.core_list
seqs_unflatten = saved_core.core_unflatten

def basic_info_of_list(seqs_list=seqs):
    # # print(len(list(set(seqs))))
    # # print(seqs)
    # print("number of packets of seqs", len(seqs_unflatten))
    # print("number of seqs in seqs:", sum(len(tseqs) for tseqs in seqs_unflatten))
    # print("unique ids:")
    ids = [seq[0] for seq in seqs]
    print("numbers of all saved sequences:", len(ids))
    print("all distinct id saved:", len(list(set(ids))))
    print("last 4 seqs in seqs:", seqs[-4:])
    return
# basic_info_of_list()

## -- remove seq A000035 -- ##
def remove_seqs_of_list(seqs_to_remove=["A000035"], seqs_list=seqs):
    seqs = seqs_list
    print("Removing seqs by hand ... ")
    seqs_dict = dict(seqs)
    print("number of seqs (before removing):", len(list(seqs_dict)))
    # seqs_dict = dict(seqs_flat)
    # seqs_to_remove = ["A000035"]
    seqr = seqs_to_remove[0]
    print("no error?", seqs_dict[seqr])
    print("is the seq inside before removing:", seqs_to_remove[0] in seqs_dict)
    [seqs_dict.pop(seq, None) for seq in seqs_to_remove]
    print("is seq inside after removing:", seqs_to_remove[0] in seqs_dict)
    print("number of seqs (now):", len(list(seqs_dict)))
    # print(seqs_dict)
    # print("error?", seqs_dict[seqr])
    return seqs_dict
# remove_seqs_of_list()

## --- Length of sequence analisis: --- ##
import numpy as np
def thresholds_amount_manys(seqs=seqs):
    # result = 0
    # for ten_seqs in seqs:
    #     result += 10
    #     print(f"in results: {result-10}-{result}")
    #     print(len(ten_seqs))
    # for seq_pair in seqs_flat:
    #     print("number of terms in sequence:", len(seq_pair[1]))
    # print(np.mean(np.array([len(seq_pair[1]) for seq_pair in seqs_flat])))
    lens = np.array([len(seq_pair[1]) for seq_pair in seqs])
    lens = [len(seq) for _id, seq in seqs]
    lens.sort()
    # print("lens sorted:", lens)

    # print(sum(lens<10))
    # for i in range(10):
    #     print(sum(lens<10*i), 10*i)
    # print(len(lens))
    thresholds = np.arange(max(lens))
    lens = np.array(lens)
    amount_manys = list(map(lambda i: sum(lens>=i), thresholds))
    # print(bigs)
    return thresholds, amount_manys
thresholds, amount_manys = thresholds_amount_manys()

## -- check those with more than 100 terms -- ##
def more_than_cents(seqs_dict=dict(seqs)):
    print("100lens")
    # cents = [(seq[0], len(seq[1]), seq[1]) for seq in seqs if len(seq[1])>100]
    ids_cents = [id for id in seqs_dict if len(seqs_dict[id])>=23]
    # print(cents, "cents")
    ids_cents.sort()
    print(ids_cents)
    print("number of sequences lots", len(ids_cents))
    return ids_cents
# ids_lots = more_than_cents()

## -- check those with terms bigger than 1e16 -- ##
# seqs = seqs_flat
def bigger_than_1e16(seqs_dict=dict(seqs), verbose=True):
    if verbose:
        print("big numbers")
    # largs = [(seq[0], len(seq[1]), seq[1]) for seq in seqs if max(seq[1])>1e16]
    # ids_largs = [seq[0] for seq in seqs if max(seq[1])<=1e16.5]
    ids_largs = [id for id in seqs_dict if max(seqs_dict[id])<=10**(15.6)]
    ids_largs.sort()
    # print(largs, "largs")
    if verbose:
        print(ids_largs)
        print("number of sequences large w/ numbers", len(ids_largs))
    return ids_largs
# ids_largs = bigger_than_1e16()
# assert check_centum() == pick_bignum(), "they do not perfectly match"

## -- new metric (sum of digits) -- ##
def metric(seq):
    # print("calculating metric of the seq")
    # print(seq)
    # print([str(an) for an in seq])
    # print([2+len(str(an)) for an in seq])
    return sum([1+len(str(an)) for an in seq])
# print("some metric:", metric(seqs_dict["A005036"]))

def metric_analysis(seqs_dict=dict(seqs)):
    metrics = [metric(seqs_dict[seq]) for seq in seqs_dict]
    metrics_bounds = (min(metrics), max(metrics))
    print(metrics_bounds)
    metrics_dict = {} 
    for i in metrics:
        if str(i) in metrics_dict:
            metrics_dict[str(i)] += 1
        else:
            metrics_dict[str(i)] = 1
    print(metrics_dict)
    metric_histo = [metrics_dict.get(str(long), 0) 
        for long in range(metrics_bounds[0], metrics_bounds[1])]
    # metric_histo = [long
    #     for long in range(metrics_bounds[0], metrics_bounds[1]+1)]
    print(metric_histo)
    return
# metric_analysis()

def plot_metric(xs, ys):
    plt.title("metric(length)")
    plt.ylabel("metric")
    plt.xlabel("length")
    plt.plot(xs, ys)
    plt.show()
    return
# plot_metric(np.arange(min(metrics), max(metrics)), metric_histo)

## -- new metric's lots -- ##
keyword_more = ("A000109", "A000112", "A000609", "A002106", "A003094", "A005470", "A006966")
def metrics_lots(seqs_dict=dict(seqs)):
    metrics = [metric(seqs_dict[seq]) for seq in seqs_dict]
    find_threshold = [sum(np.array(metrics)<=threshold)<=137 
        for threshold in range(min(metrics), max(metrics))]
    threshold = min(metrics) + sum(find_threshold)
    print("threshold found:", threshold)
    metric_dict = {}
    [metric_dict.update({i:seqs_dict[i]}) 
        for i in seqs_dict if metric(seqs_dict[i])<=threshold]
    print(len(metric_dict))
    print(sum(np.array(metrics)<=threshold))
    ids_metrics = [i for i in seqs_dict if metric(seqs_dict[i])<=threshold]
    ids_metrics = [i for i in seqs_dict if metric(seqs_dict[i])>=250]
    print("high metric", ids_metrics)
    ids_metrics_spec = [i for i in seqs_dict if metric(seqs_dict[i]) in range(0, 195)]
    ids_metrics_spec = list(set(ids_metrics_spec).difference(set({})))
    print(len(ids_metrics_spec), ids_metrics_spec)
    ids_metrics_spec = list(set(ids_metrics_spec).difference(set(keyword_more)))
    print(len(ids_metrics_spec), ids_metrics_spec)
    nice_ids = [(i, metric(seqs_dict[i]), len(seqs_dict[i])) for i in ids_metrics_spec]
    print(len(nice_ids), nice_ids)
    print(min(metrics), max(metrics))

    # print("all metrics: \nthresh: metric: 300 terms: 23 max term: 1e16\n")
    # for i in seqs_dict:
    #     seq = seqs_dict[i]
    #     print(i, "metric:", metric(seq), "terms:", len(seq), "max term:", "{0:e}".format(max(seq)))
# metrics_lots()

def intersectium(seqs_dict=dict(seqs)):
    ids_largs = bigger_than_1e16(seqs_dict, verbose=False)
    ids_lots = more_than_cents(seqs_dict)
    inter = set(ids_largs).intersection(set(ids_lots))
    print("intersection:", inter, "len(intersection) : ", len(list(inter)))
    dif_lots = set(ids_lots).difference(inter)
    dif_largs = set(ids_largs).difference(inter)
    print(len(dif_lots))
    print(len(dif_largs))
    # inter_metric = set(inter).intersection(set(ids_metrics))
    # print("inter \cap ids_metrics", len(inter_metric))


    print("\n\n")
    for i in [(id, 
                len(dict(seqs)[id]), 
                float(max(dict(seqs)[id])), 
                metric(seqs_dict[id]),
                dict(seqs)[id],
                ) for id in dif_lots]:
        print(i)
    print("\n\n")
    for i in [(id, 
                len(dict(seqs)[id]), 
                "{0:e}".format(float(max(dict(seqs)[id]))), 
                metric(seqs_dict[id]),
                dict(seqs)[id]) for id in dif_largs]:
        print(i)
    # print(seqs[:3], "seqs")
    # print(dict(seqs[:3]))
    return
# intersectium()

## -- checkout ids_largs -- ##
def checkout_ids_largs(seqs_dict=dict(seqs)):
    ids_largs = bigger_than_1e16(seqs_dict, verbose=False)
    # ids_lots = more_than_cents(seqs_dict)
    # inter = set(ids_largs).intersection(set(ids_lots))

    largs2 = [len(seqs_dict[i]) for i in ids_largs]
    # print(seqs_dict)
    print("number of enough terms", len(ids_largs))
    largs2.sort()
    print(largs2, "largs2")
    # print(ids_largs, "ids_largs")
    largs_max = min([len(seqs_dict[i]) for i in ids_largs])
    print(largs_max, "largs_max")
    return
# checkout_ids_largs()

def pre_plot_nomores(seqs_dict=dict(seqs), verbose=True):
    ids_largs = bigger_than_1e16(seqs_dict, verbose=False)
    ids_largs_nomore = list(set(ids_largs).difference(set(keyword_more)))
    if verbose:
        print("largs nomore:", len(ids_largs_nomore))
    largs_nomore = [len(seqs_dict[i]) for i in ids_largs_nomore]
    largs_nomore.sort()
    if verbose:
        print(largs_nomore)
    nomores = list(set(seqs_dict.keys()).difference(set(keyword_more)))
    nomores_lens = [len(seqs_dict[i]) for i in nomores]
    nomores_lens.sort()
    if verbose:
        print("nomores lens:", nomores_lens)
    return nomores_lens, largs_nomore
# plot nomores lens:
nomores_lens, largs_nomore = pre_plot_nomores(verbose=False)
thresholds_nomores = np.arange(max(nomores_lens))
amount_manys_nomores = list(map(lambda i: sum(nomores_lens>=i), thresholds))
# plot largs_nomores:
thresholds_largs_nomores = np.arange(max(largs_nomore))
amount_manys_largs_nomores = list(map(lambda i: sum(largs_nomore>=i), thresholds_largs_nomores))


# plot largs:
def pre_plot_largs(seqs_dict=dict(seqs)):
    maxs = np.array([max([abs(term) for term in seq]) for _, seq in seqs_dict.items()])
    # xs = np.array([10**i for i in range(int(np.log10(max(maxs))))])
    # xs = [10**i for i in range(int(np.log10(max(maxs))))]
    xs = np.array([float(10**i) for i in range(1, 30)])
    # xs = np.array([i for i in range(1, 300)])
    # nums = 10**xs
    max_exp = sum(xs < max(maxs))
    xs = xs[:max_exp]#[::-1]
    # xs = float(xs)
    # xs = xs[:15]
    # # print(max_exp, max(maxs))
    # print(np.log10(max(maxs)))
    largs = list(map(lambda x: sum(maxs<=x), xs))
    # largs = list(map(lambda x: x, xs))
    # largs = list(map(lambda x: x**2, xs))
    # xs = (-1)*xs
    # print(xs)
    return xs, largs

def plot_largs(xs, largs, is_save=False, filename="plot_largs"):
    fig, ax = plt.subplots()
    # plt.grid(True)
    plt.xlabel("size [int]")
    plt.ylabel("number of sequences with largest absolute term smaller than *threshold* (x)")
    ax.plot(xs, largs)
    print(len(xs))
    ax.set_xscale("log", base=10)
    ax.set_xlim(float(xs[-1]), xs[0])
    # ax.xaxis.set_major_locator(MultipleLocator(45*(xs[-1]-xs[0])/len(xs)))
    # ax.xaxis.set_major_formatter('{x:.0f}')
    # ax.xaxis.set_minor_locator(MultipleLocator(4*(xs[-1]-xs[0])/len(xs)))
    # ax.xaxis.set_minor_locator(xs)
    # ax.xaxis.set_minor_locator(AutoMinorLocator())
    min_mult = 3
    # ax.set_xticks(xs[::3], minor=True)
    ax.set_xticks(xs[::], minor=True)
    # ax.set_xticks(xs[::5*3])
    plt.xticks(xs[::3])
    # ax.set_yticks(np.array(list(set(largs[::10]))))
    # ax.set_yticks(np.array(list(set(largs[::2]))), minor=True)
    ax.set_yticks(np.arange(0, largs[-1], 20))
    ax.set_yticks(np.arange(0, largs[-1], 5), minor=True)
    # tle tuki
    print(np.array(list(set(largs[::10]))))
    # ax.xaxis.grid(True, which="minor")
    ax.axes.grid(True, which="minor")
    # ax.xaxis.grid(True, which="major", color="k", linewidth=1)
    ax.axes.grid(True, which="major", color="k", linestyle="-", linewidth=1)
    # ax.xaxis.grid(True)
    # ax.tick_params(which='both', width=2)
    ax.tick_params(which='major', length=5, width=1)
    ax.tick_params(which='minor', length=2, color='r')
    # plt.plot(xs, largs)
    # plt.xscale("symlog", base=10)
    # plt.xscale("log", base=10)
    # ax.xscale("log", base=10)  # Not working
    # plt.xscale("log", base=1.2)
    # plt.xlim(xs[-1], xs[0])
    # plt.xlim(min(xs)-1, max(xs)+1)
    # print(float(xs[-1]))
    # plt.xlim(0, float(xs[-1]))
    # plt.xlim(float(xs[-1]), xs[0])
    # plt.xlim(0, 10**100)
    # plt.xlim(0, 1e99)
    # plt.xlim(0, 1e99)
    # plt.xlim(10*100, 0)
    # plt.title("Sequences with small enough terms")
    # plt.xticks(xs[::3])
    # plt.yticks(np.array(set(largs[::10])))
    # plt.yticks([i for i in range(1, 178, 10)])
    plt.get_current_fig_manager().window.state('zoomed')  # works (all on windows)
    # mng.resize(*mng.window.maxsize())  #works (kinda)
    # mng.full_screen_toggle()     # works kinda  
    # mng.window.showMaximized()    dont work
    # mng.frame.Maximize(True)      dont work
    plt.show()
    if is_save:
        fig.savefig(filename)
    return
# xs, largs = pre_plot_largs(dict(seqs))
# plot_largs(xs, largs)

def plot_fews(xs, ys, is_save=False, filename="plot_fews"):
    fig, ax = plt.subplots()
    ax.plot(xs, ys)
    ax.set_xticks(np.arange(0, xs[-1], 10))
    ax.set_xticks(np.arange(0, xs[-1], 20/10), minor=True)
    ax.set_yticks(np.arange(0, max(ys), 25))
    ax.set_yticks(np.arange(0, max(ys), 5), minor=True)
    ax.axes.grid(True, which="minor")
    ax.axes.grid(True, which="major", color="k", linestyle="-", linewidth=1)
    ax.set_xlabel("threshold")
    ax.set_ylabel("number of sequences with more than *threshold* terms")
    ax.set_title("Sequences with enough terms")
    plt.get_current_fig_manager().window.state('zoomed')  # works (all on windows)
    plt.show()
    if is_save:
        fig.savefig(filename)
    return
# plot_fews(thresholds, amount_manys)
# plot_fews(thresholds_nomores, amount_manys_nomores)
# plot_fews(thresholds_largs_nomores, amount_manys_largs_nomores)

def plot_alot(x, bigs):
    plt.grid(True)
    plt.xlabel("threshold")
    plt.ylabel("number of sequences with more than *threshold* terms")
    plt.plot(x, bigs)
    plt.title("Sequences with enough terms")
    plt.show()
    return
# plot_alot(x, bigs)  # not updated
## EOF lengths analysis ##
