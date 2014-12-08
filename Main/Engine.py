'''
Created on 10/mag/2014

@author: Federico
'''

import pygame.locals
import sys
import logging
import Main.LookupTable
import Main.Constants
import Main.GraphicObjects
from Main import ViewPort


logging.getLogger().setLevel(logging.DEBUG)

   
class Engine(object):
    # Angle lookup table
    ANGLE_TABLE = Main.LookupTable.CosSinTable()
    _graph_objects_list = []
       
    def __init__(self):
        self.starship = Main.GraphicObjects.StarShip(0, 0, Main.Constants.WHITE, self.ANGLE_TABLE)
        self._graph_objects_list.append(self.starship)
    
    def handle_keys(self, event):
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.locals.KEYDOWN:
            # Pulsante A
            if event.key == pygame.locals.K_a:
                self.starship.rotate(10)
                
    def draw(self, viewport, display_surface):
        for obj in self._graph_objects_list:
            obj.draw(viewport, display_surface)
                
''' Asteroid '''
def main():    
    pygame.init()
    
    ENGINE = Engine()
    VIEWPORT = ViewPort.ViewPort(500, 400)
    
    pygame.key.set_repeat(10, 10)
        
    FPS = 30
    FPSCLOCK = pygame.time.Clock()
    
    # Drawing surface
    DISPLAY_SURFACE = pygame.display.set_mode((500, 400))
        
    while True:
        for event in pygame.event.get():
            ENGINE.handle_keys(event)
                            
        DISPLAY_SURFACE.fill(Main.Constants.BLACK)
        ENGINE.draw(VIEWPORT, DISPLAY_SURFACE)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
  
    

if __name__ == "__main__":
    main()