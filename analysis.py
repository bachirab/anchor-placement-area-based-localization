from our_library import *
import pandas as pd
import matplotlib.pylab as plt

b_data = "TXT/brute.txt"
fh_data = "TXT/fear_heuristic.txt"
h_data = "TXT/heuristic.txt"
g_data = "TXT/genetic.txt"
pg_data = "TXT/p_genetic.txt"

worst = [[0,0],[0,192],[192,192]]
l = getAllSubRegions(anchors_=[(0, 96), (96, 0), (96, 96), (192, 96)])
res = getDisjointSubRegions(l)
drawNetwork(worst, res, mode_="ss")
avgRA = getExpectation(res)
entr, px_ = get_entropy(res)
print(avgRA, entr)
input()

def draw_comparison(df, nb_anchors, tics, algorithms: list):
    df.groupby(['nb_anchors', 'tics', 'algorithm']).mean().loc[nb_anchors,:,:]['Expectation']\
        .unstack().plot.bar()
    plt.show()
    df.groupby(['nb_anchors', 'tics', 'algorithm']).mean().loc[nb_anchors,:12, :]['Time']\
        .unstack().plot.bar()
    plt.show()


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
    drawNetwork(min_anchors, res, nb_anchors_=nb_anchors, tics_=tics, algo_=algorithm, mode_="ss")
    s = pd.Series(px_)
    s.plot.kde()
    plt.show()
    s.plot.hist(cumulative=True, density=True)
    plt.show()
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
fh_df["algorithm"] = ["fair heuristic" for _ in range(len(fh_df))]
g_df["algorithm"] = ["Genetic" for _ in range(len(g_df))]
pg_df["algorithm"] = ["pgenetic" for _ in range(len(pg_df))]
h_df["algorithm"] = ["Heuristic" for _ in range(len(h_df))]
All_df = pd.concat([b_df, fh_df, h_df, pg_df,g_df])

for nb_anchors_ in [3, 4, 5]:
    draw_comparison(All_df, nb_anchors=nb_anchors_, tics=96, algorithms=[])

draw_and_accuracy(All_df, nb_anchors=3, tics=96, algorithm="pgenetic")

draw_and_accuracy(All_df, nb_anchors=3, tics=96, algorithm="Brute force")

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
