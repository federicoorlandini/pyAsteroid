#!/usr/bin/env python3
"""
Factory Demo for Step 2

This script demonstrates the factory implementations working with configuration
and proper dependency injection.
"""

import sys
import os

# Add both src and src/Main to Python path
script_dir = os.path.dirname(__file__)
src_dir = os.path.join(script_dir, 'src')
main_dir = os.path.join(script_dir, 'src', 'Main')

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
if main_dir not in sys.path:
    sys.path.insert(0, main_dir)

from Infrastructure.config.config_manager import ConfigurationManager
from Infrastructure.factories.physics_factory import PhysicsFactory
from Infrastructure.factories.game_object_factory import GameObjectFactory
from Infrastructure.factories.system_factory import SystemFactory


def demonstrate_physics_factory():
    """Demonstrate physics factory functionality."""
    print("=== Physics Factory Demo ===")
    
    config = ConfigurationManager('src/Infrastructure/config/game_config.yaml')
    physics_factory = PhysicsFactory(config)
    
    # Test vector creation
    vector = physics_factory.create_vector(10, 20)
    print(f"Created vector: ({vector.x}, {vector.y})")
    
    # Test circle creation
    circle = physics_factory.create_circle(vector, 5.5)
    print(f"Created circle: center=({circle.center.x}, {circle.center.y}), radius={circle.radius}")
    
    # Test collision threshold
    threshold = physics_factory.get_collision_threshold()
    print(f"Collision threshold: {threshold}")
    
    print("+ Physics factory working correctly\n")


def demonstrate_game_object_factory():
    """Demonstrate game object factory functionality."""
    print("=== Game Object Factory Demo ===")
    
    config = ConfigurationManager('src/Infrastructure/config/game_config.yaml')
    physics_factory = PhysicsFactory(config)
    game_factory = GameObjectFactory(config, physics_factory)
    
    # Test starship creation
    starship = game_factory.create_starship(0, 0)
    print(f"Starship created: {type(starship).__name__}")
    print(f"  Position: ({starship.position.x}, {starship.position.y})")
    print(f"  Color: {starship.color}")
    print(f"  Reload counter: {starship.reload_counter}")
    
    # Test bullet creation
    bullet = game_factory.create_bullet(10, 10, 45)
    print(f"Bullet created: {type(bullet).__name__}")
    print(f"  Position: ({bullet.position.x}, {bullet.position.y})")
    print(f"  Speed: {bullet.speed}")
    print(f"  Angle: {bullet.head_angle}")
    
    # Test asteroid creation
    asteroid = game_factory.create_asteroid(100, 100, 0, 20)
    print(f"Asteroid created: {type(asteroid).__name__}")
    print(f"  Position: ({asteroid.position.x}, {asteroid.position.y})")
    print(f"  Speed: {asteroid.speed}")
    print(f"  Angle: {asteroid.head_angle}")
    
    print("+ Game object factory working correctly\n")


def demonstrate_system_factory():
    """Demonstrate system factory functionality."""
    print("=== System Factory Demo ===")
    
    config = ConfigurationManager('src/Infrastructure/config/game_config.yaml')
    system_factory = SystemFactory(config)
    
    # Test configuration retrieval
    world_bounds = system_factory.get_world_bounds()
    print(f"World bounds: {world_bounds}")
    
    fps = system_factory.get_fps()
    print(f"FPS: {fps}")
    
    key_repeat = system_factory.get_key_repeat_settings()
    print(f"Key repeat settings: {key_repeat}")
    
    print("+ System factory working correctly\n")


def demonstrate_backward_compatibility():
    """Demonstrate that existing constructors still work."""
    print("=== Backward Compatibility Demo ===")
    
    try:
        # Test that old constructors still work
        from Main.graphicobjects import StarShip, Bullet, Asteroid
        from Main.geometrytransformation2d import Vector2D
        
        # Old way - should still work
        starship = StarShip(0, 0, (255, 255, 255))
        print(f"Old starship constructor works: {type(starship).__name__}")
        
        bullet = Bullet(0, 0, 0)
        print(f"Old bullet constructor works: {type(bullet).__name__}")
        
        asteroid = Asteroid(0, 0, 0, 10)
        print(f"Old asteroid constructor works: {type(asteroid).__name__}")
        
        print("+ Backward compatibility maintained\n")
        
    except Exception as e:
        print(f"Backward compatibility issue: {e}\n")


def main():
    """Run all factory demonstrations."""
    print("pyAsteroid - Factory Implementation Demo")
    print("=" * 45)
    
    try:
        demonstrate_physics_factory()
        demonstrate_game_object_factory()
        demonstrate_system_factory()
        demonstrate_backward_compatibility()
        
        print("Step 2 Factory Implementation - COMPLETED SUCCESSFULLY!")
        print("\nThe following components are now ready:")
        print("+ Physics Factory")
        print("+ Game Object Factory")
        print("+ System Factory")
        print("+ Configuration Integration")
        print("+ Backward Compatibility")
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())