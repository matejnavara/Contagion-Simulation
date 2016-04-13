__author__ = 'Matej'

import os
import pygame

def load_image(name):
    fullname = os.path.join('Assets', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Error loading image:', name
        raise SystemExit, message
    image = image.convert()

    return image, image.get_rect()

def numberEntry(choice):
    num = int(choice)
    if num < 1:
        print("Choice too low, minimum of 1 chosen")
        return 1
    elif num > 500:
        print("Choice too high, maximum of 500 chosen")
        return 500
    else:
        return num


def boolEntry(choice):
    yesno = False
    if choice.lower() in ("y","yes"):
        yesno = True
    return yesno
