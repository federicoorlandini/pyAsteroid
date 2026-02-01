"""
Tests for the ConfigurationManager class.
"""

import unittest
import unittest.mock
import tempfile
import os

# Import test configuration (sets up paths and mocks)
import tests.conftest

from Infrastructure.config.config_manager import ConfigurationManager


class ConfigurationManagerTests(unittest.TestCase):
    """Tests for ConfigurationManager class."""
    
    def _create_temp_config(self, content):
        """Helper to create a temporary config file."""
        fd, path = tempfile.mkstemp(suffix='.yaml')
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path
    
    def _cleanup_temp_file(self, path):
        """Helper to clean up temporary file."""
        if os.path.exists(path):
            os.unlink(path)
    
    # --- Loading Tests ---
    
    def test_load_valid_yaml_config(self):
        """Should load valid YAML configuration."""
        config_content = """
display:
  width: 800
  height: 600
game:
  fps: 60
"""
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertEqual(config.get('display.width'), 800)
            self.assertEqual(config.get('display.height'), 600)
        finally:
            self._cleanup_temp_file(path)
    
    def test_load_missing_config_file_returns_empty(self):
        """Should return empty config when file doesn't exist."""
        config = ConfigurationManager('/nonexistent/path/config.yaml')
        # Should not raise, returns empty config
        self.assertIsNone(config.get('any.key'))
    
    def test_load_malformed_yaml_returns_empty(self):
        """Should return empty config when YAML is malformed."""
        config_content = """
invalid yaml: [unclosed bracket
"""
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            # Should not raise, returns empty config
            self.assertIsNone(config.get('any.key'))
        finally:
            self._cleanup_temp_file(path)
    
    def test_load_empty_yaml_file(self):
        """Should handle empty YAML file."""
        path = self._create_temp_config("")
        try:
            config = ConfigurationManager(path)
            self.assertIsNone(config.get('any.key'))
        finally:
            self._cleanup_temp_file(path)
    
    # --- get() Tests ---
    
    def test_get_with_dot_notation(self):
        """Should access nested values using dot notation."""
        config_content = """
level1:
  level2:
    level3: deep_value
"""
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertEqual(config.get('level1.level2.level3'), 'deep_value')
        finally:
            self._cleanup_temp_file(path)
    
    def test_get_missing_key_returns_default(self):
        """Should return default when key doesn't exist."""
        config_content = "existing_key: value"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            result = config.get('nonexistent.key', 'default_value')
            self.assertEqual(result, 'default_value')
        finally:
            self._cleanup_temp_file(path)
    
    def test_get_empty_key_returns_default(self):
        """Should return default when key is empty string."""
        config_content = "key: value"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            result = config.get('', 'default')
            self.assertEqual(result, 'default')
        finally:
            self._cleanup_temp_file(path)
    
    def test_get_top_level_key(self):
        """Should get top-level keys without dot notation."""
        config_content = "top_level: top_value"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertEqual(config.get('top_level'), 'top_value')
        finally:
            self._cleanup_temp_file(path)
    
    # --- get_int() Tests ---
    
    def test_get_int_with_valid_integer(self):
        """Should return integer value."""
        config_content = "count: 42"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertEqual(config.get_int('count'), 42)
        finally:
            self._cleanup_temp_file(path)
    
    def test_get_int_with_string_number(self):
        """Should convert string number to integer."""
        config_content = 'count: "100"'
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertEqual(config.get_int('count'), 100)
        finally:
            self._cleanup_temp_file(path)
    
    def test_get_int_with_invalid_value_returns_default(self):
        """Should return default when value can't be converted."""
        config_content = "count: not_a_number"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertEqual(config.get_int('count', 99), 99)
        finally:
            self._cleanup_temp_file(path)
    
    # --- get_float() Tests ---
    
    def test_get_float_with_valid_float(self):
        """Should return float value."""
        config_content = "rate: 3.14"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertAlmostEqual(config.get_float('rate'), 3.14)
        finally:
            self._cleanup_temp_file(path)
    
    def test_get_float_with_integer(self):
        """Should convert integer to float."""
        config_content = "rate: 5"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertEqual(config.get_float('rate'), 5.0)
        finally:
            self._cleanup_temp_file(path)
    
    def test_get_float_with_invalid_value_returns_default(self):
        """Should return default when value can't be converted."""
        config_content = "rate: invalid"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertEqual(config.get_float('rate', 1.5), 1.5)
        finally:
            self._cleanup_temp_file(path)
    
    # --- get_bool() Tests ---
    
    def test_get_bool_with_true_value(self):
        """Should return True for boolean true."""
        config_content = "enabled: true"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertTrue(config.get_bool('enabled'))
        finally:
            self._cleanup_temp_file(path)
    
    def test_get_bool_with_false_value(self):
        """Should return False for boolean false."""
        config_content = "enabled: false"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertFalse(config.get_bool('enabled'))
        finally:
            self._cleanup_temp_file(path)
    
    def test_get_bool_with_string_yes(self):
        """Should return True for string 'yes'."""
        config_content = 'enabled: "yes"'
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertTrue(config.get_bool('enabled'))
        finally:
            self._cleanup_temp_file(path)
    
    def test_get_bool_with_string_on(self):
        """Should return True for string 'on'."""
        config_content = 'enabled: "on"'
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertTrue(config.get_bool('enabled'))
        finally:
            self._cleanup_temp_file(path)
    
    # --- get_color() Tests ---
    
    def test_get_color_with_list(self):
        """Should return color tuple from list."""
        config_content = "color: [255, 128, 64]"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertEqual(config.get_color('color'), (255, 128, 64))
        finally:
            self._cleanup_temp_file(path)
    
    def test_get_color_with_invalid_returns_default(self):
        """Should return default when color is invalid."""
        config_content = "color: not_a_color"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            default = (100, 100, 100)
            self.assertEqual(config.get_color('color', default), default)
        finally:
            self._cleanup_temp_file(path)
    
    def test_get_color_with_short_list_returns_default(self):
        """Should return default when color list is too short."""
        config_content = "color: [255, 128]"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            default = (200, 200, 200)
            self.assertEqual(config.get_color('color', default), default)
        finally:
            self._cleanup_temp_file(path)
    
    # --- get_vertexes() Tests ---
    
    def test_get_vertexes_with_valid_list(self):
        """Should return list of vertex tuples."""
        config_content = """
vertexes:
  - [10, 20]
  - [30, 40]
  - [50, 60]
"""
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            result = config.get_vertexes('vertexes')
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0], (10, 20))
            self.assertEqual(result[1], (30, 40))
        finally:
            self._cleanup_temp_file(path)
    
    def test_get_vertexes_with_missing_key_returns_default(self):
        """Should return default when key is missing."""
        config_content = "other: value"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            default = [(1, 2), (3, 4)]
            result = config.get_vertexes('vertexes', default)
            self.assertEqual(result, default)
        finally:
            self._cleanup_temp_file(path)
    
    # --- has() Tests ---
    
    def test_has_returns_true_for_existing_key(self):
        """Should return True when key exists."""
        config_content = "existing: value"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertTrue(config.has('existing'))
        finally:
            self._cleanup_temp_file(path)
    
    def test_has_returns_false_for_missing_key(self):
        """Should return False when key doesn't exist."""
        config_content = "existing: value"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertFalse(config.has('nonexistent'))
        finally:
            self._cleanup_temp_file(path)
    
    def test_has_with_nested_key(self):
        """Should work with nested keys."""
        config_content = """
parent:
  child: value
"""
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertTrue(config.has('parent.child'))
            self.assertFalse(config.has('parent.nonexistent'))
        finally:
            self._cleanup_temp_file(path)
    
    # --- reload() Tests ---
    
    def test_reload_updates_config(self):
        """Should reload configuration from file."""
        config_content = "value: original"
        path = self._create_temp_config(config_content)
        try:
            config = ConfigurationManager(path)
            self.assertEqual(config.get('value'), 'original')
            
            # Update the file
            with open(path, 'w') as f:
                f.write("value: updated")
            
            config.reload()
            self.assertEqual(config.get('value'), 'updated')
        finally:
            self._cleanup_temp_file(path)


if __name__ == "__main__":
    unittest.main()
