#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 31-10-2020 16:20:57

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

from setuptools import setup, find_packages

setup(name='gameoflife',
      version='0.0.1',
      description='',
      url='',
      author='Benedict Wilkins',
      author_email='benrjw@gmail.com',
      packages=find_packages(),
      install_requires=["numpy", "pygame"],
      zip_safe=False)

# NOTE: opencv requires ffmpeg


