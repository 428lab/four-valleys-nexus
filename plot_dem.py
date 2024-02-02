import matplotlib.pyplot as plt
#plt.rcParams['font.family'] = 'IPAexGothic'
from matplotlib import animation
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TKAgg')


import sys
import pandas as pd
from scipy.interpolate import griddata
import argparse
#import terrain_csv
import math
import cv2
import os

#print( plt.rcParams['font.family'] )

from matplotlib.font_manager import FontProperties



font_path = '/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'
font_prop = FontProperties(fname=font_path)
matplotlib.rcParams['font.family'] = font_prop.get_name()

import glob
import pickle

#from pympler.tracker import SummaryTracker
#tracker = SummaryTracker()


def read_csv(file_name):
    df = pd.read_csv(file_name)
    return df

class PlotMap:
    def __init__(self):
        self.fig = plt.figure(figsize=(6*2,4*2))
        self.ax0 = self.fig.add_subplot(121, projection='3d')
        self.ax1 = self.fig.add_subplot(122, aspect='equal')

    def plot_map(self, title, img):
        self.fig.suptitle(title)

        rows, cols = img.shape
        x = np.arange(cols)
        y = np.arange(rows)
        z = img.copy()

        X, Y = np.meshgrid(x, y)

        self.ax0.plot_surface(X, Y, z, cmap=cm.gist_earth, linewidth=0, antialiased=False)
        self.ax1.contourf(X, Y, z, cmap=cm.gist_earth)

        # スケールを統一するためのリミット設定
        max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), z.max()-z.min()]).max() / 2.0

        mid_x = (X.max()+X.min()) * 0.5
        mid_y = (Y.max()+Y.min()) * 0.5
        mid_z = (z.max()+z.min()) * 0.5

        self.ax0.set_xlim(mid_x - max_range, mid_x + max_range)
        self.ax0.set_ylim(mid_y - max_range, mid_y + max_range)
        self.ax0.set_zlim(mid_z - max_range, mid_z + max_range)

    def close(self):
        self.fig.clear()
        plt.close()
        plt.cla()
        plt.clf()
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parameters')
    parser.add_argument('-pkl-file', dest='pkl_file', type=str, help='DEM pkl file', default='yotsuya.pkl')
    parser.add_argument('-out-img', dest='out_img', type=str, help='output png file', default='yotsuya.png')
    params = parser.parse_args()

    pkl_file = params.pkl_file
    out_img = params.out_img

    title = '四谷'
   
    with open(pkl_file, 'rb') as f:
        img = pickle.load(f) 

    plot = PlotMap()
    plot.plot_map(title, img)

    plt.show()

    plot.close()

