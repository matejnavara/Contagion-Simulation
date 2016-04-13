__author__ = 'Matej'

import sys, pygame, random, time, numpy
import Healthy, Infected, Dead, Hunter, Utilities
from matplotlib import pyplot as plt


if not pygame.font: print 'Warning, fonts disabled'

"""INPUT VARIABLES"""
startHealthyPop = Utilities.numberEntry(raw_input("Enter number of healthy (1-500): "))
startInfectedPop = Utilities.numberEntry(raw_input("Enter number of infected (1-500): "))
addHunter = Utilities.boolEntry(raw_input("Add a hunter? (y/n): "))

"""Increases their likelihood of winning an encounter"""
healthyBonus = 0
infectedBonus = 0

"""Lists used to plot results"""
healthyplot = []
infectedplot = []
deadplot = []

hfitnessplot = []
ifitnessplot = []

delay = 0.05



class Main:
    def __init__(self, width=1000, height=600):
        #startHealthyPop = int(raw_input("Enter number of healthy: "))
        #print(startHealthyPop,type(startHealthyPop))
        #startInfectedPop = int(raw_input("Enter number of infected: "))
        #addHunter = input("Add a hunter? (True/False): ")

        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        pygame.display.set_caption("Contagion Simulation - Matej Navara - 10818271")
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.totalHealthy = startHealthyPop
        self.totalInfected = startInfectedPop
        self.totalDead = 0
        self.theEnd = False
        self.debugHealthy = False
        self.debugInfected = False

    def MainLoop(self):
        """This is the Main Loop of the Game"""

        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        clock = pygame.time.Clock()

        self.ImportAssets()

        """Main loop during execution"""
        while 1:
            """Check for quit events and button presses"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYUP:
                    keyName = pygame.key.name(event.key)
                    if keyName == "h":
                        self.debugHealthy = not self.debugHealthy
                    if keyName == "i":
                        self.debugInfected = not self.debugInfected

            deltaTime = clock.tick()/1000.0

            self.screen.blit(self.background, (0, 0))

            """Update agents"""
            self.collisionDetect()
            self.proximityDetect()

            self.healthy_sprites.update(deltaTime)
            self.infected_sprites.update(deltaTime)

            self.debugTarget()

            """Draw agents"""
            self.dead_sprites.draw(self.screen)
            self.healthy_sprites.draw(self.screen)
            self.infected_sprites.draw(self.screen)

            """While simulation has not ended update the result lists and days passed"""
            if self.theEnd is not True:
                days = pygame.time.get_ticks()/1000
                healthyplot.append(self.totalHealthy)
                infectedplot.append(self.totalInfected)
                deadplot.append(self.totalDead)
                hfitnessplot.append(self.healthyAvgFitness())
                ifitnessplot.append(self.infectedAvgFitness())

            """When simulation has ended, break out of the main loop"""
            if self.theEnd is True:
                break

            """Draw user interface"""
            if pygame.font:
                font = pygame.font.Font(None, 36)
                bigfont = pygame.font.Font(None, 50)
                timetext = bigfont.render("   Day: " + str(days), 1, (255, 255, 255))
                text = font.render("Healthy: " + str(len(self.healthy_sprites))
                                   + "  Infected: " + str(len(self.infected_sprites))
                                   + "  Dead: " + str(self.totalDead)
                                   , 1, (255, 255, 255))
                textpos = text.get_rect(centerx=self.background.get_width() / 2)
                self.screen.blit(text, textpos)
                self.screen.blit(timetext, (0,0))

                text2 = font.render(self.hunterCheck()
                                    + "Average Healthy Fitness: " + str(int(self.healthyAvgFitness()))
                                    + "    Average Infected Fitness: " + str(int(self.infectedAvgFitness()))
                                    , 1, (255, 255, 255))
                textpos2 = text2.get_rect(bottom=self.background.get_height())
                self.screen.blit(text2, textpos2)

                """Check end condition and display healthy win message"""
                if self.totalInfected < 1:
                    textWin = bigfont.render("HEALTHY HAVE OVERCOME THE INFECTION", 1, (255, 255, 255))
                    textWinPos = textWin.get_rect(centery=self.background.get_height() / 2)
                    self.theEnd = True
                    self.screen.blit(textWin, textWinPos)

                """Check end condition and display infected win message"""
                if self.totalHealthy < 1:
                    textLose = bigfont.render("ALL HEALTHY HAVE BEEN INFECTED", 1, (255, 255, 255))
                    textLosePos = textLose.get_rect(centery=self.background.get_height() / 2)
                    self.theEnd = True
                    self.screen.blit(textLose, textLosePos)

                time.sleep(delay)
                pygame.display.flip()

    def ImportAssets(self):
        """Used to import initial agent assets"""
        """Create sprite groups for each agent"""
        self.healthy_sprites = pygame.sprite.Group()
        self.infected_sprites = pygame.sprite.Group()
        self.dead_sprites = pygame.sprite.Group()

        """Add hunter agent into the healthy group if selected"""
        if addHunter:
            self.hunter = Hunter.Hunter()
            self.healthy_sprites.add(self.hunter)

        """Populate healthy agents up to the defined population size"""
        for x in range(startHealthyPop):
            self.healthy = Healthy.Healthy()
            self.healthy_sprites.add(self.healthy)

        """Populate infected agents up to the defined population size"""
        for y in range(startInfectedPop):
            self.infected = Infected.Infected()
            self.infected_sprites.add(self.infected)

    def proximityDetect(self):
        """Used to find the targets within each agents proximity"""
        """Loop through the agents and find the collisions within their radius"""
        for healthy in self.healthy_sprites:
            for infected in self.infected_sprites:
                if len(healthy.rect)==4 and len(infected.rect)==4:
                        if pygame.sprite.collide_circle(healthy, infected):
                                healthy.findTarget(infected)
                                infected.findTarget(healthy)

    def collisionDetect(self):
        """Used to determine the collision between two agents. It also determines the result of an encounter"""
        for col in self.healthy_sprites:
            for infected in self.infected_sprites:
                if len(col.rect)==4 and len(infected.rect)==4:
                    if pygame.sprite.collide_rect(col,infected):
                    #collided = pygame.sprite.spritecollide(col, self.infected_sprites, False)
                    #for infected in collided:
                        if(infected.alive() and col.alive()):
                            """Determines resolution of conflict based on random roll scaled by fitness"""
                            healthy_roll = random.randrange(float(col.fitness/5), col.fitness) + healthyBonus
                            infected_roll = random.randrange(float(infected.fitness/5), infected.fitness) + infectedBonus

                            # print "INFECTED ROLL : " + str(infected_roll) + " VS HEALTHY ROLL: " + str(healthy_roll) \
                            #       + "   I fitness: " + str(infected.fitness) + "  H fitness: " + str(col.fitness)

                            if infected_roll <= healthy_roll:
                                """If healthy roll is greater or equal to the infected roll it will:
                                evolve, create a dead sprite for the infected in its place,
                                remove the infected agent, change global totals"""
                                col.target = None
                                col.evolve()
                                self.dead = Dead.Dead(infected.rect.center)
                                self.dead_sprites.add(self.dead)
                                infected.kill()
                                self.totalInfected = self.totalInfected - 1
                                self.totalDead = self.totalDead + 1
                                #print "INFECTED KILLED"
                            elif infected_roll > healthy_roll:
                                """If infected roll is greater than the healthy roll it will:
                                evolve, create a new infected sprite with the healthy agent's fitness,
                                remove the healthy agent, change global totals"""
                                infected.target = None
                                infected.evolve()
                                self.newinfected = Infected.Infected(col.fitness)
                                self.newinfected.rect.center = col.rect.center
                                self.newinfected.target = None
                                self.infected_sprites.add(self.newinfected)
                                col.kill()
                                self.totalHealthy = self.totalHealthy - 1
                                self.totalInfected = self.totalInfected + 1
                                #print "HEALTHY INFECTED"


    def hunterCheck(self):
        """Used to check the presence of a hunter and update the GUI"""
        if addHunter is False:
            return " < NO HUNTER >  "
        if self.hunter.alive():
            fitness = self.hunter.fitness
            return "  HUNTER Fitness: " + str(fitness) + "  "
        else:
            return "  < HUNTER DEAD >  "

    def debugTarget(self):
        """Used to display the debug proximity and target for infected/healthy agents"""
        if self.debugHealthy:
            for healthy in self.healthy_sprites:
                if healthy.alive():
                    pygame.draw.circle(self.screen, ( 0, 255, 0), healthy.rect.center, healthy.awareness, 2)
                if healthy.target is not None:
                    pygame.draw.line(self.screen, (0, 255, 0), healthy.rect.center, healthy.target.rect.center)
        if self.debugInfected:
            for infected in self.infected_sprites:
                if infected.alive():
                    pygame.draw.circle(self.screen, (255, 0, 0), infected.rect.center, infected.awareness, 2)
                if infected.target is not None:
                    pygame.draw.line(self.screen, (255, 0, 0), infected.rect.center, infected.target.rect.center)
        if addHunter:
            if self.hunter.alive():
                pygame.draw.circle(self.screen, (0, 0, 255), self.hunter.rect.center, self.hunter.awareness, 2)
                if self.hunter.target is not None:
                    pygame.draw.line(self.screen, (0, 0, 255), self.hunter.rect.center, self.hunter.target.rect.center)


    def healthyAvgFitness(self):
        """Calculates the average fitness of the healthy population, excluding the hunter's fitness"""
        average = 0.0
        if self.totalHealthy > 0:
            total = float(sum(healthy.fitness for healthy in self.healthy_sprites))
            if addHunter and self.hunter.alive():
                total = total - self.hunter.fitness
            average = total/self.totalHealthy
        return average

    def infectedAvgFitness(self):
        """Calculates the average fitness of the infected population"""
        average = 0.0
        if self.totalInfected > 0:
            total = float(sum(infected.fitness for infected in self.infected_sprites))
            average = total/self.totalInfected
        return average

    def plotResults(self):
        """Plots the results using matplotlib"""
        """Converts the global result lists into numpy arrays for use in matplotlib"""
        healthynp = numpy.array(healthyplot)
        infectednp = numpy.array(infectedplot)
        deadnp = numpy.array(deadplot)
        hfitnessnp = numpy.array(hfitnessplot)
        ifitnessnp = numpy.array(ifitnessplot)

        x = numpy.linspace(0, len(healthynp), len(healthynp))

        with plt.style.context('fivethirtyeight'):
            """Graph for average fitness over time"""
            fig = plt.figure()
            fig.suptitle('Fitness Over Time', fontsize=14, fontweight='bold')
            plt.plot(x, ifitnessnp, color='red')
            plt.plot(x, hfitnessnp, color='green')
            plt.show()
            """Graph for population size over time"""
            fig = plt.figure()
            fig.suptitle('Population Over Time', fontsize=14, fontweight='bold')
            #plt.plot(x, deadnp, color ='black')
            plt.plot(x, infectednp, color='red')
            plt.plot(x, healthynp, color='green')
            plt.show()


if __name__ == "__main__":
    MainWindow = Main()
    MainWindow.MainLoop()
    Main.plotResults(MainWindow)



