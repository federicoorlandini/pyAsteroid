"""
Tests for the DI Container.

Migrated from step1_demo.py and expanded with proper assertions.
"""

import unittest

# Import test configuration (sets up paths and mocks)
import tests.conftest

from Infrastructure.di.container import DIContainer, DIError
from Infrastructure.interfaces.interfaces import IConfiguration
from Infrastructure.config.config_manager import ConfigurationManager


class FakeService:
    """A simple fake service for testing DI registration."""
    
    def __init__(self):
        self.value = "fake"


class FakeInterface:
    """A fake interface marker for testing."""
    pass


class FakeImplementation(FakeInterface):
    """A fake implementation of FakeInterface."""
    
    def __init__(self):
        self.created = True


class DIContainerRegistrationTests(unittest.TestCase):
    """Tests for DI container registration methods."""
    
    def setUp(self):
        self.container = DIContainer()
    
    def test_register_instance_makes_interface_resolvable(self):
        """register_instance() should make the interface resolvable."""
        instance = FakeService()
        self.container.register_instance(FakeInterface, instance)
        
        resolved = self.container.resolve(FakeInterface)
        
        self.assertIs(resolved, instance)
    
    def test_register_instance_returns_same_object(self):
        """register_instance() should return the exact same object (singleton)."""
        instance = FakeService()
        self.container.register_instance(FakeInterface, instance)
        
        resolved1 = self.container.resolve(FakeInterface)
        resolved2 = self.container.resolve(FakeInterface)
        
        self.assertIs(resolved1, resolved2)
        self.assertIs(resolved1, instance)
    
    def test_register_singleton_factory_creates_single_instance(self):
        """register_singleton() with factory should create only one instance."""
        call_count = 0
        
        def factory():
            nonlocal call_count
            call_count += 1
            return FakeService()
        
        self.container.register_singleton(FakeInterface, factory)
        
        resolved1 = self.container.resolve(FakeInterface)
        resolved2 = self.container.resolve(FakeInterface)
        
        self.assertIs(resolved1, resolved2)
        self.assertEqual(call_count, 1)
    
    def test_register_transient_creates_new_instance_each_time(self):
        """register_transient() should create a new instance on each resolve."""
        self.container.register_transient(FakeInterface, FakeService)
        
        resolved1 = self.container.resolve(FakeInterface)
        resolved2 = self.container.resolve(FakeInterface)
        
        self.assertIsNot(resolved1, resolved2)
        self.assertIsInstance(resolved1, FakeService)
        self.assertIsInstance(resolved2, FakeService)


class DIContainerResolveTests(unittest.TestCase):
    """Tests for DI container resolution."""
    
    def setUp(self):
        self.container = DIContainer()
    
    def test_resolve_unregistered_interface_raises_error(self):
        """resolve() should raise ValueError for unregistered abstract interface."""
        from abc import ABC, abstractmethod
        
        class UnregisteredInterface(ABC):
            @abstractmethod
            def do_something(self):
                pass
        
        with self.assertRaises((ValueError, TypeError)):
            self.container.resolve(UnregisteredInterface)
    
    def test_resolve_with_configuration_manager(self):
        """resolve() should work with real ConfigurationManager instance."""
        config = ConfigurationManager()
        self.container.register_instance(IConfiguration, config)
        
        resolved = self.container.resolve(IConfiguration)
        
        self.assertIs(resolved, config)
    
    def test_resolve_returns_functional_instance(self):
        """Resolved instance should be fully functional."""
        config = ConfigurationManager()
        self.container.register_instance(IConfiguration, config)
        
        resolved = self.container.resolve(IConfiguration)
        
        # Should be able to call methods on it
        result = resolved.get('nonexistent.key', 'default')
        self.assertEqual(result, 'default')


class DIContainerUtilityTests(unittest.TestCase):
    """Tests for DI container utility methods."""
    
    def setUp(self):
        self.container = DIContainer()
    
    def test_is_registered_returns_true_for_registered_interface(self):
        """is_registered() should return True for registered interfaces."""
        self.container.register_instance(FakeInterface, FakeService())
        
        self.assertTrue(self.container.is_registered(FakeInterface))
    
    def test_is_registered_returns_false_for_unregistered_interface(self):
        """is_registered() should return False for unregistered interfaces."""
        self.assertFalse(self.container.is_registered(FakeInterface))
    
    def test_is_registered_works_for_singleton_factory(self):
        """is_registered() should detect singleton factory registrations."""
        self.container.register_singleton(FakeInterface, FakeService)
        
        self.assertTrue(self.container.is_registered(FakeInterface))
    
    def test_is_registered_works_for_transient(self):
        """is_registered() should detect transient registrations."""
        self.container.register_transient(FakeInterface, FakeService)
        
        self.assertTrue(self.container.is_registered(FakeInterface))
    
    def test_clear_removes_all_registrations(self):
        """clear() should remove all registered services."""
        self.container.register_instance(FakeInterface, FakeService())
        self.container.register_transient(FakeService, FakeService)
        
        self.container.clear()
        
        self.assertFalse(self.container.is_registered(FakeInterface))
        self.assertFalse(self.container.is_registered(FakeService))
    
    def test_get_registered_services_returns_all_services(self):
        """get_registered_services() should list all registered services."""
        self.container.register_instance(FakeInterface, FakeService())
        self.container.register_transient(FakeService, FakeService)
        
        services = self.container.get_registered_services()
        
        self.assertEqual(len(services), 2)
    
    def test_get_registered_services_shows_lifecycle_type(self):
        """get_registered_services() should indicate singleton vs transient."""
        self.container.register_instance(FakeInterface, FakeService())
        self.container.register_transient(FakeService, FakeService)
        
        services = self.container.get_registered_services()
        
        # Find the singleton entry
        singleton_entries = [v for v in services.values() if 'singleton' in v]
        transient_entries = [v for v in services.values() if 'transient' in v]
        
        self.assertEqual(len(singleton_entries), 1)
        self.assertEqual(len(transient_entries), 1)
    
    def test_get_registered_services_empty_container(self):
        """get_registered_services() should return empty dict for new container."""
        services = self.container.get_registered_services()
        
        self.assertEqual(len(services), 0)


if __name__ == "__main__":
    unittest.main()
