# -*- coding: utf-8 -*-
import argparse
import pandas as pd
import os
import geocoder
from multiprocessing.dummy import Pool
#from multiprocessing import Pool

import matplotlib.pyplot as plt
from math import log
from math import tan
from math import pi

import numpy as np
import cv2

import pickle

OUT_FILENAME = 'map.csv'

parser = argparse.ArgumentParser(description='住所から高低差地図(DEM)を取得するプログラム')
parser.add_argument('--output', default='yotsuya')
parser.add_argument('--name', default='四谷')

def main():
    save_terrain(name)


def save_terrain(address):

    ret = geocoder.osm(address, timeout=5.0)

    print ('ret',ret)
    if ret:
        zoom = 14
        x, y = latlon2tile(ret.latlng[1], ret.latlng[0], zoom)
        nabewari = (zoom, x, y) # タイル座標 (z, x, y)
        nabewari_tile = fetch_tile(*nabewari)

        with open(output + '.pkl', 'wb') as f:
            pickle.dump(np.array(nabewari_tile ,dtype='float64'), f)
        f.close()

   
def fetch_tile(z, x, y):
    url = "https://cyberjapandata.gsi.go.jp/xyz/dem/{z}/{x}/{y}.txt".format(z=z, x=x, y=y)
    print(url)
    df = pd.read_csv(url, header=None).replace("e", 0.0)
    return df.values
 
def latlon2tile(lon, lat, z):
    x = int((lon / 180 + 1) * 2**z / 2) # x座標
    y = int(((-log(tan((45 + lat / 2) * pi / 180)) + pi) * 2**z / (2 * pi))) 
    return x, y

if __name__ == "__main__":
    args = parser.parse_args()
    output = args.output
    name = args.name
    main()
