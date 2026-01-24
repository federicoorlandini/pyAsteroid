import pygame.locals
from Infrastructure.interfaces.interfaces import IInputHandler


class KeyboardInputHandler(IInputHandler):
    """Handles keyboard input using dependency injection pattern"""
    
    def __init__(self, world):
        """Initialize with world dependency"""
        self._world = world
        self._exit_requested = False
    
    def handle_input(self):
        """Process keyboard input and update world state"""
        keys_pressed = pygame.key.get_pressed()
        
        # Ship rotation
        if keys_pressed[pygame.locals.K_a]:
            self._world.starship.rotate_object(-10)
        
        if keys_pressed[pygame.locals.K_d]:
            self._world.starship.rotate_object(10)
        
        # Fire bullets
        if keys_pressed[pygame.locals.K_SPACE]:
            new_bullet = self._world.starship.fire()
            if new_bullet is not None:
                self._world.add_object(new_bullet)
        
        # Exit game
        if keys_pressed[pygame.locals.K_q] or keys_pressed[pygame.locals.K_ESCAPE]:
            self._exit_requested = True
    
    def is_exit_requested(self) -> bool:
        """Check if exit was requested"""
        return self._exit_requested