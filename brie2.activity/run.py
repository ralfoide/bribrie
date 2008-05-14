#! /usr/bin/env python
"""
Skeleton project file mainloop for new OLPCGames users
"""

import os
import logging 

import pygame
import pygame.font
import olpcgames
import olpcgames.pausescreen

import ralf.image_list
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
    #if pygame.font.get_init():
    #    print "Fonts", "\n".join(pygame.font.get_fonts())

    try:
        images = ralf.image_list.ImageList(log)
        images.GetImageList(os.path.join(base_dir, "tuxpaint-stamps-2006.10.21"))
    
        game = ralf.game_logic.GameLogic(log, screen, images)
        game.Loop()
    finally:
        pygame.font.quit()

if __name__ == "__main__":
    logging.basicConfig()
    main()
