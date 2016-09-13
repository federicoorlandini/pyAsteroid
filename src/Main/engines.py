import pygame.locals
import sys
import logging
import Main.constants
import Main.graphicobjects
import Main.logic
import Main.display
import Main.geometrytransformation2d
from Main import constants
from Main.collisions import CollisionHandler


logging.getLogger().setLevel(logging.DEBUG)


# -----------------------------------------------------------------


class Engine(object):
    def __init__(self, display):
        # The world size will be the same of the display size
        self.world = World((display.width, display.height))
        self._display = display

    def handle_key_events(self, event):
        if event.type == pygame.locals.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # Exit application
            pygame.quit()
            sys.exit()

    def handle_keyboard(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.locals.K_a]:
            # Button A --> Rotate
            self.world.starship.rotate_object(-10)

        if keys_pressed[pygame.locals.K_d]:
            # Button D --> Rotate
            self.world.starship.rotate_object(10)

        if keys_pressed[pygame.locals.K_SPACE]:
            # Space bar --> Fire
            new_bullet = self.world.starship.fire()
            if new_bullet is not None:
                self.world.add_object(new_bullet)

        if keys_pressed[pygame.locals.K_q]:
            # Exit application
            pygame.quit()
            sys.exit()

    ''' Draw the entire world '''
    def draw(self):
        # Draw all the objects included in the world
        world_objects_list_to_render = self.world.get_world_objects_list()
        # Render all the objects in the world
        for world_object in world_objects_list_to_render:
            self._display.draw_world_vertexes(world_object.vertexes, world_object.color)

    ''' Update the world status'''
    def update_world(self, time_passed):
        self.world.process(time_passed)

    ''' Return the number of objects in the world '''
    def show_number_of_objects_in_worlds(self, display_surface, font):
        label_surface = font.render("Objects: %s" % len(self.world._objects_list), 1, (255, 255, 255))
        display_surface.blit(label_surface, (0, 0))

# -----------------------------------------------------------------

''' the world contains all the objects '''
class World:
    # This is a single object that lives in the world
    class WorldObject(object):
        def __init__(self, vertexes, color):
            self.vertexes = vertexes
            self.color = color

    def __init__(self, world_size):
        # World width and height
        self._world_width = world_size[0]
        self._world_height = world_size[1]
        # Max and min coordinates in the world to be visible
        self._x_max = self._world_width / 2
        self._x_min = - self._x_max
        self._y_max = self._world_height / 2
        self._y_min = - self._y_max
        # Objects list
        self._objects_list = {}
        self._objects_counter = 0
        # Add the objects in the world
        self.starship = Main.graphicobjects.StarShip(0, 0, Main.constants.WHITE)
        self.add_object(self.starship)
        self.asteroid_generator = Main.logic.AsteroidGenerator(self, 30, 1)
        self.collision_handler = CollisionHandler(self)

    ''' Add an object to the world '''
    def add_object(self, graphical_object):
        self._objects_counter += 1
        graphical_object.id = self._objects_counter
        self._objects_list[graphical_object.id] = graphical_object

    ''' Return the list of the objects in the world '''
    def get_objects_list(self):
        return self._objects_list

    ''' Process the world, updating the status of each object '''
    def process(self, time_passed):
        # Check if there is a new asteroid
        self.asteroid_generator.process()
        new_asteroid = self.asteroid_generator.get_new_asteroid()
        if new_asteroid is not None:
            self.add_object(new_asteroid)

        # Process all the objects in the world
        for key in self._objects_list:
            self._objects_list[key].process(time_passed)

        # Remove objects that are outside the bounds
        self._remove_objects_not_visible()

        # Collision handling
        self.collision_handler.handle()

    ''' Return a collection of WorldObject.
        Each items contains the vertexes collection and the color of the object '''
    def get_world_objects_list(self):
        # For each object in the world, return an array of world vertexes
        world_vertexes_list = [self._build_world_object(value)
                               for (key, value)
                               in self._objects_list.items()]
        return world_vertexes_list

    def _build_world_object(self, object):
        world_vertexes_list = self._get_world_vertexes_for_object(object)
        color = object.get_color()
        return World.WorldObject(world_vertexes_list, color)

    ''' Transform the object local vertexes coordinates in world coordinates
        Given a world object, the method returns a list ov vertexes that are the object vertexes
        in the world coordinate axis '''
    def _get_world_vertexes_for_object(self, world_object):
        # Get the coordinates relative to the world axis (where (0,0) is the center of the screen)
        # of each vertex of the object
        object_vertexes = world_object.get_vertexes()
        # First, rotation of each vertex
        world_vertexes = [Main.geometrytransformation2d.from_local_to_world_coordinates(vertex, world_object.position, world_object.rotation_angle)
                          for vertex
                          in object_vertexes]
        return world_vertexes

    ''' Remove the objects that are outside the world bounds '''
    def _remove_objects_not_visible(self):
        keys_of_objects_to_remove = [key for key
                                     in self._objects_list
                                     if not self._is_object_visible(self._objects_list[key])]
        for key in keys_of_objects_to_remove:
            del self._objects_list[key]

    ''' Check if the object is visible.
        An object is visible if all the object vertexes are in the world bounds '''
    def _is_object_visible(self, graphic_object):
        world_vertexes = self._get_world_vertexes_for_object(graphic_object)
        for vertex in world_vertexes:
            if vertex.x < self._x_max and vertex.x > self._x_min and vertex.y > self._y_min and vertex.y < self._x_max:
                return True
        # If the code arrive here, it means that there is at least one vertex that is visible
        return False
# -----------------------------------------------------------------


def main():
    # Main game loop
    pygame.init()

    # The default font
    DEFAULT_FONT = pygame.font.SysFont("arial", 15)

    # Prepare the drawing surface
    DISPLAY_SURFACE = pygame.display.set_mode((constants.DISPLAY_SURFACE_WIDTH, constants.DISPLAY_SURFACE_HEIGHT))

    # Prepare the display area
    DISPLAY = Main.display.Display(constants.DISPLAY_SURFACE_WIDTH, constants.DISPLAY_SURFACE_HEIGHT, DISPLAY_SURFACE)

    ENGINE = Engine(DISPLAY)

    # Keyboard repeating time
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
        ENGINE.draw()
        ENGINE.show_number_of_objects_in_worlds(DISPLAY_SURFACE, DEFAULT_FONT)

        pygame.display.update()


# -----------------------------------------------------------------
if __name__ == "__main__":
    main()
