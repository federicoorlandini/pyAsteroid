'''
Created on 10/mag/2014

@author: Federico
'''

import pygame.locals
import sys
import logging
import Main.Constants
import Main.GraphicObjects
from Main import ViewPort


logging.getLogger().setLevel(logging.DEBUG)

   
class Engine(object):
    _graph_objects_list = []
       
    def __init__(self):
        self.starship = Main.GraphicObjects.StarShip(0, 0, Main.Constants.WHITE, Main.Constants.LOOKUP_TABLE)
        self._graph_objects_list.append(self.starship)
    
    def handle_keys(self, event):
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.locals.KEYDOWN:
            # Button A --> Rotate
            if event.key == pygame.locals.K_a:
                self.starship.rotate(-10)
            # Button D --> Rotate
            if event.key == pygame.locals.K_d:
                self.starship.rotate(10)
            # Space bar --> Fire
            if event.key == pygame.locals.K_SPACE:
                new_bullet = self.starship.fire()
                self._graph_objects_list.append(new_bullet)
                
    def draw(self, viewport, display_surface):
        for obj in self._graph_objects_list:
            obj.draw(viewport)
         
    def update_positions(self):
        for obj in self._graph_objects_list:
            obj.update_position()
        
''' Asteroid '''
def main():    
    pygame.init()
    
    VIEWPORT_WIDTH = 500;
    VIEWPORT_HEIGHT = 500;
    
    ENGINE = Engine()
    
    # Prepare the drawing surface
    DISPLAY_SURFACE = pygame.display.set_mode((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))
    
    # Prepare the viewport
    VIEWPORT = ViewPort.ViewPort(VIEWPORT_WIDTH, VIEWPORT_HEIGHT, DISPLAY_SURFACE)
    
    pygame.key.set_repeat(10, 10)

    # Update speed
    FPS = 30
    FPSCLOCK = pygame.time.Clock()

    # Engine loop
    while True:
        ENGINE.update_positions()
        
        for event in pygame.event.get():
            ENGINE.handle_keys(event)
                            
        DISPLAY_SURFACE.fill(Main.Constants.BLACK)
        ENGINE.draw(VIEWPORT, DISPLAY_SURFACE)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
  
    

if __name__ == "__main__":
    main()