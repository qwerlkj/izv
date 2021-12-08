#!/usr/bin/env python3.9
# coding=utf-8
# %%
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator
import pandas as pd
import seaborn as sns
import numpy as np
import os

# %%
# muzete pridat libovolnou zakladni knihovnu ci knihovnu predstavenou na prednaskach
# dalsi knihovny pak na dotaz

""" Ukol 1:
načíst soubor nehod, který byl vytvořen z vašich dat. Neznámé integerové hodnoty byly mapovány na -1.

Úkoly:
- vytvořte sloupec date, který bude ve formátu data (berte v potaz pouze datum, tj sloupec p2a)
- vhodné sloupce zmenšete pomocí kategorických datových typů. Měli byste se dostat po 0.5 GB. Neměňte však na kategorický typ region (špatně by se vám pracovalo s figure-level funkcemi)
- implementujte funkci, která vypíše kompletní (hlubkou) velikost všech sloupců v DataFrame v paměti:
orig_size=X MB
new_size=X MB

Poznámka: zobrazujte na 1 desetinné místo (.1f) a počítejte, že 1 MB = 1e6 B. 
"""


def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
    MB_IN_BYTES = 1_048_576
    df = pd.read_pickle(filename)
    before_memory = 0.0
    if verbose:
        before_memory = df.memory_usage(deep=True).sum() / MB_IN_BYTES

    df['date'] = df['p2a'].astype('datetime64[D]')
    df['p2a'] = df['p2a'].astype('datetime64[D]')
    df['p12'] = df['p12'].astype('int16')
    df['p14'] = df['p14'].astype('int32')
    df['p53'] = df['p53'].astype('int32')
    df['p37'] = df['p37'].astype('int32')
    df['p2b'] = df['p2b'].astype('int16')
    df['s'] = df['s'].astype('int32')
    df['r'] = df['r'].astype('int32')
    df['o'] = df['o'].str.replace(',', '.').replace('', np.nan).astype('float64')
    cols_i8 = ['p36', 'weekday(p2a)', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p13a', 'p13b', 'p13c',
               'p15', 'p15', 'p16', 'p17', 'p18', 'p19', 'p20', 'p21', 'p22', 'p23', 'p24', 'p27', 'p28', 'p34',
               'p35', 'p36', 'p39', 'p44', 'p45a', 'p47', 'p48a', 'p49', 'p50a', 'p50b', 'p51', 'p52', 'p55a',
               'p57', 'p58', 'p5a', 'j']
    cols_f64 = ['a', 'b', 'd', 'e', 'f', 'g']
    cols_string = ['p1', 'h', 'i', 'k', 'l', 'p', 'q', 't']

    for i8 in cols_i8:
        df[i8] = df[i8].astype('int8')
    for f64 in cols_f64:
        df[f64] = df[f64].astype('float64')
    for s in cols_string:
        dlzka = np.vectorize(len)
        df[s] = df[s].astype('U' + str(dlzka(df[s]).max()))
    if verbose:
        new_memory = df.memory_usage(deep=True).sum() / MB_IN_BYTES
        print(f"orig_size={before_memory:.1f} MB")
        print(f"new_size={new_memory:.1f} MB")

    return df


# Ukol 2: počty nehod v jednotlivých regionech podle druhu silnic

def plot_roadtype(df: pd.DataFrame, fig_location: str = None,
                  show_figure: bool = False):
    road_names = {1: "Dvojpruhová", 2: 'Trojpruhová', 3: 'Štvojpruhová',
                  4: 'Štvojpruhová', 5: 'Viacpruhová', 6: 'Rýchlostná', 0: 'Iná'}
    region = ('JHM' == df['region']) | \
             ('ZLK' == df['region']) | \
             ('PLK' == df['region']) | \
             ('VYS' == df['region'])
    dfv = df[region][['region', 'p21']].copy()
    dfv['road_count'] = np.ones(dfv['p21'].size)
    for k, v in road_names.items():
        dfv.loc[dfv['p21'] == k, 'p21'] = v
    done = dfv.groupby(["region", 'p21']).count().reset_index()
    col_order = [v for k, v in road_names.items() if k != 3]
    g = sns.catplot(data=done, x='region', col="p21", y='road_count', kind='bar', col_wrap=3, col_order=col_order)
    g.fig.tight_layout()
    g.fig.suptitle("Počet nehôd na rôznych komunikáciách.", fontsize=20)
    g.fig.subplots_adjust(top=0.9, left=0.1, right=0.95)
    g.set(xlabel='Kraj', ylabel='Počet nehôd')
    ax_number = 0
    for ax in g.axes.ravel():
        for c in ax.containers:
            labels = [f'{v.get_height():.0f}' for v in c]
            ax.bar_label(c, labels=labels, label_type='edge')
        ax.set_facecolor('#F1F1F1')
        ax.set_title(f'{col_order[ax_number]} komunikácia')
        ax_number += 1
    if fig_location is not None:
        g.fig.savefig(fig_location)
    if show_figure:
        g.fig.show()


