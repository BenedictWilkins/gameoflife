import numpy as np
import sys
import pygame
from pygame.locals import *

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

# kernel
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

class GameOfLife:

    def __init__(self, grid, speed = 20, screen_dim = (640, 640), colours =  np.array([[0, 0, 0], [120, 250, 90]])):

        self.grid_dim = np.array(grid.shape)
        self.screen_dim = np.array(screen_dim)
        self.colours  = colours
        self.speed = speed

        self.x = grid

        self.exit = False
        pygame.init()
        width, height = self.screen_dim
        self.screen = pygame.display.set_mode((width, height))
        self.draw(self.screen)
        

    def update(self, dt): # list for quit events
        for event in pygame.event.get():
            if event.type == QUIT:
                self.exit = True
        
    def draw(self, screen): # update the display      
        self.x =  step(self.x)
        surface = pygame.surfarray.make_surface(self.colours[self.x])
        surface = pygame.transform.scale(surface, self.screen_dim)

        screen.blit(surface, (0,0))
        pygame.display.flip()
    
    def run(self):
        fpsClock = pygame.time.Clock()
        dt = self.speed
        while not self.exit: 
            #print("UPDATE")
            self.update(dt)
            self.draw(self.screen)
            dt = fpsClock.tick(self.speed)
        
        pygame.quit()
  
grid_dim = np.array([100,100])
x = np.zeros(grid_dim, dtype=np.int8)
x[1:-1,1:-1] = np.random.randint(0, 2, size=grid_dim-2, dtype=np.int8) # random initial config

game = GameOfLife(x)

import time
time.sleep(10)

game.run()
