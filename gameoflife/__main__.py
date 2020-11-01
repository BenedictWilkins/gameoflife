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

        self.pause = True
        self.mouse_position = np.array([0,0])
        self.mouse_down = False
       
        

    def update(self, dt): # list for quit events
        events =  pygame.event.get()
        i = self.mouse_position
        for event in events:
            if event.type == QUIT:
                self.exit = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause

            elif self.mouse_down and event.type == pygame.MOUSEMOTION:
                i = (np.array(event.pos) // (self.screen_dim / self.grid_dim)).astype(np.int64)
                if np.any(i != self.mouse_position):
                    self.mouse_position = i
                    self.x[i[0],i[1]] = 1 - self.x[i[0],i[1]]


            elif event.type == pygame.MOUSEBUTTONDOWN:
                i = (np.array(event.pos) // (self.screen_dim / self.grid_dim)).astype(np.int64)
                self.mouse_position = i
                self.x[i[0],i[1]] = 1 - self.x[i[0],i[1]]
                self.mouse_down = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False

        if not self.pause:
            self.x =  step(self.x)
           
        
    def draw(self, screen): # update the display      
        surface = pygame.surfarray.make_surface(self.colours[self.x])
        surface = pygame.transform.scale(surface, self.screen_dim)
        screen.blit(surface, (0,0))
        pygame.display.flip()
        
    def run(self):
        fpsClock = pygame.time.Clock()
        dt = self.speed
        while not self.exit: 
            self.update(dt)
            self.draw(self.screen)
            dt = fpsClock.tick(self.speed)

        pygame.quit()
  
grid_dim = np.array([100,100])
x = np.zeros(grid_dim, dtype=np.int8)
#x[1:-1,1:-1] = np.random.randint(0, 2, size=grid_dim-2, dtype=np.int8) # random initial config

game = GameOfLife(x)
game.run()
