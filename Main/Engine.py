'''
Created on 10/mag/2014

@author: Federico
'''

import pygame, sys
import logging
import Main.LookupTable
import Main.Constants
import Main.GraphicObjects


logging.getLogger().setLevel(logging.DEBUG)

    
''' Asteroid '''
def main():
    # Angle lookup table
    ANGLE_TABLE = Main.LookupTable.CosSinTable()
    
    startPosition = (100, 100)
    starShip = Main.GraphicObjects.StarShip(startPosition[0], startPosition[1], Main.Constants.WHITE, ANGLE_TABLE)
    
    pygame.init()

    pygame.key.set_repeat(10, 10)
        
    FPS = 30
    FPSCLOCK = pygame.time.Clock()
    
    # Drawing surface
    DISPLAY_SURFACE = pygame.display.set_mode((500, 400))
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.locals.KEYDOWN:
                # Pulsante A
                if event.key == pygame.locals.K_a:
                    starShip.rotate(10)
                     
        DISPLAY_SURFACE.fill(Main.Constants.BLACK)
        starShip.draw(DISPLAY_SURFACE)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
  
        
if __name__ == "__main__":
    main()