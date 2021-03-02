"""CSCI 446 - Artificial Inteligence - Spring 2020"""
"""The edge class houses two vertices"""

__author__ = "John Dolph, Dylan Rosenbaum"
__date__   = "2-4-20"

class Edge:
    def __init__(self,vOne,vTwo):
        self.vOne = vOne
        self.vTwo = vTwo
        self.visited = False

        #adds the nodes of the edge to each node's neighbor list
        self.vOne.addNeighbor(self.vTwo)
        self.vTwo.addNeighbor(self.vOne)
