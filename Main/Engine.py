import pygame.locals
import sys
import logging
import Main.Constants
import Main.GraphicObjects
from Main import ViewPort


logging.getLogger().setLevel(logging.DEBUG)

# -----------------------------------------------------------------


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
                self.starship.rotate_head_direction(-10)
            # Button D --> Rotate
            if event.key == pygame.locals.K_d:
                self.starship.rotate_head_direction(10)
            # Space bar --> Fire
            if event.key == pygame.locals.K_SPACE:
                new_bullet = self.starship.fire()
                self._graph_objects_list.append(new_bullet)
                
    def draw(self, viewport):
        for obj in self._graph_objects_list:
            if not viewport.is_object_visible(obj):
                self._graph_objects_list.remove(obj)
            else:
                obj.draw(viewport)
         
    def update_positions(self):
        for obj in self._graph_objects_list:
            obj.update_position()

    def show_number_of_object_in_list(self, display_surface, font):
        label_surface = font.render("Objects: %s" % len(self._graph_objects_list), 1, (255,255,255))
        display_surface.blit(label_surface, (0, 0))

# -----------------------------------------------------------------


def main():
    """ Main game loop """
    pygame.init()
    
    VIEWPORT_WIDTH = 500;
    VIEWPORT_HEIGHT = 500;
    
    ENGINE = Engine()

    # The default font
    DEFAULT_FONT = pygame.font.SysFont("arial", 15)

    # Prepare the drawing surface
    DISPLAY_SURFACE = pygame.display.set_mode((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))
    
    # Prepare the viewport
    VIEWPORT = ViewPort.ViewPort(VIEWPORT_WIDTH, VIEWPORT_HEIGHT, DISPLAY_SURFACE)
    
    pygame.key.set_repeat(10, 10)

    # Update speed
    FPS = 30
    FPS_CLOCK = pygame.time.Clock()

    # Engine loop
    while True:
        ENGINE.update_positions()
        
        for event in pygame.event.get():
            ENGINE.handle_keys(event)
                            
        DISPLAY_SURFACE.fill(Main.Constants.BLACK)
        ENGINE.draw(VIEWPORT)

        ENGINE.show_number_of_object_in_list(DISPLAY_SURFACE, DEFAULT_FONT)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)
  
    
# -----------------------------------------------------------------
if __name__ == "__main__":
    main()