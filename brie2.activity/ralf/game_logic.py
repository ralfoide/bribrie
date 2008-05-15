#! /usr/bin/env python
"""
Game Logic
"""

import math
import time
import random
import pygame
import pygame.font
import olpcgames.pausescreen


BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
BLUE   = (  0,   0, 255)
BLUE1  = (128, 128, 255)
RED    = (255,   0,   0)
RED1   = (255, 128, 128)
ORANGE = (255, 128,   0)

class Target(object):
    def __init__(self, screen, xcenter, ycenter, radius, border, fill):
        self._screen = screen
        self._center = (xcenter, ycenter)
        self._radius = radius
        self._border = border
        self._fill = fill
        self._image = None
        self._image_pos = self._center
        self._sound = None
        self._selected = False

    def Draw(self):
        """
        Draws this target. Caller must flip buffers later on.
        """
        pygame.draw.circle(self._screen, self._selected and self._fill or WHITE,
                                                       self._center, self._radius, 0)
        pygame.draw.circle(self._screen, self._border, self._center, self._radius, 6)
        if self._image and self._image_pos:
            self._screen.blit(self._image, self._image_pos)
    
    def TestHit(self, x, y):
        """
        Returns true if the position <x,y> hits this target
        """
        x -= self._center[0]
        y -= self._center[1]
        dist = math.sqrt(x * x + y * y)
        return dist <= self._radius
 
    def Select(self, selected):
        """
        Set target.selected. Returns the true if value was changed.
        """
        old = self._selected
        self._selected = selected
        return old != selected
    
    def SetImage(self, image):
        """
        Sets the image. Can be None to remove it. Caller must flip buffers later.
        """
        self._image = image
        self._image_pos = (self._center[0] - image.get_width()  / 2,
                           self._center[1] - image.get_height() / 2)
 

class GameLogic(object):
    def __init__(self, log, screen, images):
        self._log = log
        self._screen = screen
        self._images = images
        self._sx = screen.get_width()
        self._sy = screen.get_height()
        self._scale_min = self._sy / 2
        self._scale_max = self._sy / 2
        self._run = True
        self._esc_count = 0
        
        sx4 = self._sx / 4
        sy2 = self._sy / 2
        self._targets = [ Target(screen, sx4    , sy2, sx4 * 0.6, BLUE, BLUE1),
                          Target(screen, sx4 * 3, sy2, sx4 * 0.6, RED, RED1)
                        ]
        
        self._font = None
        if pygame.font.get_init():
            self._font = pygame.font.SysFont("tahoma", self._sy / 6, bold=False, italic=False)

    def RescaleFactor(self, w, h):
        """
        Compute rescale factor for an image to blit.
        Imput: w,h is the size of the image in pixels.
        This takes the largest dimension and compute a factor so that it
        fit in the random range[scale_min, scale_max].
        """
        if w > h:
            h = w
        if self._scale_min != self._scale_max:
            s = random.randint(self._scale_min, self._scale_max)
        else:
            s = self._scale_min
        return float(s) / float(h)

    def SetRandomImage(self):
        """
        Get a random image from the image list and blits it at a random
        position on the screen.
        """
        img1 = self._images.GetImage()
        if img1 is None:
            return
        img2 = self._images.GetImage()
        while img1 == img2 and self._images.Count() > 1:
            img2 = self._images.GetImage()
        self.AssignImage(img1, self._targets[0])
        self.AssignImage(img2, self._targets[1])

    def AssignImage(self, img, target):        
        w, h = img.get_size()
        s = self.RescaleFactor(w, h)
        img = pygame.transform.rotozoom(img, 0, s)  # angle=0, scale=s
        target.SetImage(img)

    def ProcessEvent(self, event):
        # Log("Event: %s", repr(event))
        if event.type == pygame.QUIT:
            self._run = False
        elif event.type == pygame.KEYDOWN:
            self.ProcessKey(event)
        elif event.type == pygame.MOUSEMOTION:
            self.ProcessMouseMotion(event)

    def ProcessKey(self, event):
        if event.key == 27:
            self._esc_count += 1
            self.RedrawAll()
            if self._esc_count == 5:
                self._run = False
            else:
                self._log.debug("Ready to quit... %d more", 5 - self._esc_count)
        else:
            self._esc_count = 0
            self.SetRandomImage()
            self.RedrawAll()

    def ProcessMouseMotion(self, event):
        x = event.pos[0]
        y = event.pos[1]
        changed = False
        for t in self._targets:
            changed = changed or t.Select(t.TestHit(x, y))
        if changed:
            self.RedrawAll()

    def DrawTargets(self):
        for t in self._targets:
            t.Draw()
            
    def DrawEscCount(self):
        if self._esc_count and self._font:
            surf = self._font.render(str(self._esc_count),
                                     True, # antialias 
                                     RED)
            x = (self._sx - surf.get_width()) / 2
            y = (self._sy - surf.get_height()) / 2
            self._screen.blit(surf, (x, y))

    def RedrawAll(self):
        self._screen.fill(WHITE)
        pygame.draw.rect(self._screen, ORANGE, self._screen.get_rect(), 6)
        self.DrawTargets()
        self.DrawEscCount()
        pygame.display.flip()

    def Loop(self):
        self._run = True
        self.RedrawAll()
        while self._run:
            # Event-management loop with support for pausing after X seconds (20 here)
            events = olpcgames.pausescreen.get_events()
            if events:
                for event in events:
                    # self._log.debug("Event: %s", event)
                    self.ProcessEvent(event)
            else:
                time.sleep(0.1);

