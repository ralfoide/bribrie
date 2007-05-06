#!/bin/bash
#------------------------------------------------------------------------------|
"""
Bribrie, Babies Random Image Entertainment

Copyright (c) 2007, Ralfoide
License: GPL
"""

import os
import sys
import pygame
import random

class ImageList:
    def __init__(self):
        _images = {}
    
    def GetImageList(self, top_dir=".", extensions=[".png"]):
        """
        Lists all files in or under the current directory.
        """
        for dirpath, dirnames, filenames in os.walk(top_dir):
            for filename in filenames:
                name, ext = os.path.splitext(filename)
                if ext in extensions:
                    _images[os.path.join(dirpath, filename)] = None

    def GetImage(self):
        """
        Select a random image and return it's pygame image
        """
        assert(len(_images) > 0)
        k = random.randint(0, len(_images) - 1)
        k = _images.keys()[k]
        if _images[k] == None:
            _images[k] = pygame.image.load(k)
        return _images[k]
        

def Events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def Loop(images):
    while True:
        Events()
        

def Main():
    random.seed()
    pygame.init()
    pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Brie")
    screen = pygame.display.get_surface()

    images = ImageList()
    images.GetImageList()

    Loop(images)

    pygame.quit()
    return 0

if __name__ == "__main__":
    Main()
