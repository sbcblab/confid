#Bruno Iochins Grisci and Marcelo D. Poleto
#APRIL/2019
#http://sbcb.inf.ufrgs.br/confid
# -*- coding:utf-8 -*-

print('Checking for needed packages and libs...')

try:
    import os
    print('OK: os')
except:
    print('ERROR: could not import os')
try:
    import sys
    print('OK: sys')
except:
    print('ERROR: could not import sys')
try:
    import pprint
    print('OK: pprint')
except:
    print('ERROR: could not import pprint')
try:
    import re
    print('OK: re')
except:
    print('ERROR: could not import re')
try:
    import numpy as np
    print('OK: numpy')
except:
    print('ERROR: could not import numpy')
try:
    import operator
    print('OK: operator')
except:
    print('ERROR: could not import operator')
try:
    from collections import Counter
    print('OK: Counter from collections')
except:
    print('ERROR: could not import Counter from collections')
try:
    from itertools import imap
    print('OK: imap from itertools')
except:
    print('ERROR: could not import imap from itertools')

print('Checking for optional packages and libs...')

try:
    import graphviz
    print('OK: graphviz')
except:
    print('WARNING: could not import graphviz')
    print('WARNING: graphviz is needed if PLOT_GRAPH is True.')
try:
    import matplotlib.pyplot as plt
    print('OK: matplotlib.pyplot')
except:
    print('WARNING: could not import matplotlib.pyplot')
    print('WARNING: matplotlib.pyplot is needed if TIME_DEPENDENT_STATS is True.')

print('Finished.')
