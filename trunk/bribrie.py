#!/usr/bin/python
#------------------------------------------------------------------------------|
"""
Bribrie, Babies Random Image Entertainment

Copyright (c) 2007, Ralfoide
License: GPL
"""

import os
import sys
import random
import traceback

try:
    import pygame
except ImportError, e:
    print >> sys.stderr, \
          "\n%s\nPlease install PyGame from http://www.pygame.org/" % e
    sys.exit(1)

DEFAULT_SIZE = (640, 480)
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
BLUE   = (  0,   0, 255)
RED    = (255,   0,   0)
ORANGE = (255, 128,   0)

LOGS = [ file("_log", "w") ]
if not "w" in os.path.basename(sys.executable):
    LOGS.append(sys.stderr)  # No stderr under pythonw

def Log(msg, *params):
    for log in LOGS:
        print >> log, msg % params

class ImageList(object):
    def __init__(self):
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
        Log("Loaded %s images", len(self._images))

    def GetImage(self):
        """
        Selects a random image and returns its pygame image
        """
        n = len(self._images)
        assert(n > 0)
        i = random.randint(0, n - 1)
        k = self._images.keys()[i]
        if self._images[k] == None:
            Log("Load image (%d) %s", i, k)
            try:
                self._images[k] = pygame.image.load(k)
            except Errno, e:
                Log("Image load FAILED: %s for %s", e, k)
                return None
        return self._images[k]


class GameLogic(object):
    def __init__(self, screen, images):
        self._screen = screen
        self._images = images
        self._sx = screen.get_width()
        self._sy = screen.get_height()
        self._scale_min = self._sy / 8
        self._scale_max = self._sy / 4
        self._run = True
        self._esc_count = 0

    def RescaleFactor(self, w, h):
        """
        Compute rescale factor for an image to blit.
        Imput: w,h is the size of the image in pixels.
        This takes the largest dimension and compute a factor so that it
        fit in the random range[scale_min, scale_max].
        """
        if w > h:
            h = w
        s = random.randint(self._scale_min, self._scale_max)
        return float(s) / float(h)

    def InsertRandomImage(self):
        """
        Get a random image from the image list and blits it at a random
        position on the screen.
        """
        img = self._images.GetImage()
        if img is None:
            return
        w, h = img.get_size()
        s = self.RescaleFactor(w, h)
        img = pygame.transform.rotozoom(img, 0, s)  # angle=0, scale=s
        w, h = img.get_size()
        x = random.randint(0, self._sx - w)
        y = random.randint(0, self._sy - h)
        self._screen.blit(img, (x, y))

    def ProcessEvent(self, event):
        # Log("Event: %s", repr(event))
        if event.type == pygame.QUIT:
            self._run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 27:
                self._esc_count += 1
                if self._esc_count == 5:
                    self._run = False
                else:
                    Log("Ready to quit... %d more", 5 - self._esc_count)
            else:
                self._esc_count = 0
                self.InsertRandomImage()
                pygame.display.flip()

    def Clear(self):
        self._screen.fill(WHITE)
        pygame.draw.rect(self._screen, ORANGE, self._screen.get_rect(), 6)
        pygame.display.flip()

    def Loop(self):
        self.Clear()
        pygame.event.set_grab(True)
        while self._run:
            event = pygame.event.wait()
            self.ProcessEvent(event)
        pygame.event.set_grab(False)
        

def Main():
    random.seed()
    pygame.init()
    modes = pygame.display.list_modes(16)
    if modes == -1:
        Log("No 16 bit options...")
        modes = pygame.display.list_modes()
    if not isinstance(modes, list) or len(modes) == 0:
        Log("Revert to default windowed display %s", DEFAULT_SIZE)
        pygame.display.set_mode(DEFAULT_SIZE)
    else:
        Log("Switching to fullscreen mode %s", modes[0])
        pygame.display.set_mode(modes[0], pygame.FULLSCREEN)
    pygame.display.set_caption("Brie")
    screen = pygame.display.get_surface()

    images = ImageList()
    images.GetImageList()

    g = GameLogic(screen, images)
    g.Loop()
    pygame.quit()
    return 0

if __name__ == "__main__":
    try:
        Main()
    except Exception, e:
        Log("Unhandled top-level exception: %s", e)
        for log in LOGS:
            traceback.print_exc(file=log)
        raise

