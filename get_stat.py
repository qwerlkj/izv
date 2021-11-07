#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

import numpy as np
import matplotlib.pyplot as plt
# povolene jsou pouze zakladni knihovny (os, sys) a knihovny numpy, matplotlib a argparse

from download import DataDownloader


def plot_stat(data_source,
              fig_location=None,
              show_figure=False):
    print("Plot stat")


# TODO pri spusteni zpracovat argumenty
if __name__ == '__main__':
    print("argparse")
    fig_location = None
    show_figure = False
    plot_stat(DataDownloader().get_dict(),fig_location, show_figure)
