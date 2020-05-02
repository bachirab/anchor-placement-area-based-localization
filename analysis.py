from our_library import *
import pandas as pd
import matplotlib.pylab as plt

b_data = "TXT/brutee.txt"
fh_data = "TXT/fear_heuristic.txt"
h_data = "TXT/heuristic.txt"
g_data = "TXT/genetic.txt"
pg_data = "TXT/p_genetic.txt"
#pg_data = "TXT/P_GENETIC.TXT"


def draw_comparison(df, nb_anchors, tics, algorithms: list):
    fig, ax = plt.subplots()
    df.groupby(['nb_anchors', 'tics', 'algorithm']).min().loc[nb_anchors,:,:]['Expectation']\
        .unstack().plot.bar(ax=ax)
   # ax.legend(["Brute","Genetic","Heuristic","GGGG"])
    labels = ["2","6","12","24","48","96"]
    ax.set_xticklabels(labels)
    ax.set_xlabel("Descritization")
    ax.set_ylabel("Expected area")
#    plt.show()
    plt.savefig('IMG/accuracy_'+str(nb_anchors)+".pdf")
    fig, ax = plt.subplots()
    df.groupby(['nb_anchors', 'tics', 'algorithm']).min().loc[nb_anchors,:, :]['Time']\
        .unstack().plot.bar(log=True,ax=ax)
  #  ax.legend(["Brute","Genetic","Heuristic"])
    labels = ["2","6","12","24","48","96"]
    ax.set_xticklabels(labels)
    ax.set_xlabel("Descritization")
    ax.set_ylabel("time in (s)")
#    plt.show()
    plt.savefig('IMG/time_'+str(nb_anchors)+".pdf")


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


def draw_and_accuracy(df, nb_anchors, tics, algorithm):
    min_anchors,max_anchors = get_min_anchor(df, nb_anchors, tics, algorithm)
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


b_df = pd.read_csv(b_data, sep=";", names=["Anchors", "Expectation", "Time", "nb_anchors", "tics"])\
    .sort_values('tics', ascending=False)
fh_df = pd.read_csv(fh_data, sep=";", names=["Anchors", "Expectation", "Time", "nb_anchors", "tics"])\
    .sort_values('tics', ascending=False)
g_df = pd.read_csv(g_data, sep=";", names=["Anchors", "Expectation", "Time", "nb_anchors", "tics"])\
    .sort_values('tics', ascending=False)
pg_df = pd.read_csv(pg_data, sep=";", names=["Anchors", "Expectation", "Time", "nb_anchors", "tics"])\
    .sort_values('tics', ascending=False)
h_df = pd.read_csv(h_data, sep=";", names=["Anchors", "Expectation", "Time", "nb_anchors", "tics"])\
    .sort_values('tics', ascending=False)
b_df["algorithm"] = ["Brute force" for _ in range(len(b_df))]
fh_df["algorithm"] = ["Heuristic" for _ in range(len(fh_df))]
g_df["algorithm"] = ["Genetic" for _ in range(len(g_df))]
pg_df["algorithm"] = ["Genetic" for _ in range(len(pg_df))]
h_df["algorithm"] = ["Heuristic" for _ in range(len(h_df))]
#All_df = pd.concat([b_df, fh_df, h_df, pg_df,g_df])
All_df = pd.concat([b_df, fh_df, pg_df])


for nb_anchors_ in [3, 4, 5]:
    draw_comparison(All_df, nb_anchors=nb_anchors_, tics=96, algorithms=[])

# for algo in ["Heuristic","Brute force"]:
#     for nb_anchors_ in [5, 4, 5]:
#         for tics_ in [48,24,12,6,2]:
#             print(nb_anchors_," ",tics_)
#             draw_and_accuracy(All_df, nb_anchors=nb_anchors_, tics=tics_, algorithm=algo)

# All_df.groupby(['nb_anchors', 'tics', 'algorithm']).mean().loc[4, :12, :]['minavrg'].unstack().plot.bar()
# plt.show()
# All_df.groupby(['nb_anchors', 'tics', 'algorithm']).mean().loc[4, :12, :]['minavrg'].unstack().plot.bar()
# g_all = All_df.groupby(['nb_anchors', 'tics', 'algorithm']).mean()
#
# #All_df[(All_df.nb_anchors==3)&(All_df["algorithm"].isin(["heuristic","brute"]))].sort_values('tics',ascending=False).plot.bar(x="tics",y=["minavrg","time"])
# ax = All_df[(All_df.nb_anchors==3)&(All_df.algorithm=="fair heuristic")].plot.bar(x="tics",y=["minavrg"],subplots=True)
# gg_df.loc[(4,)].plot.bar(y=["minavrg"],ax=ax,color='red',subplots=True)
# plt.show()
#
