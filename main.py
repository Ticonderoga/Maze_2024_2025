#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 15:34:15 2024

@author: phil
"""

import time
import pygame
import networkx as nx
import random

pygame.init()  # Initialise pygame

# Permet de gérer la vitesse du jeu
clock = pygame.time.Clock()
FPS = 60

# pygame.display Permet de nommer la fenetre, voir ses dimensions, parametres d'initialisation
pygame.display.set_caption("Informatique L2")
HEIGHT = 720
WIDTH = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))

colors = [
    "#8FBCBB", # light green
    "#88C0D0", # light blue
    "#81A1C1", # darker blue
    "#5E81AC", # darkest blue
    "#BF616A", # red
    "#D08770", # orange
    "#EBCB8B", # yellow
    "#A3BE8C", # green
    "#B48EAD", # magenta
]

player_img = pygame.image.load("./assets/mower_icon2_small.png")

class Maze():
    def __init__(self,nb_cells_x=15,nb_cells_y=10):
        self.nb_cells_x = nb_cells_x
        self.nb_cells_y = nb_cells_y
        self.nb_cells = self.nb_cells_x * self.nb_cells_y
        self.dx = WIDTH // nb_cells_x
        self.dy = HEIGHT // nb_cells_y
        self.graph = nx.grid_2d_graph(self.nb_cells_x, self.nb_cells_y)
        self.init_cell = (0,0)
        self.current_cell = self.init_cell
        self.stack = []
        
        for cell in self.graph.nodes :
            self.setcell(cell, 'top', cell[1]*self.dy )
            self.setcell(cell, 'bottom',  (cell[1]+1)*self.dy)
            self.setcell(cell, 'left', cell[0]*self.dx)
            self.setcell(cell, 'right', (cell[0]+1)*self.dx)
            self.setcell(cell, 'visited', False)
        
        for e in self.graph.edges :
            self.graph.edges[e]['path'] = False
            
            
    def getcell(self,cell,attr) :
        return self.graph.nodes[cell][attr]
    
    def setcell(self,cell,attr,value):
        self.graph.nodes[cell][attr]=value
            
    def drawcell(self,cell,color) :
        # wall_thickness = 2
        pygame.draw.rect(screen, color, [self.getcell(cell,'left')+2, self.getcell(cell,'top')+2,
                           self.dx-2, self.dy-2], width=0)
        
    def draw(self):
        # wall_thickness = 2
        for path in self.graph.edges :
            start_cell, end_cell = path
            if not self.graph[start_cell][end_cell]['path'] :
                # a path with a False means a wall that will block the passage from
                # start_cell to end_cell
                if (start_cell[0] == end_cell[0]) and (start_cell[1] > end_cell[1]): 
                    # blocked along the y axis and start_cell below end_cell 
                    pygame.draw.line(screen, colors[2], (self.getcell(start_cell, 'left'), self.getcell(start_cell, 'top')), 
                                                (self.getcell(start_cell, 'right'), self.getcell(start_cell, 'top')), width=2)
                elif (start_cell[0] == end_cell[0]) and (start_cell[1] < end_cell[1]): 
                    # blocked along the y axis and start_cell above end_cell
                    pygame.draw.line(screen, colors[2], (self.getcell(start_cell, 'left'), self.getcell(start_cell, 'bottom')), 
                                                (self.getcell(start_cell, 'right'), self.getcell(start_cell, 'bottom')), width=2)
                elif (start_cell[0] > end_cell[0]) and (start_cell[1] == end_cell[1]): 
                    # blocked along the x axis and start_cell on the right of end_cell
                    pygame.draw.line(screen, colors[2], (self.getcell(start_cell, 'left'), self.getcell(start_cell, 'top')), 
                                                (self.getcell(start_cell, 'left'), self.getcell(start_cell, 'bottom')), width=2)
                elif (start_cell[0] < end_cell[0]) and (start_cell[1] == end_cell[1]): 
                    # blocked along the x axis and start_cell on the left of end_cell
                    pygame.draw.line(screen, colors[2], (self.getcell(start_cell, 'right'), self.getcell(start_cell, 'top')), 
                                                (self.getcell(start_cell, 'right'), self.getcell(start_cell, 'bottom')), width=2)
                
            
    def generate(self,visual=False):
        test = True
        while test :
            neighbors = list(nx.all_neighbors(self.graph, self.current_cell)) 
            valid_neighbors = list(filter(lambda cell : not self.getcell(cell,'visited'), neighbors))
            if len(valid_neighbors)>=1:
                next_cell = random.choice(valid_neighbors)
                self.setcell(next_cell, 'visited',  True)
                self.stack.append(self.current_cell)
                self.graph.edges[self.current_cell, next_cell]['path'] = True
                self.current_cell = next_cell
                if visual : # If you want to see the Maze generation
                    self.drawcell(self.current_cell, colors[3])            
                    pygame.display.flip()
            elif len(self.stack)>0 :
                
                self.current_cell= self.stack.pop(-1)
                
            test = sum(nx.get_node_attributes(self.graph,"visited").values())<self.nb_cells
        
        # Valid graph 
        # will be used to measure distance between prey and predator
        self.valid_graph = self.graph.copy()
        for path in self.valid_graph.edges :
            if not self.valid_graph[path[0]][path[1]]['path'] :
                self.valid_graph.remove_edge(*path)

class Player(pygame.sprite.Sprite):
    def __init__(self, cell=(0,0)):
        super().__init__()
        self.cell = cell
        self.x,self.y = cell
        self.image = player_img
        self.rect = self.image.get_rect()
        
        
    def draw(self):
        screen.blit(self.image, self.rect)

    
if __name__ == "__main__":
    frame_count = 0
    running = True
    myMaze = Maze(18,12)
    myMaze.generate()
    screen.fill(colors[-2])
    myMaze.draw()
    # pygame.display.flip()
    # time.sleep(5)
    # start_cell = (3,3)
    # end_cell = (8,11)
    # path = nx.shortest_path(myMaze.valid_graph,start_cell,end_cell)
    # for cell in path : 
    #     myMaze.drawcell(cell, colors[-1])
    mow = Player()
    while running:
        mow.draw()
        # Gestion des entrées au clavier
        for event in pygame.event.get():
            # Handle the closing
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                keypressed = event.key
                if keypressed == pygame.K_SPACE:
                    print("Appui sur la barre espace")
            else:
                keypressed = 0

        # Pour K_RIGHT ou K_LEFT on peut laisser la touche enfoncée
        if keypressed == pygame.K_RIGHT:
            print("Appui sur flèche droite")
        elif keypressed == pygame.K_LEFT:
            print("Appui sur flèche gauche")

                
        pygame.display.flip()
        clock.tick(FPS)
