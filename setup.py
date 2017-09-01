# -*- coding: utf-8 -*-

import glob
import os
from codecs import open  # To use a consistent encoding

from setuptools import setup, find_packages  # Always prefer setuptools over distutils

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def doc_files():
    result = {}
    for root, dirs, files in os.walk("doc"):
        target_dir = os.path.join("share/doc/python-snakes", *root.split(os.sep)[1:])
        for name in files:
            if target_dir not in result:
                result[target_dir] = []
            result[target_dir].append(os.path.join(root, name))
    return list(result.items())


def abcd_resources():
    collected = ["*.txt", "*.html", "*.css", "*.js", "*.png", "*.jpg"]
    result = []
    for pattern in collected:
        for path in glob.glob("snakes/utils/abcd/resources/" + pattern):
            result.append(os.path.join("resources", os.path.basename(path)))
    return result


setup(
    name="snakes-py3",
    version="0.9.17",
    description="SNAKES is the Net Algebra Kit for Editors and Simulators",
    long_description=long_description,
    author="Franck Pommereau",
    author_email="franck.pommereau@ibisc.univ-evry.fr",
    maintainer="Franck Pommereau",
    maintainer_email="franck.pommereau@ibisc.univ-evry.fr",
    url="http://http://www.ibisc.univ-evry.fr/~fpommereau/SNAKES/",
    scripts=[
        "bin/abcd", "bin/snkc", "bin/snkd"
    ],
    packages=find_packages(),
    package_data={
        "snakes.utils.abcd": abcd_resources()
    },
    data_files=doc_files(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',cd
    ],
)
