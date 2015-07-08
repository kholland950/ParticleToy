__author__ = 'kevinholland'

from graphics import Circle
from graphics import Point

class Particle:
    def __init__(self, window, p=Point(0, 0)):
        self.particle = None
        self.drawn = False
        self.color = "RED"
        self.position = p
        self.x = p.getX()
        self.y = p.getY()
        self.size = 3
        self.dX = 0
        self.dY = 0
        self.win = window
        self.particleTurnCount = 0

    def setCoord(self, x, y):
        self.x = x
        self.y = y

    def setColor(self, color):
        self.color = color
        if self.particle:
            self.particle.setFill(color)

    def setSize(self, size):
        self.size = size
        if self.drawn:
            self.undraw()
            self.draw()

    def draw(self):
        self.particle = Circle(Point(self.x, self.y), self.size)
        self.particle.setFill(self.color)
        self.particle.draw(self.win)
        self.drawn = True

    def undraw(self):
        self.particle.undraw()
        self.drawn = False

    def setParticleMovement(self, dx, dy):
        self.dX = dx
        self.dY = dy

    def move(self):
        self.particle.move(self.dX, self.dY)
        self.position = Point(self.position.getX() + self.dX, self.position.getY() + self.dY)
        self.particle.undraw()
        self.particle.draw(self.win)
