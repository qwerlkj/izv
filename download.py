#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import gzip
import io
import pickle
import time

import numpy as np
import zipfile
import re
from bs4 import BeautifulSoup
import requests
import os


# Kromě vestavěných knihoven (os, sys, re, requests …) byste si měli vystačit s: gzip, pickle, csv, zipfile, numpy, matplotlib, BeautifulSoup.
# Další knihovny je možné použít po schválení opravujícím (např ve fóru WIS).


class DataDownloader:
    """ TODO: dokumentacni retezce 

    Attributes:
        headers    Nazvy hlavicek jednotlivych CSV souboru, tyto nazvy nemente!  
        regions     Dictionary s nazvy kraju : nazev csv souboru
    """

    headers = ["p1", "p36", "p37", "p2a", "weekdayp2a", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13a",
               "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p27",
               "p28", "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53",
               "p55a", "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "n", "o", "p", "q", "r",
               "s", "t", "p5a"]

    valid_headers = ["p1", "p36", "p37", "p2a", "weekdayp2a", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12",
                     "p13a", "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23",
                     "p24", "p27", "p28", "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b",
                     "p51", "p52", "p53", "p55a", "p57", "p58", "d", "e", "p5a"]
    valid_cols = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                  28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 47, 48, 63]
    headers_types = {
        "p1": "<U14", "p36": "int8", "p37": "int8", "p2a": "<U12", "weekdayp2a": "int8", "p2b": "<U6", "p6": "int8",
        "p7": "int8", "p8": "int8", "p9": "int8", "p10": "int8", "p11": "int8", "p12": "int16", "p13a": "int8",
        "p13b": "int8", "p13c": "int8", "p14": "int8", "p15": "int8", "p16": "int8", "p17": "int8", "p18": "int8",
        "p19": "int8", "p20": "int8", "p21": "int8", "p22": "int8", "p23": "int8", "p24": "int8", "p27": "int8",
        "p28": "int8", "p34": "int8", "p35": "int8", "p39": "int8", "p44": "int8", "p45a": "int8", "p47": "int8",
        "p48a": "int8", "p49": "int8", "p50a": "int8", "p50b": "int8", "p51": "int8", "p52": "int8", "p53": "int8",
        "p55a": "int8", "p57": "int8", "p58": "int8", "a": "float", "b": "float", "d": "float", "e": "float",
        "f": "float", "g": "float", "h": "str", "i": "str", "j": "str", "k": "str", "l": "str", "n": "str", "o": "str",
        "p": "str", "q": "str", "r": "str", "s": "str", "t": "str", "p5a": "int8"
    }

    regions = {
        "PHA": "00",
        "STC": "01",
        "JHC": "02",
        "PLK": "03",
        "ULK": "04",
        "HKK": "05",
        "JHM": "06",
        "MSK": "07",
        "OLK": "14",
        "ZLK": "15",
        "VYS": "16",
        "PAK": "17",
        "LBK": "18",
        "KVK": "19",
    }

    fetched_regions = {}

    def __init__(self, url="https://ehw.fit.vutbr.cz/izv/", folder="data", cache_filename="data_{}.pkl.gz"):
        self._url = url
        self._folder = folder
        self._cache_filename = cache_filename

    def download_data(self):
        page = requests.get(self._url)
        htmlParser = BeautifulSoup(page.text, 'html.parser')
        if not os.path.isdir(self._folder):
            os.mkdir(self._folder)

        for button in htmlParser.find_all('button'):
            download_uri = re.search(r'download\(\'(.*?)\'\)', button.get('onclick'), flags=re.DOTALL).group(1)
            filename = re.search(r'[.*/](.*?.zip)', download_uri).group(1)

            print('Downloading:', filename)

            downloaded_file = requests.get(self._url + download_uri, stream=True)
            with open(os.path.join(self._folder, filename), 'wb') as f:
                for data in downloaded_file.iter_content(512):
                    f.write(data)

            print('Completed download:', filename)

    def parse_region_data(self, region):
        """PARSE REGION"""
        if not os.path.isdir(self._folder) or not os.listdir(self._folder):
            self.download_data()
        result_data = []
        idchecker = {}
        for file in os.listdir(self._folder):
            path = os.path.join(self._folder, file)
            if zipfile.is_zipfile(path):
                with zipfile.ZipFile(path, 'r') as f:
                    with f.open(self.regions[region] + '.csv', 'r') as region_file:
                        np_file = csv.reader(region_file.read().decode('cp1250').split('\n'), delimiter=';')
                        for row in np_file:
                            if len(row) > 0 and not idchecker.get(row[0]):
                                idchecker[row[0]] = True
                                newRow = '+@+'.join(row).replace(';','-')
                                newRow = newRow.split('+@+')
                                result_data.append('"' + '";"'.join(newRow) + '"')
        del idchecker
        unique_data = np.genfromtxt(result_data, dtype=None,
                                    usecols=self.valid_cols, delimiter=';',
                                    encoding='cp1250', names=self.valid_headers)
        dt = unique_data.dtype.descr
        index = 0
        for h_key in self.valid_headers:
            indexes_int = []
            indexes_float = []
            if np.issubdtype(unique_data[h_key].dtype, np.str):
                unique_data[h_key] = np.char.strip(unique_data[h_key], '"')
            if self.headers_types[h_key] == "int8" or self.headers_types[h_key] == "int16":
                if np.issubdtype(unique_data[h_key].dtype, np.str):
                    unique_data[h_key][(unique_data[h_key] == '')] = '-1'
                    for x in range(len(unique_data[h_key])):
                        try:
                            int(unique_data[h_key][x])
                        except Exception as e:
                            indexes_int.append(x)

            elif self.headers_types[h_key] == "float":
                unique_data[h_key] = np.char.replace(unique_data[h_key], ',', '.')
                unique_data[h_key][unique_data[h_key] == ''] = np.nan
                for x in range(len(unique_data[h_key])):
                    try:
                        float(unique_data[h_key][x])
                    except Exception as e:
                        indexes_float.append(x)
            unique_data[h_key][indexes_int] = '-1'
            unique_data[h_key][indexes_float] = np.nan
            dt[index] = (dt[index][0], self.headers_types[h_key])
            index += 1

        dt = np.dtype(dt)
        unique_data = unique_data.transpose()
        unique_data = unique_data.astype(dt)
        return unique_data

    def get_dict(self, regions=None):
        regs = regions
        if regions is None or len(regions) == 0:
            regs = self.regions.keys()

        return_regions = None
        for reg in regs:
            print('Fetching region ', reg, '...')
            starttime = time.time()
            if reg in self.fetched_regions.keys():
                continue
            elif os.path.exists(os.path.join(self._folder, self._cache_filename.format(reg))):
                with gzip.open(os.path.join(self._folder, self._cache_filename.format(reg)), 'rb') as region_file:
                    self.fetched_regions[reg] = pickle.load(region_file, encoding='cp1250')
            else:
                self.fetched_regions[reg] = self.parse_region_data(reg)
                with gzip.open(os.path.join(self._folder, self._cache_filename.format(reg)), 'wb') as region_file:
                    pickle.dump(self.fetched_regions[reg], region_file)
            print("Region ", reg, " -> ", time.time() - starttime)
            if return_regions is None:
                return_regions = self.fetched_regions[reg]
            else:
                return_regions = np.append(return_regions, self.fetched_regions[reg])

        return return_regions


# TODO vypsat zakladni informace pri spusteni python3 download.py (ne pri importu modulu)
if __name__ == '__main__':
    """Print Informations"""
    dd = DataDownloader()
    regions = ['PLK', 'JHM' ,'VYS']
    data = dd.get_dict(regions)
    # TODO ake su stlpce vypisat!!!
    for reg in regions:
        print("-------------------------------")
        print("Region:", reg)
        this_region_data = data[np.char.startswith(data['p1'], dd.regions[reg], start=0, end=2)]
        print("Pocet zaznamov pre region: ", this_region_data.size)
    print("Celkovy pocet zaznamov:", len(data))
