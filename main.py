#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 15:34:15 2024

@author: phil
"""


import pygame
import networkx as nx

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
    "#8FBCBB",
    "#88C0D0",
    "#81A1C1",
    "#5E81AC",
    "#BF616A",
    "#D08770",
    "#EBCB8B",
    "#A3BE8C",
    "#B48EAD",
]

class Maze():
    def __init__(self,nb_cells_x=15,nb_cells_y=10):
        self.nb_cells_x = nb_cells_x
        self.nb_cells_y = nb_cells_y
        self.nb_cells = self.nb_cells_x * self.nb_cells_y
        self.dx = WIDTH // nb_cells_x
        self.dy = HEIGHT // nb_cells_y
        self.graph = nx.grid_2d_graph(self.nb_cells_x, self.nb_cells_y)
        for cell in self.graph.nodes :
            self.graph.nodes[cell]['top'] = cell[1]*self.dy
            self.graph.nodes[cell]['bottom'] = (cell[1]+1)*self.dy
            self.graph.nodes[cell]['left'] = cell[0]*self.dx
            self.graph.nodes[cell]['right'] = (cell[0]+1)*self.dy
            
    
    def draw(self):
        for cell in self.graph.nodes :
            pygame.draw.rect(screen, colors[0], [self.graph.nodes[cell]['left'], self.graph.nodes[cell]['top'],
                                                 self.dx, self.dy], width=5)
            
        
    
        
    
if __name__ == "__main__":
    frame_count = 0
    running = True
    myMaze = Maze()
    myMaze.draw()
    while running:

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
