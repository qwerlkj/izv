#!/usr/bin/env python3.9
# coding=utf-8
# %%
from matplotlib import pyplot as plt
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

# %%
MB_IN_BYTES = 1_048_576


def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
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
    df['o'] = df['o'].str.replace(',','.').replace('', np.nan).astype('float64')
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


# %%

# Ukol 2: počty nehod v jednotlivých regionech podle druhu silnic

def plot_roadtype(df: pd.DataFrame, fig_location: str = None,
                  show_figure: bool = False):
    pass


# Ukol3: zavinění zvěří
def plot_animals(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):
    pass


# Ukol 4: Povětrnostní podmínky
def plot_conditions(df: pd.DataFrame, fig_location: str = None,
                    show_figure: bool = False):
    pass


if __name__ == "__main__":
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni ¨
    # funkce.
    # %%
    df = get_dataframe("accidents.pkl.gz", True)  # tento soubor si stahnete sami, při testování pro hodnocení bude existovat
    types = df.dtypes
    # %%
    plot_roadtype(df, fig_location="01_roadtype.png", show_figure=True)
    # %%
    plot_animals(df, "02_animals.png", True)
    plot_conditions(df, "03_conditions.png", True)
