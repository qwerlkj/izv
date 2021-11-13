#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os.path

import matplotlib.colors as colors
from matplotlib.ticker import FixedFormatter, FixedLocator
import numpy as np
import matplotlib.pyplot as plt
# povolene jsou pouze zakladni knihovny (os, sys) a knihovny numpy, matplotlib a argparse

from download import DataDownloader


def plot_stat(data_source,
              fig_location=None,
              show_figure=False):
    """
    Funkcia, ktora vizualizuje pocty nehod
    Args:
        data_source: np_array
        fig_location: cesta k suboru, do ktoreho ulozi vysledok (obrazok) alebo None
        show_figure: True|False, True ak chcete zobrazit vysledok
    """
    x = list(DataDownloader.regions.values())
    y = np.arange(6)
    y_labels = ['žiadna úprava', 'prerušovaná žltá',
                'nejde semafor', 'dopravné značky',
                'prenosné značky', 'nevyznačené']
    x_labels = list(DataDownloader.regions.keys())
    z_data = np.empty((len(x), 6), "int64")
    c = 0
    # Spocitat pocet nehod pre kraj, na dany typ.
    for _id in x:
        count = np.bincount(data_source[np.char.startswith(data_source['p1'], _id, start=0, end=2)]['p24'], minlength=6)
        z_data[c] = count
        c += 1
    z_data = z_data.T

    fig, ax = plt.subplots(2, 1, figsize=(8, 5.67))
    fig.tight_layout()

    ax[0].set_title("Absolútne")
    cmap_a = plt.get_cmap("viridis").copy()
    cmap_a.set_under("white")
    mesh = ax[0].pcolormesh(x, y, z_data, shading='auto', norm=colors.LogNorm(), cmap=cmap_a)
    ax[0].xaxis.set_major_locator(FixedLocator(np.arange(len(x))))
    ax[0].xaxis.set_major_formatter(FixedFormatter(x_labels))
    ax[0].yaxis.set_major_locator(FixedLocator(y))
    ax[0].yaxis.set_major_formatter(FixedFormatter(y_labels))
    cb1 = fig.colorbar(mesh, ax=ax[0])
    cb1.set_label("Počet nehôd")

    ax[1].set_title("Relatívne voči príčine")
    mesh = ax[1].pcolormesh(x, y,
                            (z_data.T / z_data.sum(axis=1)).T * 100,
                            shading='auto',
                            cmap=plt.get_cmap('plasma'))
    ax[1].xaxis.set_major_locator(FixedLocator(np.arange(len(x))))
    ax[1].xaxis.set_major_formatter(FixedFormatter(x_labels))
    ax[1].yaxis.set_major_locator(FixedLocator(y))
    ax[1].yaxis.set_major_formatter(FixedFormatter(y_labels))
    cb2 = fig.colorbar(mesh, ax=ax[1], ticks=[0, 20, 40, 60, 80, 100])
    cb2.set_label("Podiel nehôd pre danú príčinu [%]")
    cb2.ax.set_yticklabels([0, 20, 40, 60, 80, 100])
    fig.subplots_adjust(left=0.21, top=0.9, bottom=0.1, hspace=0.4)

    if (fig_location is not None) and (fig_location != ""):
        path = fig_location.split('/')[:-1]
        finalPath = ""
        for p in path:
            finalPath += p
            if not os.path.exists(finalPath):
                os.mkdir(finalPath)
            finalPath += "/"
        fig.savefig(fig_location)
    if show_figure:
        plt.show(block=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Definujte ci chcete statistiku ulozit alebo zobrazit.')
    parser.add_argument('--fig_location', nargs='?', default=None, action='store',
                        help='Cesta vratane nazvu suboru kam chcete ulozit statistiku.')
    parser.add_argument('--show_figure', dest='show_figure', action='store_true',
                        help='ak definujete prepinac, tak ')

    args = parser.parse_args()
    plot_stat(DataDownloader().get_dict(), args.fig_location, args.show_figure)
