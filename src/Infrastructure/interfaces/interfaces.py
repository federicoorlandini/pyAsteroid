"""
Core interfaces for the pyAsteroid game system.

This module defines the contracts and abstractions that enable loose coupling
between components through dependency injection.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict, Tuple, Union
import pygame.surface


# Core configuration interface
class IConfiguration(ABC):
    """
    Interface for configuration management.
    Provides access to game configuration values.
    """
    
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key using dot notation."""
        pass
    
    @abstractmethod
    def get_color(self, key: str, default: tuple = (255, 255, 255)) -> tuple:
        """Get a color configuration as RGB tuple."""
        pass
    
    @abstractmethod
    def get_vertexes(self, key: str, default: Optional[List[Tuple]] = None) -> List[Tuple]:
        """Get vertex configuration as list of coordinate tuples."""
        pass
    
    @abstractmethod
    def get_int(self, key: str, default: int = 0) -> int:
        """Get a configuration value as integer."""
        pass
    
    @abstractmethod
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get a configuration value as float."""
        pass
    
    @abstractmethod
    def has(self, key: str) -> bool:
        """Check if a configuration key exists."""
        pass


# Display interfaces
class IDisplay(ABC):
    """
    Interface for display and rendering operations.
    """
    
    @abstractmethod
    def draw_world_vertexes(self, world_vertex_list: List[Any], color: tuple) -> None:
        """Draw vertexes in world coordinates."""
        pass
    
    @property
    @abstractmethod
    def width(self) -> int:
        """Get display width."""
        pass
    
    @property
    @abstractmethod
    def height(self) -> int:
        """Get display height."""
        pass
    
    @property
    @abstractmethod
    def draw_surface(self) -> pygame.surface.Surface:
        """Get the drawing surface."""
        pass


# Game object interfaces
class IGameObject(ABC):
    """
    Base interface for all game objects.
    """
    
    @abstractmethod
    def process(self, delta_time: float) -> None:
        """Update the object state based on elapsed time."""
        pass
    
    @abstractmethod
    def get_vertexes(self) -> List[Any]:
        """Get the object's vertexes."""
        pass
    
    @abstractmethod
    def get_color(self) -> tuple:
        """Get the object's color."""
        pass
    
    @property
    @abstractmethod
    def position(self) -> Any:
        """Get the object's position."""
        pass
    
    @property
    @abstractmethod
    def id(self) -> int:
        """Get the object's unique ID."""
        pass
    
    @id.setter
    @abstractmethod
    def id(self, value: int) -> None:
        """Set the object's unique ID."""
        pass


class IStarShip(IGameObject):
    """
    Interface for the player's starship.
    """
    
    @abstractmethod
    def rotate_object(self, relative_angle: int) -> None:
        """Rotate the starship."""
        pass
    
    @abstractmethod
    def fire(self) -> Optional['IBullet']:
        """Fire a bullet if not reloading."""
        pass
    
    @abstractmethod
    def is_reloading(self) -> bool:
        """Check if the starship is currently reloading."""
        pass


class IBullet(IGameObject):
    """
    Interface for bullet objects.
    """
    pass


class IAsteroid(IGameObject):
    """
    Interface for asteroid objects.
    """
    pass


# Factory interfaces
class IGameObjectFactory(ABC):
    """
    Interface for creating game objects.
    """
    
    @abstractmethod
    def create_starship(self, x: float, y: float) -> IStarShip:
        """Create a starship object."""
        pass
    
    @abstractmethod
    def create_bullet(self, x: float, y: float, angle: float) -> IBullet:
        """Create a bullet object."""
        pass
    
    @abstractmethod
    def create_asteroid(self, x: float, y: float, angle: float, speed: float) -> IAsteroid:
        """Create an asteroid object."""
        pass


class IPhysicsFactory(ABC):
    """
    Interface for creating physics objects.
    """
    
    @abstractmethod
    def create_vector(self, x: float, y: float) -> Any:
        """Create a vector object."""
        pass
    
    @abstractmethod
    def create_circle(self, center: Any, radius: float) -> Any:
        """Create a circle object."""
        pass


# System interfaces
class ICollisionHandler(ABC):
    """
    Interface for collision detection and response.
    """
    
    @abstractmethod
    def handle(self) -> None:
        """Process all collisions in the world."""
        pass


class IAsteroidGenerator(ABC):
    """
    Interface for asteroid spawning system.
    """
    
    @abstractmethod
    def process(self) -> None:
        """Update the generator state."""
        pass
    
    @abstractmethod
    def get_new_asteroid(self) -> Optional[IAsteroid]:
        """Get a newly created asteroid if ready."""
        pass


class IWorld(ABC):
    """
    Interface for the game world containing all objects.
    """
    
    @abstractmethod
    def add_object(self, graphical_object: IGameObject) -> None:
        """Add an object to the world."""
        pass
    
    @abstractmethod
    def get_objects_list(self) -> Dict[int, IGameObject]:
        """Get all objects in the world."""
        pass
    
    @abstractmethod
    def process(self, time_passed: float) -> None:
        """Update the world state."""
        pass
    
    @abstractmethod
    def get_world_objects_list(self) -> List[Any]:
        """Get renderable world objects."""
        pass


class IEngine(ABC):
    """
    Interface for the main game engine.
    """
    
    @abstractmethod
    def handle_keyboard(self) -> None:
        """Handle keyboard input."""
        pass
    
    @abstractmethod
    def clean(self) -> None:
        """Clear the display."""
        pass
    
    @abstractmethod
    def draw(self) -> None:
        """Draw the entire world."""
        pass
    
    @abstractmethod
    def update_world(self, time_passed: float) -> None:
        """Update the world state."""
        pass


# Input handling interface
class ISystemFactory(ABC):
    """
    Interface for creating game system objects.
    """
    
    @abstractmethod
    def create_collision_handler(self, world: IWorld) -> ICollisionHandler:
        """Create a collision handler for the world."""
        pass
    
    @abstractmethod
    def create_asteroid_generator(self, world: IWorld) -> IAsteroidGenerator:
        """Create an asteroid generator with configuration."""
        pass
    
    @abstractmethod
    def create_display(self, width: int, height: int, draw_surface) -> IDisplay:
        """Create a display system for rendering."""
        pass
    
    @abstractmethod
    def get_fps(self) -> int:
        """Get the configured FPS for the game."""
        pass
    
    @abstractmethod
    def get_key_repeat_settings(self) -> tuple:
        """Get keyboard repeat delay and interval settings."""
        pass


class IInputHandler(ABC):
    """
    Interface for handling user input.
    """
    
    @abstractmethod
    def handle_input(self) -> None:
        """Process user input."""
        pass
    
    @abstractmethod
    def is_exit_requested(self) -> bool:
        """Check if the user requested to exit."""
        pass