# Ukol3: zavinění zvěří
def plot_animals(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):
    filter = (df['p58'] == 5) & (df['date'] < '2021-01-01')
    filter &= ('JHM' == df['region']) | \
              ('ZLK' == df['region']) | \
              ('PLK' == df['region']) | \
              ('VYS' == df['region'])
    df_all = df[filter].copy()
    df_fault = df_all[['region', 'p10']].copy()
    df_fault['month'] = df_all['date'].dt.month

    fault = {1: 'vodič', 2: 'vodič', 4: 'zver', 3: 'iné', 5: 'iné', 6: 'iné', 7: 'iné', 0: 'iné'}
    for k, v in fault.items():
        df_fault.loc[df_fault['p10'] == k, 'p10'] = v

    df_fault['count'] = np.ones(df_fault['p10'].size)
    print(df_fault.dtypes)
    done = df_fault.groupby(['region', 'p10', 'month']).count().reset_index()
    col_order = ['JHM', 'PLK', 'VYS', 'ZLK']
    g = sns.catplot(data=done, x='month', hue='p10', col="region",
                    y='count', kind='bar', col_wrap=2, col_order=col_order,
                    hue_order=['zver', 'vodič', 'iné'], aspect=1.5)
    g.set(xlabel='Mesiac', ylabel='Počet nehôd')
    g._legend.set_title("Zavinenie")
    ax_number = 0
    for ax in g.axes.ravel():
        ax.set_facecolor('#F1F1F1')
        ax.set_axisbelow(True)
        ax.yaxis.grid(color="lightgray")
        ax.set_title(f'Kraj: {col_order[ax_number]}')
        ax_number += 1
    if fig_location is not None:
        g.fig.savefig(fig_location)
    if show_figure:
        g.fig.show()


# Ukol 4: Povětrnostní podmínky
def plot_conditions(df: pd.DataFrame, fig_location: str = None,
                    show_figure: bool = False):
    filter = (df['p18'] != 0) & (df['date'] < '2021-01-31')
    REGIONS = ['JHM', 'ZLK', 'PLK', 'VYS']
    region_filter = None
    for reg in REGIONS:
        if region_filter is not None:
            region_filter |= (reg == df['region'])
        else:
            region_filter = (reg == df['region'])
    filter &= region_filter
    df_all = df[filter]
    df_cond = df_all[['region', 'date', 'p18']].copy()
    conds = {1: 'nesťažené', 2: 'Hmla', 4: 'na začiatku dažďa',
             3: 'dážď', 5: 'sneženie', 6: 'námraza', 7: 'nárazový vietor'}
    for k, v in conds.items():
        df_cond.loc[df_cond['p18'] == k, 'p18'] = v
    df_cond['count'] = np.ones(df_cond['p18'].size)

    df_grouped = df_cond.groupby(['region', 'p18', pd.Grouper(key='date', axis=0, freq='M')]).count().reset_index()

    fig, ax = plt.subplots(2, 2, sharey=True, sharex=True, figsize=(15, 8))
    date_format = DateFormatter('%m/%y')
    for y in range(2):
        for x in range(2):
            sns.lineplot(ax=ax[x, y], data=df_grouped[df_grouped['region'] == REGIONS[y * 2 + x]],
                         legend=True, x='date', y='count', hue='p18')
            ax[x, y].set_title(f'Kraj: {REGIONS[y * 2 + x]}')
            ax[x, y].grid(color="white")
            ax[x, y].set_facecolor('#F1F1F1')
            ax[x, y].xaxis.set_major_formatter(date_format)
            ax[x, y].spines['bottom'].set_position(('data', 0))
            ax[x, y].set_xlim(df_grouped['date'].min(), df_grouped['date'].max())
            ax[x, y].set_xticks(pd.date_range(df_grouped['date'].min(), df_grouped['date'].max(), freq="12M"))
            ax[x, y].legend().set_visible(False)
            if x == len(ax) - 1:
                ax[x, y].set_xlabel("Dátum")
            if y == 0:
                ax[x, y].set_ylabel("Počet nehôd")
    lines, labels = ax[0, 0].get_legend_handles_labels()
    fig.legend(lines, labels,
               loc="center right",
               borderaxespad=0.1,
               title="Podmienky"
               )
    fig.subplots_adjust(right=0.85, left=0.07)
    if fig_location is not None:
        fig.savefig(fig_location)
    if show_figure:
        fig.show()


if __name__ == "__main__":
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni ¨
    # funkce.
    df = get_dataframe("accidents.pkl.gz", True)
    plot_roadtype(df, fig_location="01_roadtype.png", show_figure=True)
    plot_animals(df, "02_animals.png", True)
    plot_conditions(df, "03_conditions.png", True)
