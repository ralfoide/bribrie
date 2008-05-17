#! /usr/bin/env python
"""
Skeleton project file mainloop for new OLPCGames users
"""

import os
import logging 

import pygame
import olpcgames
import olpcgames.pausescreen

import ralf.resource_list
import ralf.game_logic

log = logging.getLogger("Brie2 run")
log.setLevel(logging.DEBUG)

def main():
    """
    The mainloop which is specified in the activity.py file
    
    "main" is the assumed function name
    """
    size = (800,600)
    if olpcgames.ACTIVITY:
        size = olpcgames.ACTIVITY.game_size
    screen = pygame.display.set_mode(size)
    
    clock = pygame.time.Clock()

    base_dir = os.path.dirname(__file__)

    pygame.font.init()
    pygame.mixer.init()

    try:
        resources = ralf.resource_list.ResourceList(log)
        resources.GetResources(base_dir)
    
        game = ralf.game_logic.GameLogic(log, screen, resources)
        game.Loop()
    finally:
        pygame.mixer.quit()
        pygame.font.quit()

if __name__ == "__main__":
    logging.basicConfig()
    main()
