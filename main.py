#!/usr/bin/env python3
"""
pyAsteroid - A simple Asteroid game implementation

This is the main entry point for the pyAsteroid game.
Run this file from the project root directory with: python main.py
"""

import sys
import os

def setup_python_path():
    """Add src directory to Python path for proper module imports"""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Add src/Main directory to Python path for direct imports
    src_main_dir = os.path.join(script_dir, 'src', 'Main')
    if src_main_dir not in sys.path:
        sys.path.insert(0, src_main_dir)

def main():
    """Main entry point for the game"""
    try:
        # Setup Python path for imports
        setup_python_path()
        
        # Import and run the game
        from engines import main as game_main
        game_main()
        
    except ImportError as e:
        print(f"Error importing game modules: {e}")
        print("Make sure you're running this from the project root directory")
        print("Or try running: cd src/Main && python engines.py")
        sys.exit(1)
    except Exception as e:
        print(f"Error running game: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()