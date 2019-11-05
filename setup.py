import setuptools
import os
import sys
import shutil
import pprint
import re
import numpy
import operator
import collections 
import timeit
import pyparsing
import graphviz
import pydot
import matplotlib
import itertools

import check_dep
import count_populations
import count_stay
import aver2dist
import populations
import confid_help

with open("README.md", "r") as fh:
    long_description = fh.read()

os.system("dot -c")

setuptools.setup(
    name="confid",
    version="1.2.0",
    license="LGPL-3.0",
    author="Marcelo D. Poleto; Bruno Iochins Grisci; Marcio Dorn; Hugo Verli",
    author_email="bigrisci@inf.ufrgs.br",
    description="ConfID: an analytical method for conformational characterization of small molecules using molecular dynamics trajectories.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sbcblab/confid",
    packages=setuptools.find_packages(),
    py_modules=["check_dep","count_populations","count_stay","aver2dist","populations", "confid_help"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: LGPL-3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    scripts=["confID.py"]
)
