"""
Lightweight Dependency Injection Container for pyAsteroid

This module provides a simple DI container for managing dependencies and promoting
loose coupling between components. It supports both singleton and transient
lifetimes with automatic dependency resolution.
"""

from typing import Dict, Any, Callable, Type, TypeVar, Union, Optional
from inspect import signature, Parameter
import inspect


T = TypeVar('T')


class DIContainer:
    """
    A lightweight dependency injection container.
    
    Supports registration of services with singleton or transient lifetime
    and automatic dependency resolution through constructor injection.
    """
    
    def __init__(self):
        """Initialize the DI container."""
        self._singletons: Dict[Type, Any] = {}
        self._singletons_factories: Dict[Type, Callable] = {}
        self._transients: Dict[Type, Callable] = {}
        self._instances: Dict[Type, Any] = {}
    
    def register_singleton(self, interface: Type[T], implementation: Union[Callable[[], T], Type[T]], instance: Optional[T] = None) -> None:
        """
        Register a singleton service.
        
        Args:
            interface: The interface type or class to register
            implementation: The implementation class or factory function
            instance: Optional pre-created instance (for external instances)
            
        Examples:
            container.register_singleton(IRepository, SqlRepository)
            container.register_singleton(IConfig, lambda: ConfigManager())
            container.register_singleton(IService, external_service_instance, instance=external_service_instance)
        """
        if instance is not None:
            self._singletons[interface] = instance
        else:
            self._singletons_factories[interface] = implementation
    
    def register_transient(self, interface: Type[T], implementation: Union[Callable[[], T], Type[T]]) -> None:
        """
        Register a transient service (new instance created each time).
        
        Args:
            interface: The interface type or class to register
            implementation: The implementation class or factory function
            
        Examples:
            container.register_transient(IRepository, SqlRepository)
            container.register_transient(ILogger, lambda: Logger())
        """
        self._transients[interface] = implementation
    
    def register_instance(self, interface: Type[T], instance: T) -> None:
        """
        Register a pre-created instance as singleton.
        
        Args:
            interface: The interface type or class
            instance: The pre-created instance
            
        Examples:
            container.register_instance(IConfig, config_instance)
        """
        self._singletons[interface] = instance
    
    def resolve(self, interface: Type[T]) -> T:
        """
        Resolve a dependency and return an instance.
        
        Args:
            interface: The interface type or class to resolve
            
        Returns:
            An instance of the requested type
            
        Raises:
            ValueError: If the interface is not registered
            Exception: If dependency resolution fails
        """
        # Check if we already have a singleton instance
        if interface in self._singletons:
            return self._singletons[interface]
        
        # Check if it's a registered singleton factory
        if interface in self._singletons_factories:
            instance = self._create_instance(self._singletons_factories[interface])
            self._singletons[interface] = instance
            return instance
        
        # Check if it's a registered transient
        if interface in self._transients:
            return self._create_instance(self._transients[interface])
        
        # Check if it's a concrete class that can be auto-registered
        if inspect.isclass(interface) and not self._is_interface_like(interface):
            # Try to auto-register as transient
            self._transients[interface] = interface
            return self._create_instance(interface)
        
        raise ValueError(f"Interface {interface} is not registered in the container")
    
    def _create_instance(self, factory_or_class: Union[Callable, Type]) -> Any:
        """
        Create an instance using the factory or class, resolving dependencies.
        
        Args:
            factory_or_class: The factory function or class to instantiate
            
        Returns:
            The created instance
        """
        # Handle the case where we passed an instance instead of a callable
        if not callable(factory_or_class):
            return factory_or_class
            
        # Get the signature to analyze parameters
        sig = signature(factory_or_class)
        
        # Build dependency arguments
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            
            # Try to resolve the parameter type as a dependency
            param_type = param.annotation
            if param_type != inspect.Parameter.empty:
                try:
                    kwargs[param_name] = self.resolve(param_type)
                except ValueError:
                    # If the dependency is not registered, check if it has a default
                    if param.default != inspect.Parameter.empty:
                        continue
                    else:
                        # Raise an error with more context
                        raise ValueError(f"Cannot resolve dependency '{param_type}' for parameter '{param_name}' of {factory_or_class}")
            elif param.default == inspect.Parameter.empty:
                # Required parameter without type annotation
                raise ValueError(f"Parameter '{param_name}' of {factory_or_class} requires type annotation for dependency injection")
        
        # Create the instance with resolved dependencies
        return factory_or_class(**kwargs)
    
    def _is_interface_like(self, cls: Type) -> bool:
        """
        Determine if a class looks like an interface (abstract base class).
        
        Args:
            cls: The class to check
            
        Returns:
            True if the class appears to be an interface
        """
        # Check if it has abstract methods (ABC)
        if hasattr(cls, '__abstractmethods__') and cls.__abstractmethods__:
            return True
        
        # Check if it has only abstract-like method signatures
        # This is a heuristic for simple interface classes
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith('_'):
                # If it has any concrete method implementations, it's likely not an interface
                if not (getattr(attr_value, '__isabstractmethod__', False)):
                    return False
        
        # If it has methods and they all look abstract, treat as interface
        method_count = sum(1 for attr_name, attr_value in cls.__dict__.items() 
                          if callable(attr_value) and not attr_name.startswith('_'))
        return method_count > 0
    
    def is_registered(self, interface: Type) -> bool:
        """
        Check if an interface is registered in the container.
        
        Args:
            interface: The interface type to check
            
        Returns:
            True if registered, False otherwise
        """
        return (interface in self._singletons or 
                interface in self._singletons_factories or 
                interface in self._transients)
    
    def clear(self) -> None:
        """
        Clear all registered services and instances.
        """
        self._singletons.clear()
        self._singletons_factories.clear()
        self._transients.clear()
        self._instances.clear()
    
    def get_registered_services(self) -> Dict[str, str]:
        """
        Get a dictionary of all registered services for debugging.
        
        Returns:
            Dictionary mapping service names to their lifecycle type
        """
        services = {}
        for interface in self._singletons:
            services[str(interface)] = "singleton (instance)"
        for interface in self._singletons_factories:
            services[str(interface)] = "singleton (factory)"
        for interface in self._transients:
            services[str(interface)] = "transient"
        return services


class DIError(Exception):
    """Custom exception for dependency injection errors."""
    pass