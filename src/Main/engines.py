import pygame.locals
import sys
import logging
import constants
import graphicobjects
import logic
import display
import geometrytransformation2d
from collisions import CollisionHandler

__all__ = ['Engine', 'World']

logging.getLogger().setLevel(logging.DEBUG)


# -----------------------------------------------------------------


class Engine(object):
    def __init__(self, display, world, input_handler):
        # The world size will be the same of the display size
        self.world = world
        self._display = display
        self._input_handler = input_handler
        
    def handle_keyboard(self):
        """Delegate to injected input handler"""
        self._input_handler.handle_input()
        if self._input_handler.is_exit_requested():
            pygame.quit()
            sys.exit(0)

    ''' Fill the display surface with black '''
    def clean(self):
        self._display.draw_surface.fill(constants.BLACK)

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
    def show_number_of_objects_in_worlds(self, font):
        label_surface = font.render("Objects: %s" % len(self.world._objects_list), 1, (255, 255, 255))
        self._display.draw_surface.blit(label_surface, (0, 0))
    
    def start_game(self):
        """Start the main game loop using DI-provided configuration.
        
        This method initializes all game subsystems using the DI container
        and enters the main game loop. It requires pygame to be available.
        
        Raises:
            ValueError: If required factories cannot be created.
            ImportError: If required modules are not available.
        """
        import pygame
        
        pygame.init()
        
        # Add src to path for imports
        import os
        script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        src_dir = os.path.join(script_dir, 'src')
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
        
        from Infrastructure.config.config_manager import ConfigurationManager
        from Infrastructure.factories.system_factory import SystemFactory
        from Infrastructure.factories.game_object_factory import GameObjectFactory
        from Infrastructure.factories.physics_factory import PhysicsFactory
        from Main.input_handler import KeyboardInputHandler
        
        # Initialize configuration and factories
        config = ConfigurationManager()
        
        system_factory = SystemFactory(config)
        if system_factory is None:
            raise ValueError("Failed to create SystemFactory. Check configuration.")
        
        physics_factory = PhysicsFactory(config)
        if physics_factory is None:
            raise ValueError("Failed to create PhysicsFactory. Check configuration.")
        
        game_object_factory = GameObjectFactory(config, physics_factory)
        if game_object_factory is None:
            raise ValueError("Failed to create GameObjectFactory. Check configuration.")
        
        # Create display using factory and configuration
        width = config.get_int('display.width', 500)
        height = config.get_int('display.height', 500)
        draw_surface = pygame.display.set_mode((width, height))
        
        display_obj = display.Display(width, height, draw_surface)
        
        # Update engine with DI-provided dependencies
        self._display = display_obj
        
        # Update world with factory dependencies
        self.world.starship = game_object_factory.create_starship_at_origin()
        self.world.asteroid_generator = system_factory.create_asteroid_generator(self.world)
        self.world.collision_handler = system_factory.create_collision_handler(self.world)
        
        # Update input handler
        self._input_handler = KeyboardInputHandler(self.world)
        
        # Get FPS and keyboard settings from configuration
        fps = system_factory.get_fps()
        key_delay, key_interval = system_factory.get_key_repeat_settings()
        pygame.key.set_repeat(key_delay, key_interval)
        
        # Game setup
        DEFAULT_FONT = pygame.font.SysFont("arial", 15)
        FPS_CLOCK = pygame.time.Clock()
        
        # Engine loop
        while True:
            # handle events
            pygame.event.get()

            # Handle keyboard
            self.handle_keyboard()

            delta_time = FPS_CLOCK.tick(fps)

            self.update_world(delta_time / 1000)

            # Draw the scene
            self.clean()
            self.draw()
            self.show_number_of_objects_in_worlds(DEFAULT_FONT)

            pygame.display.update()

# -----------------------------------------------------------------

''' the world contains all the objects '''
class World:
    # This is a single object that lives in the world
    class WorldObject(object):
        def __init__(self, vertexes, color):
            self.vertexes = vertexes
            self.color = color

    def __init__(self, world_size, game_object_factory, system_factory):
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
        # Add the objects in the world using factories
        self.starship = game_object_factory.create_starship_at_origin()
        self.add_object(self.starship)
        self.asteroid_generator = system_factory.create_asteroid_generator(self)
        self.collision_handler = system_factory.create_collision_handler(self)

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
        world_vertexes = [geometrytransformation2d.from_local_to_world_coordinates(vertex, world_object.position, world_object.rotation_angle)
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
        # If the code arrive here, it means that all the vertex are outside the visible area, so the object is not visible
        return False
# -----------------------------------------------------------------


def main():
    """Legacy entry point for the game.
    
    Uses the DI-based start_game() method on Engine for proper
    factory initialization and configuration loading.
    """
    import os

    # Add src to path for imports
    script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    src_dir = os.path.join(script_dir, 'src')
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    from Infrastructure.config.config_manager import ConfigurationManager
    from Infrastructure.factories.system_factory import SystemFactory
    from Infrastructure.factories.game_object_factory import GameObjectFactory
    from Infrastructure.factories.physics_factory import PhysicsFactory
    from Main.input_handler import KeyboardInputHandler

    # Initialize configuration and factories
    config = ConfigurationManager()
    system_factory = SystemFactory(config)
    physics_factory = PhysicsFactory(config)
    game_object_factory = GameObjectFactory(config, physics_factory)

    # Create the world
    width = config.get_int('display.width', constants.DISPLAY_SURFACE_WIDTH)
    height = config.get_int('display.height', constants.DISPLAY_SURFACE_HEIGHT)
    world = World((width, height), game_object_factory, system_factory)

    # Create display
    pygame.init()
    draw_surface = pygame.display.set_mode((width, height))
    DISPLAY = display.Display(width, height, draw_surface)

    # Create input handler
    input_handler = KeyboardInputHandler(world)

    # Create engine with all dependencies
    ENGINE = Engine(DISPLAY, world, input_handler)

    # Keyboard repeating time
    key_delay, key_interval = system_factory.get_key_repeat_settings()
    pygame.key.set_repeat(key_delay, key_interval)

    # Update speed
    FPS = system_factory.get_fps()
    FPS_CLOCK = pygame.time.Clock()
    DEFAULT_FONT = pygame.font.SysFont("arial", 15)

    # Engine loop
    while True:
        # handle events
        pygame.event.get()

        # Handle keyboard
        ENGINE.handle_keyboard()

        delta_time = FPS_CLOCK.tick(FPS)

        ENGINE.update_world(delta_time / 1000)

        # Draw the scene
        ENGINE.clean()
        ENGINE.draw()
        ENGINE.show_number_of_objects_in_worlds(DEFAULT_FONT)

        pygame.display.update()


# -----------------------------------------------------------------
if __name__ == "__main__":
    main()
