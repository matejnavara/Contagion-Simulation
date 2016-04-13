__author__ = 'Matej'

import pygame, random, math
from pygame.locals import *
import Utilities

class Infected(pygame.sprite.Sprite):

    def __init__(self, fitness=2):

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.fitness = fitness
        self.awareness = random.randint(50,60) + self.fitness
        self.speed = random.randint(30,40) + self.fitness

        self.radius = self.awareness

        self.target = None
        self.tempTarget = (random.randint(self.area.left + 50, self.area.right - 50),random.randint(self.area.top + 50, self.area.bottom - 50))

        self.high = False
        self.med = False
        self.low = False

        self.highFitness = Utilities.load_image('infectedSuper.png')
        self.medFitness = Utilities.load_image('infected1.png')
        self.lowFitness = Utilities.load_image('infected2.png')

        if(self.fitness >= 10):
            self.image, self.rect = self.highFitness
        elif(self.fitness >= 5):
            self.image, self.rect = self.medFitness
        elif(self.fitness < 5):
            self.image, self.rect = self.lowFitness
            self.low = True

        self.rect.center = (random.randint(self.area.left+6, self.area.right - 6), random.randint(self.area.top + 32, self.area.bottom - 6))

        pygame.sprite.Sprite.__init__(self)
        self.active = True
        #print "CREATED INFECTED WITH FITNESS " + str(self.fitness) + " and speed " + str(self.speed)


    def update(self, deltaTime):
        self.checkTarget()

        if self.target is not None:
            vector = ( self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y)
        elif self.rect.collidepoint(self.tempTarget[0], self.tempTarget[1]):
            randX = random.randint(self.area.left+6, self.area.right - 6)
            randY = random.randint(self.area.top + 32, self.area.bottom - 6)
            # print "seeking X: " + str(randX) + " and Y: " + str(randY)
            self.tempTarget = (randX, randY)
            vector = ( self.tempTarget[0] - self.rect.x, self.tempTarget[1] - self.rect.y)
        else:
            vector = ( self.tempTarget[0] - self.rect.x, self.tempTarget[1] - self.rect.y)


        magnitude = math.sqrt((vector[0] * vector[0]) + (vector[1] * vector[1]))
        #print "infected magnitude: " + str(magnitude)

        if(self.tempTarget and magnitude < 10):
            randX = random.randint(self.area.left + 50, self.area.right - 50)
            randY = random.randint(self.area.top + 50, self.area.bottom - 50)
            self.tempTarget = (randX, randY)

        if(magnitude < 0.5):
            magnitude = 1

        self.move((vector[0] / magnitude) * self.speed * deltaTime, (vector[1] / magnitude) * self.speed * deltaTime)
        self.checkBounds()

    def move(self, moveX, moveY):
        newpos = self.rect.move((moveX, moveY))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                moveX = -(moveX) * 2
            if self.rect.top < self.area.top or self.rect.bottom > self.area.bottom:
                moveY = -(moveY) * 2

        newpos = self.rect.move(int(moveX), int(moveY))

        self.rect = newpos

    def findTarget(self, col):
        colDistance = math.hypot((self.rect.x - col.rect.x), (self.rect.y - col.rect.y))
        if self.target:
            nearestT = math.hypot((self.rect.x - self.target.rect.x), (self.rect.y - self.target.rect.y))
            if abs(colDistance) < abs(nearestT) or col.fitness < self.target.fitness:
                self.target = col
        elif abs(colDistance) < self.radius:
            self.target = col

    def checkTarget(self):
        if self.target:
            nearestT = math.hypot((self.rect.x - self.target.rect.x), (self.rect.y - self.target.rect.y))
            if abs(nearestT) > self.radius:
                self.target = None
        if self.target and not self.target.alive():
            self.target = None

    """Check for out of bounds position and bring back into game"""
    def checkBounds(self):
        if self.alive():
            if not self.area.contains(self.rect):
                print "INFECTED OOB: " + str(self.rect)

    def evolve(self):
        self.fitness = self.fitness + 1
        if(self.fitness >= 10 and not self.high):
            self.image, tmp = self.highFitness
            self.speed = self.speed + 10
            self.high = True
            self.med = True
        elif(self.fitness >= 5 and not self.med):
            self.image, tmp = self.medFitness
            self.speed = self.speed + 10
            self.med = True
