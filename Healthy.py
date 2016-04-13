__author__ = 'Matej'

import pygame, random, math
from pygame.locals import *
import Utilities


class Healthy(pygame.sprite.Sprite):
    def __init__(self):

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.fitness = random.randrange(1, 3)
        self.awareness = random.randint(50, 60) + self.fitness
        self.speed = random.randint(30, 40) + self.fitness

        self.radius = self.awareness

        self.target = None
        self.tempTarget = (random.randint(self.area.left + 50, self.area.right - 50),
                           random.randint(self.area.top + 50, self.area.bottom - 50))

        self.high = False
        self.med = False
        self.low = False

        self.highFitness = Utilities.load_image('healthySuper.png')
        self.medFitness = Utilities.load_image('healthy1.png')
        self.lowFitness = Utilities.load_image('healthy2.png')

        if (self.fitness >= 10):
            self.image, self.rect = self.highFitness
            self.high = True
        elif (self.fitness >= 5):
            self.image, self.rect = self.medFitness
            self.med = True
        elif (self.fitness < 5):
            self.image, self.rect = self.lowFitness
            self.low = True

        self.rect.center = (random.randint(self.area.left + 50, self.area.right - 50),
                            random.randint(self.area.top + 50, self.area.bottom - 50))

        pygame.sprite.Sprite.__init__(self)
        self.active = True

        # print "CREATED HEALTHY WITH FITNESS " + str(self.fitness) \
        #       + " and speed " + str(self.speed) \
        #       + " and awareness " + str(self.awareness)


    def update(self, deltaTime):
        self.checkTarget()

        if self.target is not None:
            if self.target.fitness < (self.fitness / 3):
                vector = ((self.target.rect.x - self.rect.x), (self.target.rect.y - self.rect.y))
            else:
                vector = (-(self.target.rect.x - self.rect.x), -(self.target.rect.y - self.rect.y))
        elif self.rect.collidepoint(self.tempTarget[0], self.tempTarget[1]):
            randX = random.randrange(self.area.left + 50, self.area.right - 50)
            randY = random.randrange(self.area.top + 50, self.area.bottom - 50)
            # print "seeking X: " + str(randX) + " and Y: " + str(randY)
            self.tempTarget = (randX, randY)
            vector = (self.tempTarget[0] - self.rect.x, self.tempTarget[1] - self.rect.y)
        else:
            vector = (self.tempTarget[0] - self.rect.x, self.tempTarget[1] - self.rect.y)

        self.magnitude = math.sqrt((vector[0] * vector[0]) + (vector[1] * vector[1]))
        # print "healthy magnitude: " + str(self.magnitude)

        if self.tempTarget and self.magnitude < self.awareness:
            randX = random.randint(self.area.left + 6, self.area.right - 6)
            randY = random.randint(self.area.top + 32, self.area.bottom - 6)
            self.tempTarget = (randX, randY)

        if(self.magnitude < 0.5):
            self.magnitude = 1

        self.move((vector[0] / self.magnitude) * self.speed * deltaTime,
                  (vector[1] / self.magnitude) * self.speed * deltaTime)
        self.checkBounds()

    """Move function to reposition the agent. Checks whether new position is within the screen bounds"""
    def move(self, moveX, moveY):
        newpos = self.rect.move((moveX, moveY))
        if not self.area.contains(newpos):
            if self.rect.left - 6 < self.area.left or self.rect.right + 6 > self.area.right:
                moveX = -(moveX) * 2
            if self.rect.top - 32 < self.area.top or self.rect.bottom + 6 > self.area.bottom:
                moveY = -(moveY) * 2

        newpos = self.rect.move((int(moveX), int(moveY)))

        self.rect = newpos

    """Find a target within the agent's awareness radius.
    If a new potential target is closer than current target it will become the new target.
    Otherwise if no target accept any potential target."""
    def findTarget(self, col):
        colDistance = math.hypot((self.rect.x - col.rect.x), (self.rect.y - col.rect.y))
        if self.target:
            nearestT = math.hypot((self.rect.x - self.target.rect.x), (self.rect.y - self.target.rect.y))
            if abs(colDistance) < abs(nearestT):
                self.target = col
        elif abs(colDistance) < self.radius:
            self.target = col

    """Check the current target whether it is out of range or removed, if so targeted agent is un-targeted"""
    def checkTarget(self):
        if self.target:
            nearestT = math.hypot((self.rect.x - self.target.rect.x), (self.rect.y - self.target.rect.y))
            if abs(nearestT) > self.radius + 10:
                self.target = None
        if self.target and not self.target.alive():
            self.target = None

    """Additional check for out of bounds position and bring back into game"""
    def checkBounds(self):
        if self.alive():
            if not self.area.contains(self.rect):
                print "HEALTHY OOB: " + str(self.rect)

    """Increments the agent's fitness upon winning an encounter, also evolves its appearance and stats through each stage"""
    def evolve(self):
        self.fitness = self.fitness + 1
        if (self.fitness >= 10 and not self.high):
            self.image, tmp = self.highFitness
            self.awareness = self.awareness + self.fitness + 10
            self.radius = self.awareness
            self.high = True
        elif (self.fitness >= 5 and not self.med):
            self.image, tmp = self.medFitness
            self.awareness = self.awareness + self.fitness + 10
            self.radius = self.awareness
            self.med = True
