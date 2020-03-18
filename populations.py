#Bruno Iochins Grisci and Marcelo D. Poleto
#FEBRUARY/2018
#http://sbcb.inf.ufrgs.br/confid
# -*- coding:utf-8 -*-

import os
import sys
import numpy as np
import re

class pops:
    def __init__(self, data_file_name, folder_name, window_len, window, fp=20.0, fv=50.0):
        self.data_file_name = data_file_name
        self.folder_name = folder_name
        self.fp = fp
        self.fv = fv

        angles = []
        dists  = []
        with open(self.data_file_name, 'r') as df:
            for line in df:
                if '#' in line or '@' in line or '-180' in line:
                    pass
                else:
                   l = line.split()
                   angles.append(int(l[0]))
                   dists.append(float(l[1]))

        self.data_file_name = data_file_name.replace('Dihedrals/', '')

        angles = np.array(angles)
        dists = np.array(dists)

        min_value_index = np.argmin(dists)
        translation = np.array([360]*min_value_index + [0]*(angles.size - min_value_index))
        angles = angles + translation

        sorter = np.argsort(angles)
        s = self.smooth(dists[sorter], window_len, window)

        peaks = self.find_peaks(s)
        pk = np.zeros(angles.size)
        for i in peaks:
            pk[i] = s[i]

        valleys = self.find_valleys(s)
        vl = np.zeros(angles.size)
        for i in valleys:
            vl[i] = np.max(s)/4.0

        self.regions = self.get_regions(peaks, valleys, angles[sorter])
        self.peaks = angles[sorter][peaks]
        for p in range(len(self.peaks)):
            if self.peaks[p] > 180.0:
                self.peaks[p] -= 360.0
            elif self.peaks[p] < -180.0:
                self.peaks[p] += 360.0

        self.save(self.data_file_name.replace('.xvg', 'shift'),   self.folder_name,  angles[sorter], dists[sorter])
        self.save(self.data_file_name.replace('.xvg', 'smooth'),  self.folder_name,  angles[sorter], s)
        self.save(self.data_file_name.replace('.xvg', 'peaks'),   self.folder_name,  angles[sorter], pk)
        self.save(self.data_file_name.replace('.xvg', 'valleys'), self.folder_name,  angles[sorter], vl)

    def smooth(self, x, window_len, window):
        if x.ndim != 1:
            raise ValueError("Smooth only accepts 1 dimension arrays.")
        if x.size < window_len:
            raise ValueError("Input vector needs to be bigger than window size.")
        if window_len<3:
            return x
        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
            raise ValueError("Window must be one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")
        s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
        #print(len(s))
        if window == 'flat': #moving average
            w=np.ones(window_len,'d')
        else:
            w=eval('np.'+window+'(window_len)')
        y=np.convolve(w/w.sum(),s,mode='valid')
        y_neighbours = int(np.floor(window_len/2))
        return y[y_neighbours:-y_neighbours]

    def find_peaks(self, distribution):
        peaks = []
        for i in range(1, distribution.size-1):
            if (distribution[i] > distribution[i-1] and distribution[i] > distribution[i+1] and distribution[i] >= (np.max(distribution)/self.fp)):
                peaks.append(i)

        if (len(peaks) <= 0):
            raise Exception('\nERROR: No peaks were found! Try using a larger FP (>{}) to solve the problem.\n'.format(self.fp))
        return peaks

    def find_valleys(self, distribution):
        valleys = []
        for i in range(1, distribution.size-1):
            if (distribution[i] <= distribution[i-1] and distribution[i] <= distribution[i+1]) or distribution[i] <= np.max(distribution)/self.fv:
                valleys.append(i)

        if (len(valleys) <= 0):
            raise Exception('\nERROR: No valleys were found! Try using a lower FV (<{}) to solve the problem.\n'.format(self.fv))
        return valleys

    def get_regions(self, peaks, valleys, angles):
        regions = []
        for p in peaks:
            try:
                start = max([v for v in valleys if v < p])
            except:
                start = 0
            try:
                end   = min([v for v in valleys if v > p])
            except:
                end   = -1
            if angles[start] <= 180 and angles[end] <= 180:
                regions.append((angles[start], angles[end]))
            if angles[start] > 180  and angles[end] > 180:
                regions.append((angles[start]-360, angles[end]-360))
            if angles[start] <= 180 and angles[end] > 180:
                regions.append((-180, angles[end]-360, angles[start], 180))
        return regions

    def save(self, file_name, folder_name, angles, dists):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        with open(folder_name + file_name+'.xvg', 'w') as of:
            of.write(re.sub(r' *\n *', '\n', np.array_str(np.c_[angles, dists]).replace('[', '').replace(']', '').strip()))
        #print('Saved file {}'.format(folder_name + file_name))
