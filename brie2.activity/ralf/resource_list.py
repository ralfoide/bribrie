#! /usr/bin/env python
"""
ResourceList
"""

import os
import random
import pygame

_MAP = {
    "butterfly": "cricket",
    "clownfish": "bubbles",
    "edward_bear" : "cat",
    "fire_engine" : "alarm",
    "giraffe" : "horse",
    "ladybug" : "cricket",
    "magellanic_penguin" : "",
    "rooster" : "birds",
    "rubberduck" : "birds",
    "seahorse" : "bubbles",
    "snail" : "cricket",
    "tux" : "carhorn",
    "zebra" : "horse"
    } 


class ResourceInfo(object):
    def __init__(self, image_path, sound_path):
        self._image_path = image_path
        self._sound_path = sound_path
        self._py_image = None
        self._py_sound = None

    def GetPyImage(self):
        if not self._py_image and self._image_path:
            try:
                self._py_image = pygame.image.load(self._image_path)
            except Errno, e:
                self._log.exception("Image load Failed: %s", k)
        return self._py_image

    def GetPySound(self):
        if not self._py_sound and self._sound_path:
            try:
                self._py_sound = pygame.mixer.Sound(self._sound_path)
            except Errno, e:
                self._log.exception("Sound load Failed: %s", k)
        return self._py_sound
        

class ResourceList(object):
    def __init__(self, log):
        self._log = log
        self._resources = []

    def GetResources(self, top_dir="."):
        global _MAP
        images = self._GetFiles(top_dir, extensions=[".png"])
        sounds = self._GetFiles(top_dir, extensions=[".wav"])
        for i in images:
            img_name = os.path.splitext(os.path.basename(i))[0]
            if img_name in _MAP:
                v = _MAP[img_name]
                for s in sounds:
                    snd_name = os.path.splitext(os.path.basename(s))[0]
                    if snd_name == v:
                        self._resources.append(ResourceInfo(i, s))
                        break
    
    def _GetFiles(self, top_dir, extensions):
        """
        Lists all files in or under the current directory that match
        any of the given extension list.
        """
        files = []
        for dirpath, dirnames, filenames in os.walk(top_dir):
            for filename in filenames:
                name, ext = os.path.splitext(filename)
                if ext in extensions:
                    files.append(os.path.join(dirpath, filename))
        return files

    def GetResource(self):
        """
        Selects a random resource and returns a ResourceInfo with
        its pygame image and pygame sound.
        """
        n = len(self._resources)
        assert(n > 0)
        i = random.randint(0, n - 1)
        return self._resources[i]

    def Count(self):
        return len(self._resources)