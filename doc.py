import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np


def get_alcohol_graph(df, show_figure=False, fig_location=None):
    """Graf poctu percent v krajoch, kedy pri nehode vodic bol pod vplyvom alkoholu."""
    df2 = df[df['p57'] != -1]
    alco_ret = df2.copy()

    alco = df2[['region']].copy()
    alco['alco'] = ((df2['p57'] == 4) | (df2['p57'] == 5)).astype('bool')
    alco_ret['alco'] = alco['alco']
    alco['count'] = np.ones(alco['region'].size).astype('int')
    alco = alco.groupby(['region', 'alco']).count().reset_index()
    regions = alco['region'].unique()
    alco = alco.set_index('region')
    for r in regions:
        alco.loc[r, 'aperc'] = alco.loc[r, 'count'] * 100 / alco.loc[r, 'count'].sum()
    fig, ax = plt.subplots()
    ax.grid(axis='y', linestyle='--')
    ax.set_axisbelow(True)
    sb.barplot(data=alco[alco['alco']], x=regions, y='aperc', ax=ax, color="g")
    ax.set(xlabel='Kraj', ylabel='Vodič pod vplyvom alkoholu (v %)')
    ax.set_title("Percentuálny počet nehôd, kedy vodič bol pod vplyvom alkoholu")
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    fig.tight_layout()
    if fig_location is not None:
        fig.savefig(fig_location)
    if show_figure:
        fig.show()
    return alco_ret


def get_alcohol_data(df):
    """Vypise tabulku poctu rozdielnych stavov vodica, zameranych na nameranu hladinu alkoholu v krvi vodica"""
    df2 = df[['region', 'p57', 'alco']].copy()
    regions = df2['region'].unique()
    states = ['pod 1‰', '1‰ a viac', 'iný stav']
    df2.rename(columns={'alco': 'count', 'p57': 'state'}, inplace=True)
    df2.loc[~df2['count'], 'state'] = 'iný stav'
    df2.loc[df2['state'] == 4, 'state'] = 'pod 1‰'
    df2.loc[df2['state'] == 5, 'state'] = '1‰ a viac'
    df2['state'] = df2['state'].astype('category')
    df2 = df2.groupby(['region', 'state']).count()

    print("Kraj;vodič pod vplyvom do 1‰;vodič pod vplyvom 1‰ a viac;vodič bol v inom stave")
    for r in regions:
        print(r, end=';')
        for s in states:
            print(df2.loc[(r, s), 'count'], end=';' if s != states[-1] else '\n')


def get_stats(df):
    """Vypise zakladne statistiky o stave vodiča a počte nehôd"""
    stav = df['p57'] != -1
    alco = (df['p57'] == 4) | (df['p57'] == 5)
    pocet_znamy_stav = df[stav]['p1'].count()
    print("Celkový počet nehôd:\t\t\t\t\t\t\t\t\t\t{}".format(df['p1'].count()))
    print("Celkový počet nehôd, kde je známy stav vodiča:\t\t\t\t{}".format(pocet_znamy_stav))
    print("Celkový počet nehôd, kde je neznámy stav vodiča:\t\t\t{}".format(df[~stav]['p1'].count()))
    print("Celkový počet nehôd, kde je prítomný alkohol u vodiča:\t\t{}".format(df[alco]['p1'].count()))
    print("Celkové percento nehôd, kde je prítomný alkohol u vodiča:\t{}".format(df[alco]['p1'].count() * 100/pocet_znamy_stav))
    print("Celkový počet nehôd, kde nie je prítomný alkohol u vodiča:\t{}".format(df[(~alco) & stav]['p1'].count()))


if __name__ == "__main__":
    data = pd.read_pickle("accidents.pkl.gz")
    alco_set = get_alcohol_graph(data, False, 'fig.png')
    get_alcohol_data(alco_set)
    get_stats(data)
