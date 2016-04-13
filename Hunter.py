__author__ = 'Matej'

import pygame, random, math
from pygame.locals import *
import Utilities

class Hunter(pygame.sprite.Sprite):

    baseSpeed = 50
    baseAwareness = 50

    def __init__(self):
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.fitness = random.randint(5,15)
        self.awareness = 70 + self.fitness
        self.speed = 50 + self.fitness
        self.radius = self.awareness
        # self.theta = 0
        # self.thetaVelocity = 1

        self.active = True
        self.target = None

        self.med = False
        self.high = False

        self.medFitness = Utilities.load_image('hunter2.png')
        self.highFitness = Utilities.load_image('hunter1.png')

        if(self.fitness >= 30):
            self.image, self.rect = self.highFitness
            self.high = True
        elif(self.fitness >= 5):
            self.image, self.rect = self.medFitness
            self.med = True

        self.tempTarget = (self.area.centerx, self.area.centery)

        self.rect.move(50,50)
        pygame.sprite.Sprite.__init__(self)

        print "CREATED HUNTER WITH FITNESS " + str(self.fitness) + " and speed " + str(self.speed) + " and awareness " + str(self.awareness)


    def update(self, deltaTime):

        self.checkTarget()

        #when hunter has a target the vector aims towards the target's position
        if self.target is not None:
            vector = ( self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y)
        elif self.rect.collidepoint(self.tempTarget[0], self.tempTarget[1]):
            randX = random.randint(self.area.left + 50, self.area.right - 50)
            randY = random.randint(self.area.top + 50, self.area.bottom - 50)
            print "seeking X: " + str(randX) + " and Y: " + str(randY)
            self.tempTarget = (randX, randY)
            vector = ( self.tempTarget[0] - self.rect.x, self.tempTarget[1] - self.rect.y)
        else:
            vector = ( self.tempTarget[0] - self.rect.x, self.tempTarget[1] - self.rect.y)

        magnitude = math.sqrt((vector[0] * vector[0]) + (vector[1] * vector[1]))
        if(self.tempTarget and magnitude < self.awareness):
            randX = random.randint(self.area.left+6, self.area.right - 6)
            randY = random.randint(self.area.top + 32, self.area.bottom - 6)
            self.tempTarget = (randX, randY)

        self.move((vector[0] / magnitude) * self.speed * deltaTime, (vector[1] / magnitude) * self.speed * deltaTime)


    def move(self, moveX, moveY):
        newpos = self.rect.move((moveX, moveY))
        if not self.area.contains(newpos):
            if self.rect.left - 6 < self.area.left or self.rect.right + 6 > self.area.right:
                moveX = -(moveX*2)
            if self.rect.top - 32 < self.area.top or self.rect.bottom + 6 > self.area.bottom:
                moveY = -(moveY*2)

        newpos = self.rect.move((moveX, moveY))

        self.rect = newpos

    def findTarget(self, col):
        if self.target:
            nearestT = math.hypot((self.rect.x - self.target.rect.x), (self.rect.y - self.target.rect.y))
            colDistance = math.hypot((self.rect.x - col.rect.x), (self.rect.y - col.rect.y))
            if abs(colDistance) < abs(nearestT):
                self.target = col
        else:
            self.target = col


    def checkTarget(self):
        if self.target:
            nearestT = math.hypot((self.rect.x - self.target.rect.x), (self.rect.y - self.target.rect.y))
            if abs(nearestT) > self.radius + 10:
                self.target = None
        if self.target and not self.target.alive():
            self.target = None

    def evolve(self):
        if(self.fitness >= 20 and not self.high):
            self.image, tmp = self.highFitness
            self.high = True
        elif(self.fitness >= 10 and not self.med):
            self.image, tmp = self.medFitness
            self.med = True
        elif(self.fitness < 20):
            self.fitness = self.fitness + 1
