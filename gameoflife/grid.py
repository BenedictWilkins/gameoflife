#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 31-10-2020 16:38:46

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

import numpy as np


k = np.ones((3,3), dtype=np.int8)

def window(x, shape=(3,3)):
    s = (x.shape[0] - shape[0] + 1,) + (x.shape[1] - shape[1] + 1,) + shape
    strides = x.strides + x.strides
    r = np.lib.stride_tricks.as_strided(x, shape=s, strides=strides, )
    return r.reshape(r.shape[0] * r.shape[1], *r.shape[2:])

def step(x1):
    global k
    
    size = np.array(x1.shape)
    w = window(x1)
    k = k.reshape(-1)
    w = w.reshape(w.shape[0], -1)

    x2 = np.zeros_like(x1)
    x2[1:-1,1:-1] = np.dot(w, k).reshape(size-2)
    x2 = np.abs(((x2 - 3) * 2) - x1)
    return (x2 == x1).astype(np.int8)








