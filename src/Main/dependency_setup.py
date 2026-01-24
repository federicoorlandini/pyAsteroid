"""Dependency injection setup for the pyAsteroid game"""

from Infrastructure.di.container import DIContainer
from Infrastructure.config.config_manager import ConfigurationManager
from Infrastructure.factories.system_factory import SystemFactory
from Infrastructure.factories.game_object_factory import GameObjectFactory
from Infrastructure.factories.physics_factory import PhysicsFactory
from Infrastructure.interfaces.interfaces import (
    IConfiguration, ISystemFactory, IGameObjectFactory, 
    IPhysicsFactory, IEngine, IInputHandler
)
from Main.engines import Engine
from Main.input_handler import KeyboardInputHandler


def setup_dependencies() -> DIContainer:
    """Setup and configure the DI container with all dependencies"""
    container = DIContainer()
    
    # Register configuration as singleton
    config = ConfigurationManager()
    container.register_singleton(IConfiguration, lambda: config)
    
    # Register factories as singletons
    container.register_singleton(IPhysicsFactory, lambda: PhysicsFactory())
    container.register_singleton(IGameObjectFactory, lambda: GameObjectFactory())
    container.register_singleton(ISystemFactory, lambda: SystemFactory())
    
    # Register engine as singleton - will create dependencies internally
    container.register_singleton(IEngine, lambda: Engine(
        # Display will be set in start_game method
        None,
        # World with factory dependencies
        World(
            (config.get_int('display.width', 500), config.get_int('display.height', 500)),
            GameObjectFactory(),
            SystemFactory()
        ),
        # Input handler with world dependency
        KeyboardInputHandler(None)  # World will be set in start_game
    ))
    
    return container