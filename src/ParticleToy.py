__author__ = 'kevinholland'

from graphics import *
import time
from random import Random
from Button import Button
from Particle import *

class ParticleToy:
    def __init__(self):
        print("LAUNCHING WINDOW")
        self.win = GraphWin("Particles", 500, 500, False)
        self.win.setCoords(0, 0, 1000, 1000)
        self._mouseLocation = Point(0, 0)
        self.particleSize = 5
        self.numOfParticles = 100
        self._particles = []
        self.showWelcomePage()
        self._gameElements = []
        self._welcomePageElements = []


    def startGame(self):
        print("STARTING GAME")
        self.win.setBackground("Light Blue")
        self.speed = 1
        self.crazyColor = False
        self._initializeGameView()
        self._timer()
        self.win.checkMouse()

    def _initializeGameView(self):
        print("INITIALIZING GAME VIEW")
        self.lastFpsUpdate = 0
        self.frameCounter = 0
        self._gameElements = []
        self._initializeButtons()
        self._initializeParticles()

        keyFunctionsPrompt = Text(Point(430, 35), "Press 'q' to Quit.     Press 'r' to Reset. ").draw(self.win)
        self.fpsText = Text(Point(50, 900), "")
        self._gameElements.append(keyFunctionsPrompt)
        self._gameElements.append(self.fpsText)

    def _initializeButtons(self):
        print("INITIALIZING BUTTONS")
        self.speed1Button = Button("Speed 1", Point(660, 15), Point(760, 50), self.win)
        self.speed2Button = Button("Speed 2", Point(770, 15), Point(870, 50), self.win)
        self.speed3Button = Button("Speed 3", Point(880, 15), Point(980, 50), self.win)
        self.crazyColorButton = Button("cRaZy CoLoR!", Point(20, 15), Point(180, 50), self.win)
        self.backToMenuButton = Button("Back to Menu", Point(20, 950), Point(170, 980), self.win)

        self._gameElements.append(self.speed1Button)
        self._gameElements.append(self.speed2Button)
        self._gameElements.append(self.speed3Button)
        self._gameElements.append(self.crazyColorButton)
        self._gameElements.append(self.backToMenuButton)

    def _timer(self):
        print("STARTING GAME TIMER")
        while self._running:
            self.frameCounter += 1

            if time.time() - self.lastFpsUpdate > 1:
                self.fpsText.setText(self.frameCounter)
                self.fpsText.undraw()
                self.fpsText.draw(self.win)
                self.lastFpsUpdate = time.time()
                self.frameCounter = 0

            self._keyboardCallback()
            self._mouseCallback()
            self._displayCallback()


    def _keyboardCallback(self):
        key = self.win.checkKey()
        if key == "q":
            print("QUITTING")
            self._running = False
        if key == "r":
            print("RESETTING PARTICLES")
            self._killParticles()
            self._initializeParticles()
        return

    def _mouseCallback(self):
        mouseLocation = Point(0, 0)
        if mouseLocation.getX() == 0 and mouseLocation.getY() == 0:
            point = self.win.checkMouse()
        else:
            point = None
        if point:
            mouseLocation = point

        if self.speed1Button.clicked(mouseLocation):
            self.speed = 1
            print("SPEED 1")
        elif self.speed2Button.clicked(mouseLocation):
            self.speed = 3
            print("SPEED 2")
        elif self.speed3Button.clicked(mouseLocation):
            self.speed = 6
            print("SPEED 3")
        elif self.crazyColorButton.clicked(mouseLocation):
            if self.crazyColor:
                self.crazyColor = False
                print("CRAZY COLOR OFF")
                self.particleSize = self.originalSize
            else:
                self.crazyColor = True
                print("CRAZY COLOR ON")
                self.originalSize = self.particleSize
        elif self.backToMenuButton.clicked(mouseLocation):
            self.backToMenu()

        return

    def _displayCallback(self):
        self._calculateParticleMovement()
        self.win.flush()
        return

    def _initializeParticles(self):
        print("INITIALIZING PARTICLES")
        for i in range(self.numOfParticles):
            r = Random()
            particle = Particle(self.win, Point(r.randrange(0, 1000), r.randrange(70, 1000)))

            # generate random color
            randFunc = lambda: r.randint(0, 255)
            particle.setColor('#%02X%02X%02X' % (randFunc(), randFunc(), randFunc()))

            particle.setSize(self.particleSize)

            particle.draw()
            self._particles.append(particle)


    def findParticle(self, particle):
        if particle.position.getX() < 0:
            return "left"
        if particle.position.getX() > 1000:
            return "right"
        if particle.position.getY() < 100:
            return "below"
        if particle.position.getY() > 1000:
            return "above"
        else:
            return "in"

    def reflect(self, particle):
        if self.findParticle(particle) == "in":
            return False
        elif self.findParticle(particle) == "left":
            particle.setParticleMovement(abs(particle.dX), particle.dY)
            return True
        elif self.findParticle(particle) == "right":
            particle.setParticleMovement(-abs(particle.dX), particle.dY)
            return True
        elif self.findParticle(particle) == "bottom":
            particle.setParticleMovement(particle.dX, abs(particle.dY))
            return True
        elif self.findParticle(particle) == "top":
            particle.setParticleMovement(particle.dX, -abs(particle.dY))
            return True


    def _calculateParticleMovement(self):
        r = Random()
        for i in range(len(self._particles)):
            particle = self._particles[i]

            if r.randrange(0, 10) > 8 and not self.reflect(particle):
                particle.setParticleMovement(self.speed * r.randrange(-3, 4.0), self.speed * r.randrange(-3, 4.0))

            if self.crazyColor:
                randFunc = lambda: r.randint(0, 255)
                particle.setColor('#%02X%02X%02X' % (randFunc(), randFunc(), randFunc()))


            particle.move()
        return

    def _killParticles(self):
        print("KILLING PARTICLES")
        for particle in self._particles:
            particle.undraw()
        self._particles = []

    def showWelcomePage(self):
        print("SHOWING WELCOME PAGE")
        self._welcomePageElements = []
        self.win.setBackground("Dark Gray")
        atWelcome = True

        welcomeText = Text(Point(500, 850), "Random Particle Movement Generator")
        welcomeText.setSize(28)
        welcomeText.setTextColor("BLUE")
        welcomeText.draw(self.win)
        self._welcomePageElements.append(welcomeText)

        startButton = Button("Start", Point(400, 350), Point(600, 450), self.win)
        startButton.setTextSize(32)
        self._welcomePageElements.append(startButton)

        particleSizeText = Text(Point(300, 600), "Particle Size").draw(self.win)
        self._welcomePageElements.append(particleSizeText)

        particleSizeInput = Entry(Point(500, 600), 8).setText("5").draw(self.win)
        self._welcomePageElements.append(particleSizeInput)

        particleSizeRangeText = Text(Point(650, 600), "(1-15)").draw(self.win)
        self._welcomePageElements.append(particleSizeRangeText)

        numOfParticlesText = Text(Point(270, 700), "Number of Particles").draw(self.win)
        self._welcomePageElements.append(numOfParticlesText)

        numOfParticlesInput = Entry(Point(500, 700), 8).setText("100").draw(self.win)
        self._welcomePageElements.append(numOfParticlesInput)

        numOfParticlesInfoText = Text(Point(650, 700), "(5-1000)").draw(self.win)
        self._welcomePageElements.append(numOfParticlesInfoText)

        valid = True
        valid2 = True

        while atWelcome:
            time.sleep(.1)
            point = self.win.checkMouse()
            if point and valid and valid2 and startButton.clicked(point):
                self._running = True
                self.hideWelcomePage()
                self.startGame()
                atWelcome = False
                return
            elif self.win.checkKey() == "q":
                print("QUITTING")
                atWelcome = False
                return
            if particleSizeInput.getText() != "":
                try:
                    self.particleSize = int(particleSizeInput.getText())
                    if self.particleSize < 1 or self.particleSize > 15:
                        self.textErrorMessage(particleSizeRangeText, "Invalid Entry. Enter 1-15", Point(750, 600))
                        valid = False
                    else:
                        self.textErrorMessage(particleSizeRangeText, "(1 - 15)", Point(650, 600), "BLACK")
                        valid = True
                except:
                    self.textErrorMessage(particleSizeRangeText, "Invalid Entry. Numbers only", Point(750, 600))
                    valid = False

            if numOfParticlesInput.getText() != "":
                try:
                    self.numOfParticles = int(numOfParticlesInput.getText())
                    if self.numOfParticles < 5 or self.numOfParticles > 1000:
                        self.textErrorMessage(numOfParticlesInfoText, "Invalid Entry. Enter 5-1000", Point(750, 700))
                        valid2 = False
                    else:
                        self.textErrorMessage(numOfParticlesInfoText, "(5 - 1000)", Point(650, 700), "BLACK")
                        valid2 = True
                except:
                    self.textErrorMessage(numOfParticlesInfoText, "Invalid Entry. Numbers Only", Point(750, 700))
                    valid2 = False

    def textErrorMessage(self, textObject, message, newAnchor, color="RED"):
        textObject.setText(message)
        textObject.setTextColor(color)
        textObject.anchor = newAnchor
        textObject.undraw()
        textObject.draw(self.win)

    def backToMenu(self):
        print("GOING BACK TO WELCOME MENU")
        self._killParticles()
        for element in self._gameElements:
            element.undraw()
            del element

        self._running = False
        self.showWelcomePage()

    def hideWelcomePage(self):
        print("HIDING WELCOME PAGE")
        for element in self._welcomePageElements:
            element.undraw()
            del element
