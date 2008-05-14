#! /usr/bin/env python
"""
ImageList
"""

import os
import random
import pygame

class ImageList(object):
    def __init__(self, log):
        self._log = log
        self._images = {}
    
    def GetImageList(self, top_dir=".", extensions=[".png"]):
        """
        Lists all files in or under the current directory.
        """
        for dirpath, dirnames, filenames in os.walk(top_dir):
            for filename in filenames:
                name, ext = os.path.splitext(filename)
                if ext in extensions:
                    self._images[os.path.join(dirpath, filename)] = None
        self._log.debug("Loaded %s images", len(self._images))

    def GetImage(self):
        """
        Selects a random image and returns its pygame image
        """
        n = len(self._images)
        assert(n > 0)
        i = random.randint(0, n - 1)
        k = self._images.keys()[i]
        if self._images[k] == None:
            self._log.debug("Load image (%d) %s", i, k)
            try:
                self._images[k] = pygame.image.load(k)
            except Errno, e:
                self._log.exception("Image load FAILED: %s", k)
                return None
        return self._images[k]

    def Count(self):
        return len(self._images)