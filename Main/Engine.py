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
    
    def handle_key_events(self, event):
        if event.type == pygame.locals.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # Exit application
            pygame.quit()
            sys.exit()

    def handle_keyboard(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.locals.K_a]:
            # Button A --> Rotate
            self.starship.rotate_head_direction(-10)
        if keys_pressed[pygame.locals.K_d]:
            # Button D --> Rotate
            self.starship.rotate_head_direction(10)
        if keys_pressed[pygame.locals.K_SPACE]:
            # Space bar --> Fire
            new_bullet = self.starship.fire()
            self._graph_objects_list.append(new_bullet)
        if keys_pressed[pygame.locals.K_q]:
            # Exit application
            pygame.quit()
            sys.exit()

    def draw(self, viewport):
        for obj in self._graph_objects_list:
            if not viewport.is_object_visible(obj):
                self._graph_objects_list.remove(obj)
            else:
                obj.draw(viewport)
         
    def update_positions(self, delta_time):
        for obj in self._graph_objects_list:
            obj.update_position(delta_time)

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
        # handle events
        for event in pygame.event.get():
            ENGINE.handle_key_events(event)

        # Handle keyboard
        ENGINE.handle_keyboard()

        delta_time = FPS_CLOCK.tick(FPS)

        ENGINE.update_positions(delta_time / 1000)

        # Draw the scene
        DISPLAY_SURFACE.fill(Main.Constants.BLACK)
        ENGINE.draw(VIEWPORT)
        ENGINE.show_number_of_object_in_list(DISPLAY_SURFACE, DEFAULT_FONT)

        pygame.display.update()

  
    
# -----------------------------------------------------------------
if __name__ == "__main__":
    main()