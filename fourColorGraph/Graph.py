"""CSCI 446 - Artificial Inteligence - Spring 2020"""
"""The graph class contains lists of edges and vertices and handles the random node scatter and edge construction functions"""

__author__ = "John Dolph, Dylan Rosenbaum"
__date__   = "2-4-20"

import random as rand
import math
from Vertex import Vertex
from Edge import Edge

class Graph:
    
    def __init__(self,n,k):
        self.n = n
        self.vertices = []
        self.edges = []
        self.costs = []
        self.k = k
        self.vVisited=[]
        
    """Scatters nodes on the unit square"""
    def construct(self):
        for i in range(self.n):
            x = rand.uniform(0,1)
            y = rand.uniform(0,1)
            v = Vertex(x,y,self.k,i)
            self.vertices.append(v)

    """Selects some point X at random, then connects it to the nearest Y
       such that X is not already connected to Y and no lines intersect."""
    def pairXY(self):
        possible = True
        for i in range(self.n*10):
            xIndex = rand.randint(0,self.n-1)  #The index of random object X in the vertices array
            X = self.vertices[xIndex]
            closestPoint = Vertex(100,100,self.k,0)
            closestDistance = 100
            distance = 0
            y = 1
            for vert in self.vertices:
                potential = True
                distance = math.sqrt((vert.x - X.x)**2+(vert.y - X.y)**2)
                if(distance != 0 and distance < closestDistance):
                    for edge in self.edges:
                        if(edge.vOne == vert or edge.vTwo == vert):
                            if(edge.vOne == X or edge.vTwo == X):
                                potential = False
                    if(potential):
                        if(self.doLinesCross(X.x, vert.x, X.y, vert.y)):
                            closestDistance = distance
                            closestPoint = vert
            if(closestPoint.x != 100 and closestPoint.y != 100):
                newEdge = Edge(X,closestPoint)

                self.edges.append(newEdge)

        return X

    """calculates if two line segments cross"""
    def doLinesCross(self, x1, x2, y1, y2):
        line = True
        slope = (y2-y1)/(x2-x1)
        b = (y2) - (slope*x2)
        for edge in self.edges:
            slope2 = (edge.vTwo.y - edge.vOne.y)/(edge.vTwo.x - edge.vOne.x)
            b2 = edge.vTwo.y - (slope2*edge.vTwo.x)
            b2 = b2 - b
            slope2 = slope - slope2
            x = b2/slope2
            if(x < min(x1,x2) or x > max(x1,x2)):
                pass
            elif(x < min(edge.vOne.x, edge.vTwo.x) or x > max(edge.vOne.x, edge.vTwo.x)):
                pass
            elif(x - min(x1,x2) < .000001 and x - min(x1,x2) > -.000001):
                pass
            elif(x - max(x1,x2) < .000001 and x - max(x1,x2) > -.000001):
                pass
            else:
                line = False


        return line

    """calculates probability of success"""
    def calcFitness(self, T, localMax):                     #T is temperature
        successRate = 0                                     #this will hold the final fitness
        for vert in self.vertices:
            badNeighbor = False                             #neighbor has same color
            for neighbor in vert.neighbors:
                if(neighbor.color == vert.color):
                    badNeighbor = True
            if(badNeighbor == False):                       
                successRate += 1                            #adds 1 point for every vertice that has at least one badNeighbor with the same color
        successRate = successRate/len(self.vertices)        #gets percentage of vertices that satisfy the constraints
        print(localMax, "    T: ",T,"                                                               Raw: ", successRate)
        successRate = successRate**T                        #makes it exponential depending on the temperature
        return successRate
