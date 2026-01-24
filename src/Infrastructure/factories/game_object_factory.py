"""
Game Object Factory for pyAsteroid

This factory creates all game objects (StarShip, Bullet, Asteroid) with
configuration-driven properties and proper dependency injection.
"""

from typing import List, Tuple
from Infrastructure.interfaces.interfaces import (
    IGameObjectFactory, IConfiguration, IPhysicsFactory, 
    IStarShip, IBullet, IAsteroid
)
from Main.graphicobjects import StarShip, Bullet, Asteroid
from Main.geometrytransformation2d import Vector2D


class GameObjectFactory(IGameObjectFactory):
    """
    Factory for creating game objects with configuration support.
    
    This factory bridges the new DI system with the existing game
    objects while providing configuration flexibility and maintaining
    backward compatibility.
    """
    
    def __init__(self, config: IConfiguration, physics_factory: IPhysicsFactory):
        """
        Initialize the game object factory.
        
        Args:
            config: Configuration manager instance
            physics_factory: Physics factory for creating vectors and circles
        """
        self._config = config
        self._physics_factory = physics_factory
    
    def create_starship(self, x: float, y: float) -> IStarShip:
        """
        Create a StarShip object with configuration-driven properties.
        
        Args:
            x: X coordinate for the starship
            y: Y coordinate for the starship
            
        Returns:
            Configured StarShip instance
        """
        # Get configuration for starship
        color = self._config.get_color('game.starship.color', (255, 255, 255))
        vertexes_config = self._config.get_vertexes('game.starship.vertexes')
        
        # Convert vertexes to Vector2D objects
        vertexes = [
            self._physics_factory.create_vector(v[0], v[1]) 
            for v in vertexes_config
        ] if vertexes_config else None
        
        # Create starship with configured properties
        starship = StarShip(x, y, color, vertexes if vertexes else None)
        
        # Apply additional configuration if needed
        reload_counter = self._config.get_int('game.starship.reload_counter', 10)
        starship.reload_counter = reload_counter
        
        return starship
    
    def create_bullet(self, x: float, y: float, angle: float) -> IBullet:
        """
        Create a Bullet object with configuration-driven properties.
        
        Args:
            x: X coordinate for the bullet
            y: Y coordinate for the bullet
            angle: Direction angle of the bullet
            
        Returns:
            Configured Bullet instance
        """
        # Get configuration for bullet
        speed = self._config.get_int('game.bullet.speed', 150)
        vertexes_config = self._config.get_vertexes('game.bullet.vertexes')
        
        # Convert vertexes to Vector2D objects
        vertexes = [
            self._physics_factory.create_vector(v[0], v[1]) 
            for v in vertexes_config
        ] if vertexes_config else None
        
        # Create bullet with configured properties
        return Bullet(x, y, angle, speed, vertexes)
    
    def create_asteroid(self, x: float, y: float, angle: float, speed: float) -> IAsteroid:
        """
        Create an Asteroid object with configuration-driven properties.
        
        Args:
            x: X coordinate for the asteroid
            y: Y coordinate for the asteroid
            angle: Direction angle of the asteroid
            speed: Speed of the asteroid
            
        Returns:
            Configured Asteroid instance
        """
        # Get configuration for asteroid
        vertexes_config = self._config.get_vertexes('game.asteroid.vertexes')
        
        # Convert vertexes to Vector2D objects
        vertexes = [
            self._physics_factory.create_vector(v[0], v[1]) 
            for v in vertexes_config
        ] if vertexes_config else None
        
        # Create asteroid with configured properties
        return Asteroid(x, y, angle, speed, vertexes)
    
    def create_starship_at_origin(self) -> IStarShip:
        """
        Create a starship at the origin (0, 0).
        
        Returns:
            StarShip instance at origin
        """
        return self.create_starship(0, 0)
    
    def create_bullet_from_starship(self, starship) -> IBullet:
        """
        Create a bullet fired from the given starship.
        
        Args:
            starship: The starship firing the bullet
            
        Returns:
            Bullet instance positioned at starship's front
        """
        # Get starship position and direction
        position = starship.position
        
        # Calculate bullet starting position (front of starship)
        # This mirrors the original StarShip.fire() logic
        if hasattr(starship, 'object_vertexes') and starship.object_vertexes:
            front_vertex = starship.object_vertexes[0]  # First vertex is the front
            # Transform front vertex to world coordinates
            start_pos = self._transform_vertex_to_world(
                front_vertex, position, starship.rotation_angle
            )
            return self.create_bullet(start_pos.x, start_pos.y, starship.head_angle)
        else:
            # Fallback to starship position
            return self.create_bullet(position.x, position.y, starship.head_angle)
    
    def _transform_vertex_to_world(self, vertex: Vector2D, translation: Vector2D, rotation_angle: float) -> Vector2D:
        """
        Transform a local vertex to world coordinates.
        
        Args:
            vertex: Local vertex to transform
            translation: Translation (position)
            rotation_angle: Rotation angle in degrees
            
        Returns:
            Transformed vertex in world coordinates
        """
        from src.Main.geometrytransformation2d import from_local_to_world_coordinates
        return from_local_to_world_coordinates(vertex, translation, rotation_angle)