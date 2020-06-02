from our_library import *
import pandas as pd
import matplotlib.pylab as plt

b_data = "TXT/brutee.txt"
fh_data = "TXT/heuristic.txt"
g_data = "TXT/genetic.txt"
pg_data = "TXT/p_genetic.txt"
ppg_data = "TXT/evolution.txt"
color = ['green', 'blue', 'red']


# plotting evolution of time or expectation
def plot_complexity(df, axis=None, nb_anchors=3, c='blue', value='Time'):
    if axis == None:
        df_m = df[df.nb_anchors == nb_anchors].groupby(['ngen'])[value].agg(['mean', 'std'])
        ax = df_m.plot(y='mean', c=c)
        plt.fill_between(df_m.index[:], df_m['mean'].values - df_m['std'].values,
                         df_m['mean'].values + df_m['std'].values,
                         color=c, alpha=0.2)
    else:
        df_m = df[df.nb_anchors == nb_anchors].groupby(['ngen'])[value].agg(['mean', 'std'])
        ax = df_m.plot(y='mean', c=c, ax=axis)
        plt.fill_between(df_m.index[:], df_m['mean'].values - df_m['std'].values, df_m['mean'].values + df_m['std'].values,
                         color=c, alpha=0.2)
    return ax


# plot the bars for to for every configuration
def draw_comparison(df, nb_anchors):
    fig, ax = plt.subplots()
    df_t = df.groupby(['nb_anchors', 'tics', 'algorithm']).agg(["mean", "std"]).loc[nb_anchors, :, :]['Expectation']\
        .unstack()
    df_t = df_t.sort_values('tics', ascending=False)
    df_t.plot.bar(y='mean', yerr='std', ax=ax, edgecolor='black')
    labels = ['96', '48', '24', '12', '6', '2']
    ax.set_xticklabels(labels)
    ax.set_xlabel("Descritization")
    ax.set_ylabel("Expected area")
    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which='major', linestyle=':', linewidth='0.5', color='blue')
    plt.show()
    plt.savefig('IMG/accuracy_'+str(nb_anchors)+".pdf")
    fig, ax = plt.subplots()
    df_t = df.groupby(['nb_anchors', 'tics', 'algorithm']).min().loc[nb_anchors, :, :]['Time'].unstack()
    df_t = df_t.sort_values('tics', ascending=False)
    df_t.plot.bar(log=True, ax=ax, edgecolor='black')
    ax.set_xticklabels(labels)
    ax.set_xlabel("Descritization")
    ax.set_ylabel("time in (s)")
    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which='major', linestyle=':', linewidth='0.5', color='blue')
#    plt.show()
    plt.savefig('IMG/time_'+str(nb_anchors)+".pdf")


# the anchor which have the min avrg
def get_min_anchor(df, nb_anchors, tics, algorithm="pgenetic"):
    tmp_df = df[(df.nb_anchors == nb_anchors) & (df.tics == tics) & (df.algorithm == algorithm)]
    if len(tmp_df) == 0:
        return None, None
    if algorithm not in ["genetic", "pgenetic"]:
        anchor = eval(tmp_df["Anchors"].values[0])
        return anchor, anchor
    tmp_max = tmp_df[tmp_df.Expectation == tmp_df.Expectation.max()]
    tmp_df = tmp_df[tmp_df.Expectation == tmp_df.Expectation.min()]
    anchor = eval(tmp_df["Anchors"].values[0])
    return anchor, eval(tmp_max["Anchors"].values[0])


# draw simulation area and cdf
def draw_and_accuracy(df, nb_anchors, tics, algorithm):
    min_anchors, max_anchors = get_min_anchor(df, nb_anchors, tics, algorithm)
    l = getAllSubRegions(anchors_=min_anchors)
    res = getDisjointSubRegions(l)
    avgRA = getExpectation(res)
    entr, px_ = get_entropy(res)
    drawNetwork(min_anchors, res, nb_anchors_=nb_anchors, tics_=tics, algo_=algorithm)
#    s = pd.Series(px_)
#    s.plot.kde()
#    plt.show()
#    s.plot.hist(cumulative=True)
#    plt.show()
    return avgRA, entr


# Reading data from csv files
b_df = pd.read_csv(b_data, sep=";", names=["Anchors", "Expectation", "Time", "nb_anchors", "tics"])\
    .sort_values('tics', ascending=False)
fh_df = pd.read_csv(fh_data, sep=";", names=["Anchors", "Expectation", "Time", "nb_anchors", "tics"])\
    .sort_values('tics', ascending=False)
g_df = pd.read_csv(g_data, sep=";", names=["Anchors", "Expectation", "Time", "nb_anchors", "tics"])\
    .sort_values('tics', ascending=False)
pg_df = pd.read_csv(pg_data, sep=";", names=["Anchors", "Expectation", "Time", "nb_anchors", "tics"])\
    .sort_values('tics', ascending=False)
ppg_df = pd.read_csv(ppg_data, sep=";", names=["nb_anchors", "ngen", "Expectation", "Time"])\
    .sort_values('ngen', ascending=True)

# creating Dataframes
b_df["algorithm"] = ["Brute force" for _ in range(len(b_df))]
fh_df["algorithm"] = ["Heuristic" for _ in range(len(fh_df))]
g_df["algorithm"] = ["Genetic" for _ in range(len(g_df))]
pg_df["algorithm"] = ["Genetic" for _ in range(len(pg_df))]
All_df = pd.concat([b_df, fh_df, pg_df])
# Drawing complexity
ax = plot_complexity(ppg_df, c='blue', nb_anchors=3,value='Time')
ax = plot_complexity(ppg_df, axis=ax, c='red', nb_anchors=4, value='Time')
ax = plot_complexity(ppg_df, axis=ax, c='green', nb_anchors=5, value='Time')
ax.set_axisbelow(True)
ax.minorticks_on()
ax.grid(which='major', linestyle=':', linewidth='0.5', color='black')
ax.set_xlabel("Generation")
ax.set_ylabel("Expected area")
legend = ['3 anchors', '4 anchors', '5 anchors']
plt.legend(legend)
ax.set_xlabel("Generation")
ax.set_ylabel("Time (s)")
#plt.show()
plt.savefig('./IMG/timecomplexity.pdf')

for nb_anchors_ in [3, 4, 5]:
    draw_comparison(All_df, nb_anchors=nb_anchors_)


# plt.show()

# plotting the simulation area and cdf
# for algo in ["Heuristic","Brute force"]:
#     for nb_anchors_ in [5, 4, 5]:
#         for tics_ in [48,24,12,6,2]:
#             print(nb_anchors_," ",tics_)
#             draw_and_accuracy(All_df, nb_anchors=nb_anchors_, tics=tics_, algorithm=algo)
