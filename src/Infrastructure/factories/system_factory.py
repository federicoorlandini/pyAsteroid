"""
System Factory for pyAsteroid

This factory creates game system objects (collision handlers, asteroid generators, etc.)
with configuration-driven properties and proper dependency injection.
"""

from typing import Optional
from Infrastructure.interfaces.interfaces import (
    ISystemFactory, IConfiguration, IWorld, ICollisionHandler, 
    IAsteroidGenerator, IDisplay
)
from Main.collisions import CollisionHandler
from Main.logic import AsteroidGenerator


class SystemFactory(ISystemFactory):
    """
    Factory for creating game system objects with configuration support.
    
    This factory bridges the new DI system with existing game
    systems while providing configuration flexibility.
    """
    
    def __init__(self, config: IConfiguration):
        """
        Initialize system factory.
        
        Args:
            config: Configuration manager instance
        """
        self._config = config
    
    def create_collision_handler(self, world: IWorld) -> ICollisionHandler:
        """
        Create a collision handler for the given world.
        
        Args:
            world: The world instance to handle collisions for
            
        Returns:
            Configured CollisionHandler instance
        """
        return CollisionHandler(world)
    
    def create_asteroid_generator(self, world: IWorld) -> IAsteroidGenerator:
        """
        Create an asteroid generator with configuration-driven settings.
        
        Args:
            world: The world instance to spawn asteroids in
            
        Returns:
            Configured AsteroidGenerator instance
        """
        # Get configuration values
        initial_countdown = self._config.get_int('game.asteroid.spawn_countdown', 30)
        max_asteroids = self._config.get_int('game.asteroid.max_count', 1)
        
        return AsteroidGenerator(world, initial_countdown, max_asteroids)
    
    def create_display(self, width: int, height: int, draw_surface) -> IDisplay:
        """
        Create a display system for rendering.
        
        Args:
            width: Display width
            height: Display height
            draw_surface: Pygame surface to draw on
            
        Returns:
            Configured Display instance
        """
        from src.Main.display import Display
        return Display(width, height, draw_surface)
    
    def get_world_bounds(self) -> tuple:
        """
        Get world bounds from configuration.
        
        Returns:
            Tuple of (width, height) for world boundaries
        """
        width = self._config.get_int('display.width', 500)
        height = self._config.get_int('display.height', 500)
        return (width, height)
    
    def get_fps(self) -> int:
        """
        Get FPS from configuration.
        
        Returns:
            FPS setting
        """
        return self._config.get_int('display.fps', 30)
    
    def get_key_repeat_settings(self) -> tuple:
        """
        Get keyboard repeat settings from configuration.
        
        Returns:
            Tuple of (delay_ms, interval_ms) for key repeat
        """
        delay = self._config.get_int('input.key_repeat_delay', 10)
        interval = self._config.get_int('input.key_repeat_interval', 10)
        return (delay, interval)