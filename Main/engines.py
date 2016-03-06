import pygame.locals
import sys
import logging
import Main.constants
import Main.graphicobjects
import Main.logic
from Main import viewport, constants
from Main.collisions import CollisionHandler


logging.getLogger().setLevel(logging.DEBUG)


# -----------------------------------------------------------------


class Engine(object):
    def __init__(self, screen_size):
        self.world = World(screen_size)

    def handle_key_events(self, event):
        if event.type == pygame.locals.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # Exit application
            pygame.quit()
            sys.exit()

    def handle_keyboard(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.locals.K_a]:
            # Button A --> Rotate
            self.world.starship.rotate_head_direction(-10)

        if keys_pressed[pygame.locals.K_d]:
            # Button D --> Rotate
            self.world.starship.rotate_head_direction(10)

        if keys_pressed[pygame.locals.K_SPACE]:
            # Space bar --> Fire
            new_bullet = self.world.starship.fire()
            if new_bullet is not None:
                self.world.add_object(new_bullet)

        if keys_pressed[pygame.locals.K_q]:
            # Exit application
            pygame.quit()
            sys.exit()

    def draw(self, viewport):
        self.world.render(viewport)

    def update_world(self, time_passed):
        self.world.process(time_passed)

    def show_number_of_object_in_list(self, display_surface, font):
        label_surface = font.render("Objects: %s" % len(self.world.object_list), 1, (255, 255, 255))
        display_surface.blit(label_surface, (0, 0))


# -----------------------------------------------------------------


class World:
    def __init__(self, screen_size):
        background = pygame.Surface(screen_size)
        self.background = background.convert()
        self.background.fill((0, 0, 0))
        self.object_list = {}
        self._object_counter = 0
        # Add the objects in the world
        self.starship = Main.graphicobjects.StarShip(self, 0, 0, Main.constants.WHITE, Main.constants.LOOKUP_TABLE)
        self.add_object(self.starship)
        self.asteroid_generator = Main.logic.AsteroidGenerator(self, 30, 1)
        self.collision_handler = CollisionHandler(self)

    def add_object(self, graphical_object):
        self._object_counter += 1
        graphical_object.id = self._object_counter
        self.object_list[graphical_object.id] = graphical_object

    def process(self, time_passed):
        # Check if there is a new asteroid
        self.asteroid_generator.process()
        new_asteroid = self.asteroid_generator.get_new_asteroid()
        if new_asteroid is not None:
            self.add_object(new_asteroid)

        # Process all the objects in the world
        for key in self.object_list:
            self.object_list[key].process(time_passed)

        # Collision handling
        self.collision_handler.handle()

    def render(self, viewport):
        # Draw the background
        viewport.draw_surface.blit(self.background, (0, 0))

        # Remove the not visible objects from the world
        self._remove_objects_not_visible(viewport)

        # Render all the objects in the world
        for key in self.object_list:
            obj = self.object_list[key]
            obj.render(viewport)

    def _remove_objects_not_visible(self, viewport):
        keys_of_objects_to_remove = [key for key in self.object_list if
                                     not viewport.is_object_visible(self.object_list[key])]
        for key in keys_of_objects_to_remove:
            del self.object_list[key]

# -----------------------------------------------------------------


def main():
    # Main game loop
    pygame.init()

    # The default font
    DEFAULT_FONT = pygame.font.SysFont("arial", 15)

    # Prepare the drawing surface
    DISPLAY_SURFACE = pygame.display.set_mode((constants.VIEWPORT_WIDTH, constants.VIEWPORT_HEIGHT))

    # Prepare the viewport
    VIEWPORT = viewport.ViewPort(constants.VIEWPORT_WIDTH, constants.VIEWPORT_HEIGHT, DISPLAY_SURFACE)

    ENGINE = Engine((constants.VIEWPORT_WIDTH, constants.VIEWPORT_HEIGHT))

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

        ENGINE.update_world(delta_time / 1000)

        # Draw the scene
        DISPLAY_SURFACE.fill(Main.constants.BLACK)
        ENGINE.draw(VIEWPORT)
        ENGINE.show_number_of_object_in_list(DISPLAY_SURFACE, DEFAULT_FONT)

        pygame.display.update()


# -----------------------------------------------------------------
if __name__ == "__main__":
    main()
