import numpy as np
import sys
import pygame
from pygame.locals import *

import grid

class GameOfLife:

    def __init__(self, grid_dim = (500,500), speed=20, screen_dim = (1000, 1000)):
        self.speed = speed
        self.grid_dim = np.array(grid_dim)
        self.colours = colors = np.array([[0, 0, 0], [120, 250, 90]])
        self.screen_dim = np.array(screen_dim)
        self.x = np.zeros(grid_dim, dtype=np.int8)
        
        #self.x[1:-1,1:-1] = np.random.randint(0, 2, size=self.grid_dim-2, dtype=np.int8) # random initial config
        #self.x[1:-1,1:-1] = np.random.choice([0,1], size=self.grid_dim-2, p=[0.9,0.1]).astype(np.int8) # random initial config
        n = 100
        self.x[n:-n,n:-n] = np.random.choice([0,1], size=self.grid_dim-2*n, p=[0.9,0.1]).astype(np.int8)

        pygame.init()

    def update(self, dt):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit() 
        
    def draw(self, screen):
        self.x =  grid.step(self.x)
        surface = pygame.surfarray.make_surface(self.colours[self.x])
        surface = pygame.transform.scale(surface, self.screen_dim)  # Scaled a bit.
        screen.blit(surface, (0,0))
        pygame.display.flip()
    
    def run(self):
        fpsClock = pygame.time.Clock()
        width, height = self.screen_dim
        screen = pygame.display.set_mode((width, height))
     
        dt = self.speed
        while True: 
            #print("UPDATE")
            self.update(dt)
            self.draw(screen)
            dt = fpsClock.tick(self.speed)

GameOfLife(grid_dim=(500,500)).run()