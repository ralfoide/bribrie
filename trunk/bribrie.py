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

FULLSCREEN = True  # Set to False for debugging
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


try:
    import pygame
except ImportError, e:
    Log("%s. Please install PyGame from http://www.pygame.org/", e)
    sys.exit(1)

try:
    import Numeric
    import pygame.surfarray as surfarray
except ImportError, e:
    Log("%s. Please install old-Numeric from http://numpy.scipy.org/", e)
    sys.exit(1)


class ImageList(object):
    def __init__(self):
        self._images = {}
    
    def InitImageList(self, top_dir=".", extensions=[".png"]):
        """
        Lists all files in or under the current directory.
        Returns self, the sprite.
        """
        for dirpath, dirnames, filenames in os.walk(top_dir):
            for filename in filenames:
                name, ext = os.path.splitext(filename)
                if ext in extensions:
                    self._images[os.path.join(dirpath, filename)] = None
        Log("Loaded %s images", len(self._images))
        return self

    def GetSprite(self):
        """
        Selects a random image and returns a new Sprite.
        Returns None on error.
        """
        n = len(self._images)
        assert(n > 0)
        i = random.randint(0, n - 1)
        k = self._images.keys()[i]
        img = self._images[k]
        if not img:
            Log("Load image (%d) %s", i, k)
            try:
                img = self._images[k] = pygame.image.load(k)
            except Errno, e:
                Log("Image load FAILED: %s for %s", e, k)
                return None
        if img:
            return Sprite(img)
        return None


class Sprite(object):
    def __init__(self, image):
        self._image = image

    def InitScalePos(self, horiz, sx, sy):
        """
        Setup the initial position and scale of a sprite.
        Parameters:
        - horiz (float): hint on the horizontal position of the sprite
          on the screen. 0.0=to the left, 1.0=to the right.
        - sx, sy: size of screen in pixel.
        Returns self, the sprite.
        """
        w, h = self._image.get_size()
        s = random.randint(sy / 8, sy / 4)
        if h > w:
            s = float(s) / float(h)
        else:
            s = float(s) / float(w)
        self._image = pygame.transform.rotozoom(self._image, 0, s) # angle=0
        w, h = self._image.get_size()
        x = random.randint(0, sx - w)
        y = random.randint(0, sy - h)
        self._pos = (x, y)
        self._alpha = 256
        return self

    def Dim(self):
        """
        Dim the sprite.
        Returns True if the sprite is still visible.
        """
        if self._alpha > 0:
            self._alpha -= 16
            self._ChangeAlpha(self._image, self._alpha - 1)
        return self._alpha > 0

    def _ChangeAlpha(self, surface, mask):
        """
        Masks the alpha channel of the surface.
        """
        channel = surfarray.pixels_alpha(surface)  # lock surface
        temp = Numeric.bitwise_and(channel.astype(Numeric.Int32), mask)
        channel[:] = temp.astype(Numeric.UnsignedInt8)
        del channel  # unlocks surface

    def Draw(self, dest):
        """
        Draws the sprite on the 'dest'ination surface.
        """
        dest.blit(self._image, self._pos)


class GameLogic(object):
    def __init__(self, screen, images):
        self._screen = screen
        self._images = images
        self._sx = screen.get_width()
        self._sy = screen.get_height()
        self._run = True
        self._esc_count = 0
        self._sprites = []

    def _AddSprite(self):
        """
        Get a random image from the image list and blits it at a random
        position on the screen.
        """
        sprite = self._images.GetSprite()
        if sprite:
            sprite.InitScalePos(.5, self._sx, self._sy)
            self._sprites.append(sprite)
            Log("Add Sprite: %s, Total %d", sprite, len(self._sprites))

    def _DimSprites(self):
        for s in self._sprites:
            if not s.Dim():
                self._sprites.remove(s)
                Log("Remove Sprite: %s, Total %d", s, len(self._sprites))

    def _DrawSprites(self):
        for s in self._sprites:
            s.Draw(self._screen)

    def _ProcessEvent(self, event):
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
                self._DimSprites()
                self._AddSprite()

    def _Clear(self):
        self._screen.fill(WHITE)
        pygame.draw.rect(self._screen, ORANGE, self._screen.get_rect(), 6)

    def Loop(self):
        self._Clear()
        pygame.display.flip()
        pygame.event.set_grab(True)
        while self._run:
            self._Clear()
            event = pygame.event.wait()
            self._ProcessEvent(event)
            self._DrawSprites()
            pygame.display.flip()
        pygame.event.set_grab(False)
        

def Main():
    random.seed()
    pygame.init()
    modes = FULLSCREEN and pygame.display.list_modes(32) or -1
    if FULLSCREEN and modes == -1:
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

    images = ImageList().InitImageList()

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

