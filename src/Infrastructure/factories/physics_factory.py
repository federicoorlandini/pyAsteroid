"""
Physics Factory for pyAsteroid

This factory creates physics-related objects (vectors, circles, etc.) with
configuration-driven properties and proper dependency injection.
"""

from typing import Tuple, Any
from Infrastructure.interfaces.interfaces import IPhysicsFactory, IConfiguration
from Main.geometrytransformation2d import Vector2D, Circle


class PhysicsFactory(IPhysicsFactory):
    """
    Factory for creating physics objects with configuration support.
    
    This factory bridges the new DI system with the existing physics
    implementation while providing configuration flexibility.
    """
    
    def __init__(self, config: IConfiguration):
        """
        Initialize the physics factory.
        
        Args:
            config: Configuration manager instance
        """
        self._config = config
    
    def create_vector(self, x: float, y: float) -> Vector2D:
        """
        Create a Vector2D object.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Vector2D instance
        """
        return Vector2D(x, y)
    
    def create_circle(self, center: Vector2D, radius: float) -> Circle:
        """
        Create a Circle object for collision detection.
        
        Args:
            center: Center point as Vector2D
            radius: Circle radius
            
        Returns:
            Circle instance
        """
        return Circle(center, radius)
    
    def create_vector_from_config(self, config_key: str, default: Tuple[float, float] = (0.0, 0.0)) -> Vector2D:
        """
        Create a Vector2D from configuration.
        
        Args:
            config_key: Configuration key for the vector coordinates
            default: Default coordinates if config not found
            
        Returns:
            Vector2D instance
        """
        coords = self._config.get(config_key, default)
        if isinstance(coords, list) and len(coords) >= 2:
            return self.create_vector(float(coords[0]), float(coords[1]))
        elif isinstance(coords, tuple) and len(coords) >= 2:
            return self.create_vector(float(coords[0]), float(coords[1]))
        else:
            return self.create_vector(float(default[0]), float(default[1]))
    
    def get_collision_threshold(self) -> float:
        """
        Get the collision threshold from configuration.
        
        Returns:
            Collision threshold value
        """
        return self._config.get_float('physics.collision_threshold', 0.0001)