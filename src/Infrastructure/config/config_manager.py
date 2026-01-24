"""
Configuration Manager for pyAsteroid

This module provides a centralized way to load and manage game configuration
from YAML files, with support for default values and nested key access.
"""

import yaml
import os
from typing import Dict, Any, Optional, Union


class ConfigurationManager:
    """
    Manages game configuration loaded from YAML files.
    
    Provides methods to access configuration values with default fallbacks
    and supports nested key access using dot notation.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the YAML configuration file. 
                        If None, uses default path.
        """
        if config_path is None:
            # Default to the game_config.yaml in the same directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, 'game_config.yaml')
        
        self._config_path = config_path
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Returns:
            Dictionary containing the configuration data.
            
        Raises:
            FileNotFoundError: If the config file doesn't exist.
            yaml.YAMLError: If the YAML file is malformed.
        """
        try:
            with open(self._config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            # Return empty config if file doesn't exist
            # This allows the game to run with hardcoded defaults
            print(f"Warning: Config file not found at {self._config_path}. Using defaults.")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML config: {e}. Using defaults.")
            return {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Configuration key using dot notation (e.g., 'display.width')
            default: Default value if key is not found
            
        Returns:
            The configuration value or default if not found
            
        Examples:
            config.get('display.width')  # Returns 500
            config.get('game.starship.reload_counter')  # Returns 10
            config.get('nonexistent.key', 'default')  # Returns 'default'
        """
        if not key:
            return default
            
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_color(self, key: str, default: tuple = (255, 255, 255)) -> tuple:
        """
        Get a color configuration as a tuple.
        
        Args:
            key: Configuration key for the color
            default: Default color as RGB tuple
            
        Returns:
            Color as RGB tuple
        """
        color_list = self.get(key, default)
        if isinstance(color_list, list) and len(color_list) >= 3:
            return tuple(color_list[:3])
        elif isinstance(color_list, tuple) and len(color_list) >= 3:
            return color_list[:3]
        else:
            return default
    
    def get_vertexes(self, key: str, default: list = None) -> list:
        """
        Get vertex configuration as a list of coordinate tuples.
        
        Args:
            key: Configuration key for vertexes
            default: Default vertex list
            
        Returns:
            List of (x, y) tuples
        """
        vertex_list = self.get(key, default or [])
        if isinstance(vertex_list, list):
            return [(v[0], v[1]) if isinstance(v, list) and len(v) >= 2 else v 
                   for v in vertex_list]
        return default or []
    
    def get_int(self, key: str, default: int = 0) -> int:
        """
        Get a configuration value as integer.
        
        Args:
            key: Configuration key
            default: Default integer value
            
        Returns:
            Integer value or default
        """
        value = self.get(key, default)
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """
        Get a configuration value as float.
        
        Args:
            key: Configuration key
            default: Default float value
            
        Returns:
            Float value or default
        """
        value = self.get(key, default)
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        Get a configuration value as boolean.
        
        Args:
            key: Configuration key
            default: Default boolean value
            
        Returns:
            Boolean value or default
        """
        value = self.get(key, default)
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            return value.lower() in ('true', 'yes', '1', 'on')
        else:
            return bool(value)
    
    def reload(self) -> None:
        """
        Reload the configuration from file.
        """
        self._config = self._load_config()
    
    def has(self, key: str) -> bool:
        """
        Check if a configuration key exists.
        
        Args:
            key: Configuration key to check
            
        Returns:
            True if key exists, False otherwise
        """
        return self.get(key) is not None