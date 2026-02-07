# pyAsteroid

This is a simple porting of the very old Asteroid games in python. I wrote down from scratch using the pyGame library (http://www.pygame.org/hifi.html).

## How to Run

### Method 1: From Project Root (Recommended)
```bash
python main.py
```

### Method 2: From Source Directory
```bash
cd src/Main
python engines.py
```

## Game Controls
- Key A: Rotate the battleship counter-clockwise
- Key D: Rotate the battleship clockwise  
- Spacebar: Fire a bullet
- Q or ESC: Exit game

## Limitations
Now the battleship is only able to rotate and fire a bullet. There is only one asteroid coming from the left (I used it to test the code).

## Project Structure

```
pyAsteroid/
├── main.py                        # Entry point
├── README.md
├── requirements.txt
├── src/
│   ├── Main/                      # Core game modules
│   │   ├── engines.py             # Engine and World classes
│   │   ├── graphicobjects.py      # GraphicObject, StarShip, Bullet, Asteroid
│   │   ├── collisions.py          # CollisionHandler and CollisionInfo
│   │   ├── logic.py               # AsteroidGenerator
│   │   ├── display.py             # Display rendering
│   │   ├── input_handler.py       # Keyboard input handling
│   │   ├── geometrytransformation2d.py  # Vector2D, Circle, transforms
│   │   ├── angles.py              # Angle conversion utilities
│   │   ├── values.py              # Float comparison utilities
│   │   ├── constants.py           # Game constants (colors, dimensions)
│   │   └── lookuptables.py        # Sin/Cos lookup tables
│   └── Infrastructure/            # DI and configuration
│       ├── interfaces/            # Abstract interfaces (ABC)
│       ├── factories/             # SystemFactory, GameObjectFactory, PhysicsFactory
│       ├── config/                # ConfigurationManager (YAML-based)
│       └── di/                    # Dependency injection container
└── tests/                         # Test suite
    ├── __init__.py
    ├── conftest.py                # Shared test configuration and fixtures
    ├── test_angles.py
    ├── test_values.py
    ├── test_geometry.py
    ├── test_graphicobjects.py
    ├── test_world.py
    ├── test_collisions.py
    ├── test_display.py
    ├── test_asteroid_generator.py
    ├── test_input_handler.py
    ├── test_config_manager.py
    └── test_factories.py
```

## Testing

### Running Tests

From the project root:

```bash
python -m unittest discover tests/ -v
```

### Test Infrastructure

The test suite is organized under `tests/` at the project root and uses Python's built-in `unittest` framework.

#### Key Design Decisions

- **Centralized configuration** (`tests/conftest.py`): Handles Python path setup, pygame mocking, and shared test fixtures. All test files import this module first.
- **Pygame mocking**: Since tests run without a display, pygame is fully mocked via `conftest.py`. This prevents `pygame.init()` and display initialization errors.
- **Shared fixtures**: Common mock classes (`MockWorld`, `MockConfiguration`, `MockGameObjectFactory`, `MockSystemFactory`) live in `conftest.py` to avoid duplication across test files.

#### Test File Naming Convention

- All test files: `test_<module>.py`
- All test classes: `<Module>Tests(unittest.TestCase)`
- All test methods: `test_<description>`

#### Writing New Tests

1. Import test configuration first:
   ```python
   import tests.conftest
   ```

2. Import shared fixtures as needed:
   ```python
   from tests.conftest import MockWorld, MockConfiguration, create_test_vector
   ```

3. Import game modules (paths are set up by conftest):
   ```python
   from graphicobjects import GraphicObject, StarShip
   from geometrytransformation2d import Vector2D
   ```

4. Write test classes inheriting from `unittest.TestCase`:
   ```python
   class MyModuleTests(unittest.TestCase):
       def test_something_should_do_expected_behavior(self):
           # Arrange
           obj = GraphicObject()
           # Act
           result = obj.some_method()
           # Assert
           self.assertEqual(result, expected)
   ```

### Test Coverage Summary

| Module | Test File | Tests |
|--------|-----------|-------|
| `angles.py` | `test_angles.py` | 4 |
| `values.py` | `test_values.py` | 5 |
| `geometrytransformation2d.py` | `test_geometry.py` | 14 |
| `graphicobjects.py` | `test_graphicobjects.py` | 25 |
| `engines.py` (World) | `test_world.py` | 14 |
| `collisions.py` | `test_collisions.py` | 8 |
| `display.py` | `test_display.py` | 7 |
| `logic.py` | `test_asteroid_generator.py` | 11 |
| `input_handler.py` | `test_input_handler.py` | 11 |
| `config_manager.py` | `test_config_manager.py` | 28 |
| Factory classes | `test_factories.py` | 21 |
| **Total** | | **148** |
