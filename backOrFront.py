#!/usr/bin/env python
# coding: utf-8
# n-dimensional arrays
import numpy as np
# plotting lib, imported this way to prevent a bug on Mac
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# import figure like that to prevent memory leak
# see https://stackoverflow.com/a/12300012
from matplotlib import figure
# because pandas are cool
import pandas as pd
# to read the image
import skimage
import skimage.io
# to measure properties of the regions
from skimage.measure import regionprops
# to smooth the curves
from scipy.signal import savgol_filter
# to threshold images
import mahotas as mh
# to get the biggest region
from operator import attrgetter
# to use *.tif
import glob
# to export as csv
import csv
# to get the filename
import os
# to detect OS
import platform
# for peak detection
import peakutils
#from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory


def getMiddleLine(img):
    index = round(len(img)/2)
    return img[round(len(img)/2)], index


#folder = askdirectory()
folder = 'mean-cells'
tifFiles = folder + os.sep + '*.tif'

# create directory for output
meanDir = folder + os.sep + 'mean'
if not os.path.exists(meanDir):
    os.makedirs(meanDir)

for fileNb, file in enumerate(glob.iglob(tifFiles, recursive=True)):
    img = skimage.io.imread(file)
    fileName = os.path.basename(file)

    mean = img.mean(axis=0)

    fig = figure.Figure()
    w=10
    h=12
    fig = plt.figure(figsize=(8, 8))
    columns = 1
    rows = 4

    fig.add_subplot(rows, columns, 1)
    plt.imshow(img)
    plt.title("Mean cell (" + fileName + ")")

    fig.add_subplot(rows, columns, 2)
    plt.imshow(img, cmap='gist_ncar')
    plt.title("Mean cell with gist_ncar cmap")

    # PLOT THE MEAN
    fig.add_subplot(rows, columns, 3)
    plt.title("Mean curve")
    plt.plot(mean)
    plt.title("Mean curve (" + fileName + ")")
    #ax.set_ylim(30000, mean.max() + 100)

    # PLOT ONLY THE MIDDLE LINE
    fig.add_subplot(rows, columns, 4)
    middleLine, index = getMiddleLine(img)
    plt.plot(middleLine)
    plt.title("Middle line [" + str(index) + "] (" + fileName + ")")

    # split image in two
    splits = np.array_split(img, 2, axis=1)

    # use a ratio of std deviation to see if front/back
    stdRatio = np.std(splits[0]) / np.std(splits[1])

    if stdRatio > 1:
        text = "Actin is at the back"
    else:
        text = "Actin is at the front"

    # display the stdRatio along the title
    text += " " + str(round(stdRatio, 3))
    # add super title
    plt.suptitle(text, fontsize=16)

    # adjust layout for the suptitle
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    # save png file
    out = meanDir + os.sep + fileName + '-figure.png'
    fig.savefig(out, dpi=300)
