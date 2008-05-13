#! /usr/bin/env python
"""
Game Logic
"""

import random
import pygame
import olpcgames.pausescreen


BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
BLUE   = (  0,   0, 255)
RED    = (255,   0,   0)
ORANGE = (255, 128,   0)

class Target(object):
    def __init__(self, screen, xcenter, ycenter, radius, color):
        self._screen = screen
        self._center = (xcenter, ycenter)
        self._radius = radius
        self._color = color
        self._image = None
        self._sound = None
    
    def Draw(self):
        pygame.draw.circle(self._screen, self._color, self._center, self._radius, 6)
 

class GameLogic(object):
    def __init__(self, log, screen, images):
        self._log = log
        self._screen = screen
        self._images = images
        self._sx = screen.get_width()
        self._sy = screen.get_height()
        self._scale_min = self._sy / 8
        self._scale_max = self._sy / 4
        self._run = True
        self._esc_count = 0
        
        sx4 = self._sx / 4
        sy2 = self._sy / 2
        self._targets = [
             Target(screen, sx4    , sy2, sx4 * 0.6, BLUE),
             Target(screen, sx4 * 3, sy2, sx4 * 0.6, RED),
             ]

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
                    self._log.debug("Ready to quit... %d more", 5 - self._esc_count)
            else:
                self._esc_count = 0
                self.InsertRandomImage()
                pygame.display.flip()

    def DrawTargets(self):
        for t in self._targets:
            t.Draw()

    def Clear(self):
        self._screen.fill(WHITE)
        pygame.draw.rect(self._screen, ORANGE, self._screen.get_rect(), 6)
        self.DrawTargets()
        pygame.display.flip()

    def Loop(self):
        self._run = True
        self.Clear()
        while self._run:
            # Event-management loop with support for pausing after X seconds (20 here)
            events = olpcgames.pausescreen.get_events()
            if events:
                for event in events:
                    self._log.debug("Event: %s", event)
                    self.ProcessEvent(event)

