#Bruno Iochins Grisci and Marcelo D. Poleto
#APRIL/2019
#http://sbcb.inf.ufrgs.br/confid
# -*- coding:utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import os
import sys
import pprint
import numpy as np
try:
    from itertools import imap
except ImportError:
    imap=map
import matplotlib.pyplot as plt

def assing_function(value):
    value = value.lower()
    f = None
    if value == 'sum':
        f = np.sum
    elif value == 'max':
        f = np.max
    elif value == 'min':
        f = np.min
    elif value == 'aver':
        f = np.average
    elif value == 'std':
        f = np.std
    elif value == 'median':
        f = np.median
    elif value == 'count':
        f = len
    else:
        raise Exception('ERROR: Unidentified function: {}\n'.format(value))
    return f

def main(input_file, fun1, fun2, POP_ID=None):

    f1 = assing_function(fun1)
    f2 = assing_function(fun2)

    stay   = {}
    last_t = 0.0

    with open(input_file, 'r') as inp:
        for line in inp:
            l = line.rstrip()
            l = l.replace('->',    ';')
            l = l.replace('| t =', ';')
            v = [x.strip() for x in l.split(';')]
            v[2] = float(v[2])
            if v[0] in stay:
                stay[v[0]].append(v[2] - last_t)
            else:
                stay[v[0]] = []
                stay[v[0]].append(v[2] - last_t)
            last_t = v[2]

    result = []
    x = []
    y = []
    l = []
    max_k_len = max(imap(len, stay))

    if POP_ID != None:
        keys = list(POP_ID.keys())
        for k in keys:
            POP_ID[str(k)] = POP_ID.pop(k)

    for k in stay:
        stay[k] = np.array(stay[k])
        if POP_ID != None:
            pid = POP_ID[k]
            s = 'P#{:4d} {:{mkl}s}: # sum: {:8.1f} # max: {:8.1f} # min: {:8.1f} # aver: {:8.3f} # std: {:8.3f} # median: {:8.3f} # count: {:8d}'.format(pid, k, stay[k].sum(), stay[k].max(), stay[k].min(), stay[k].mean(), stay[k].std(), np.median(stay[k]), len(stay[k]), mkl=max_k_len)
        else:
            s = '{:{mkl}s}: # sum: {:8.1f} # max: {:8.1f} # min: {:8.1f} # aver: {:8.3f} # std: {:8.3f} # median: {:8.3f} # count: {:8d}'.format(k, stay[k].sum(), stay[k].max(), stay[k].min(), stay[k].mean(), stay[k].std(), np.median(stay[k]), len(stay[k]), mkl=max_k_len)
        result.append((f1(stay[k]), f2(stay[k]), s))

        x.append(f1(stay[k]))
        y.append(f2(stay[k]))
        l.append(k)

    result.sort(reverse=True)

    with open(input_file.replace('.txt', '-Time_Stats-{}X{}.txt'.format(fun1, fun2)), 'w') as sf:
        for r in result:
            print(r[2])
            sf.write(r[2]+'\n')

    with open(input_file.replace('.txt', '-Time_Stats-{}X{}.xvg'.format(fun1, fun2)), 'w') as sc:
        sc.write("# " + fun1 + "          " + fun2 + "\n")
        for r in result:
            sc.write(str(r[0]).ljust(15,' '))
            sc.write(str(r[1]).ljust(15,' '))
            sc.write('\n')

    try:
        fig, ax = plt.subplots()
        ax.scatter(x, y)

        plt.title(input_file)
        plt.xlabel(fun1)
        plt.ylabel(fun2)
        plt.savefig(input_file.replace('.txt', '-Time_Stats-{}X{}.png'.format(fun1, fun2)))
        plt.cla()
        plt.clf()
        plt.close()
        del ax
        del fig
    except Exception as e: 
        print('ERROR while rendering time stats plots.')
        print(e)
