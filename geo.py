#!/usr/bin/python3.8
# coding=utf-8
# %%
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
import sklearn.cluster
import numpy as np


# muzete pridat vlastni knihovny
# %%

def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """ Konvertovani dataframe do geopandas.GeoDataFrame se spravnym kodovani"""
    df['p36'] = df['p36'].astype('category')
    df['p2a'] = df['p2a'].astype('datetime64')
    gdf = geopandas.GeoDataFrame(df,
                                 geometry=geopandas.points_from_xy(df['d'], df['e']),
                                 crs="EPSG:5514")
    return gdf


# %%
def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """ Vykresleni grafu s sesti podgrafy podle lokality nehody 
     (dalnice vs prvni trida) pro roky 2018-2020 """
    gdfn = gdf[(gdf['region'] == 'JHM')].to_crs("epsg:3857")
    fig, ax = plt.subplots(3, 2, figsize=(15,18))
    fig.subplots_adjust(left=0.05,
                    bottom=0.05,
                    right=0.95,
                    top=0.95,
                    wspace=0.01,
                    hspace=0.13)
    druhDict = {0: "dialnica", 1: "cesta 1. triedy"}
    color={0:"green", 1: 'red'}
    for yr in range(2018, 2021):
        for druh in range(2):
            curAx = ax[yr % 2018, druh]
            curAx.set_axis_off()
            curAx.set_xlim(1_750_000, 1_960_000)
            curAx.set_ylim(6_210_000, 6_390_000)
            curAx.set_title('JHM Kraj: {} ({})'.format(druhDict[druh], yr))
            gdfn[(gdfn['p36'] == druh) & (gdfn['p2a'].dt.year == yr)].plot(ax=curAx, markersize=1, color=color[druh])
            ctx.add_basemap(ax=curAx, crs=gdfn.crs, source=ctx.providers.Stamen.TonerLite)
    if fig_location is not None:
        fig.savefig(fig_location)
    if show_figure:
        fig.show()


# %%
def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """
    pass


# %%
if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    # %%
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    # %%
    plot_geo(gdf, "geo1.png", True)
    # %%
    plot_cluster(gdf, "geo2.png", True)
