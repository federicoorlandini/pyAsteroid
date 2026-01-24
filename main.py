#!/usr/bin/env python3
"""
pyAsteroid - A simple Asteroid game implementation

This is the main entry point for the pyAsteroid game.
Run this file from the project root directory with: python main.py
"""

import sys
import os

def setup_python_path():
    """Add src directory to Python path for proper module imports"""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Add src directory to Python path for all module imports
    src_dir = os.path.join(script_dir, 'src')
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    # Also add Main directory for backward compatibility
    src_main_dir = os.path.join(script_dir, 'src', 'Main')
    if src_main_dir not in sys.path:
        sys.path.insert(0, src_main_dir)

def main():
    """Main entry point for the game using dependency injection"""
    try:
        # Setup Python path for imports
        setup_python_path()
        
        # Import and run the game with DI
        from engines import Engine, World
        from Infrastructure.config.config_manager import ConfigurationManager
        from Infrastructure.factories.system_factory import SystemFactory
        from Infrastructure.factories.game_object_factory import GameObjectFactory
        from Infrastructure.factories.physics_factory import PhysicsFactory
        from Main.input_handler import KeyboardInputHandler
        import display
        import pygame
        import constants
        
        # Initialize configuration and factories
        config = ConfigurationManager()
        physics_factory = PhysicsFactory(config)
        system_factory = SystemFactory(config)
        game_object_factory = GameObjectFactory(config, physics_factory)
        
        # Create display using configuration
        width = config.get_int('display.width', constants.DISPLAY_SURFACE_WIDTH)
        height = config.get_int('display.height', constants.DISPLAY_SURFACE_HEIGHT)
        draw_surface = pygame.display.set_mode((width, height))
        display_obj = display.Display(width, height, draw_surface)
        
        # Create world with factory dependencies
        world_size = (width, height)
        world = World(world_size, game_object_factory, system_factory)
        
        # Create input handler
        input_handler = KeyboardInputHandler(world)
        
        # Create engine with all dependencies
        engine = Engine(display_obj, world, input_handler)
        
        # Start the game using original main function structure
        pygame.init()
        DEFAULT_FONT = pygame.font.SysFont("arial", 15)
        
        # Keyboard repeating time
        key_delay, key_interval = system_factory.get_key_repeat_settings()
        pygame.key.set_repeat(key_delay, key_interval)
        
        # Update speed
        fps = system_factory.get_fps()
        FPS_CLOCK = pygame.time.Clock()
        
        # Engine loop
        while True:
            # handle events
            pygame.event.get()

            # Handle keyboard
            engine.handle_keyboard()

            delta_time = FPS_CLOCK.tick(fps)

            engine.update_world(delta_time / 1000)

            # Draw the scene
            engine.clean()
            engine.draw()
            engine.show_number_of_objects_in_worlds(DEFAULT_FONT)

            pygame.display.update()
        
    except ImportError as e:
        print(f"Error importing game modules: {e}")
        print("Make sure you're running this from the project root directory")
        print("Or try running: cd src/Main && python engines.py")
        sys.exit(1)
    except Exception as e:
        print(f"Error running game: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()