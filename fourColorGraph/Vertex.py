"""CSCI 446 - Artificial Inteligence - Spring 2020"""
"""The vertex class holds color assignments, domains, costs to other nodes, connected neighbors and handles its own coloring functions."""

__author__ = "John Dolph, Dylan Rosenbaum"
__date__   = "2-4-20"

import random as rand

class Vertex:
    def __init__(self,x,y,k,id):
        self.x = x
        self.y = y
        if(k==4):
            self.domain = [(255,0,0),(0,255,0),(0,0,255),(230,150,0)]
        else:
            self.domain = [(255,0,0),(0,255,0),(0,0,255)]
        self.color = None
        self.costs = []
        self.neighbors = []
        self.current = False
        self.id = id


    """changes the vertex's color without evaluating the constraints"""
    def colorIt(self, color):                               
        self.color = color                                  #sets the color
        self.domain = [color]                               #The domain is the list of all possible colors so it is only the assigned color

        for neighbor in self.neighbors:                     #go to every neighbor
            for color in neighbor.domain:                   #and check if the vertex's color is in their domain
                if(color == self.color):
                    neighbor.domain.remove(color)           #if it is... remove it

    
    """resets vertex to default domain"""
    def defaultDomain(self, k):
        if(k == 4):
            self.domain = [(255,0,0),(0,255,0),(0,0,255),(230,150,0)]
        else:
            self.domain = [(255,0,0),(0,255,0),(0,0,255)]


    #sets the vertex color under domain restrictions
    def setColor(self):
        for n in self.neighbors:
            for color in self.domain:
                #if(color not in neighbor.domain):
                if(color == n.color):
                    self.domain.remove(color)
                    break
        if(len(self.domain) > 0):
            index = rand.randint(0,len(self.domain)-1)
            self.color = self.domain[index]
            self.domain.remove(self.color)
            return False
        else:
            return True

    def addNeighbor(self,v):
        self.neighbors.append(v)

    """Returns a color to the domain"""
    def returnToDomain(self):
        self.color=None
