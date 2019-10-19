#Bruno Iochins Grisci and Marcelo D. Poleto
#APRIL/2019
#http://sbcb.inf.ufrgs.br/confid
# -*- coding:utf-8 -*-

def check(print_ok=False):

    if print_ok:
        print('Checking for needed packages and libs...')

    try:
        import os
        if print_ok:
            print('OK: os')
    except:
        print('ERROR: could not import os')
    try:
        import sys
        if print_ok:
            print('OK: sys')
    except:
        print('ERROR: could not import sys')
    try:
        import pprint
        if print_ok:
            print('OK: pprint')
    except:
        print('ERROR: could not import pprint')
    try:
        import re
        if print_ok:
            print('OK: re')
    except:
        print('ERROR: could not import re')
    try:
        import numpy as np
        if print_ok:
            print('OK: numpy')
    except:
        print('ERROR: could not import numpy')
    try:
        import operator
        if print_ok:
            print('OK: operator')
    except:
        print('ERROR: could not import operator')
    try:
        from collections import Counter
        if print_ok:
            print('OK: Counter from collections')
    except:
        print('ERROR: could not import Counter from collections')
    try:
        import timeit
        if print_ok:
            print('OK: timeit')
    except:
        print('ERROR: could not import timeit')  
    if not (sys.version_info >= (3, 0)):
        try:
            from itertools import imap
            if print_ok:
                print('OK: imap from itertools')
        except:
            print('WARNING: could not import imap from itertools, if using Python 3.x ignore this warning')

    if print_ok:
        print('Checking for optional packages and libs...')

    try:
        import graphviz
        if print_ok:
            print('OK: graphviz')
    except:
        print('WARNING: could not import graphviz')
        print('WARNING: graphviz is needed if PLOT_GRAPH is True.')
    try:
        import pydot
        if print_ok:
            print('OK: pydot')
    except:
        print('WARNING: could not import pydot')
        print('WARNING: pydot is needed if PLOT_GRAPH is True.')        
    try:
        import matplotlib.pyplot as plt
        if print_ok:
            print('OK: matplotlib.pyplot')
    except:
        print('WARNING: could not import matplotlib.pyplot')
        print('WARNING: matplotlib.pyplot is needed if TIME_DEPENDENT_STATS is True.')
    if print_ok:
        print('Finished.')

if __name__ == '__main__':
    check(print_ok=True)