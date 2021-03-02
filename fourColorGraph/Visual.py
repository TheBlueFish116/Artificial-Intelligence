"""Graphical Implementation for Graphs"""
"""The Visual class provides a visualization of each graph and the steps made to reach a search solution. The class cycles through each available graph."""

__author__ = "John Dolph, DylanRosenbaum"
__date__   = "2-3-2020"

import pygame
import time

class Visual:

    def __init__(self, graphs, speed, stepSpeed, showID, xWinSize, yWinSize):
        self.graphs = graphs
        self.speed = speed
        self.stepSpeed = stepSpeed
        self.showID = showID
        self.xWinSize = xWinSize
        self.yWinSize = yWinSize

        #Sets up the graph display window
        pygame.init()
        self.bg_color = (100,100,100)
        #(self.width, self.height) = (self.xWinSize, self)
        self.screen = pygame.display.set_mode((self.xWinSize, self.yWinSize))
        pygame.display.set_caption('Graph Visualization')
        self.screen.fill(self.bg_color)
        self.font = pygame.font.SysFont('system',30)

        #start the visualization
        self.visualizeGraphs()

    #Draws each vertex of a graph and scales the x and y values to fill the window
    def displayVertex(self, vertex, index, mode):

        #each current node in the search will be red
        if(mode==True):
            if(vertex.color != None):
                color = vertex.color
                size = 13
            else:
                color = (255,255,255)
                size = 18
        else:
            color = (0,0,0)
            #color  =vertex.color
            size = 13


        pygame.draw.circle(self.screen, (255,0,0), (int(vertex.x * self.xWinSize), int(self.yWinSize - vertex.y * self.yWinSize)), 1, 1)
        pygame.draw.circle(self.screen, color, (int(vertex.x * self.xWinSize), int(self.yWinSize - vertex.y * self.yWinSize)), size, 3)
        if(self.showID):
            id = self.font.render(str(vertex.id),1, (255,255,255))
            self.screen.blit(id, (int(vertex.x*self.xWinSize)-5 , int(self.yWinSize - vertex.y*self.yWinSize)-10) )
            if(mode):
                time.sleep(self.stepSpeed)
            pygame.display.flip()

    #Draws each edge of a graph and scales the x and y values to fill the window
    def displayEdge(self, edge,color):
        vOne = edge.vOne
        vTwo = edge.vTwo

        pygame.draw.line(self.screen,color, (int(vOne.x*self.xWinSize),int(self.yWinSize - vOne.y*self.yWinSize)), (int(vTwo.x*self.xWinSize),int(self.yWinSize - vTwo.y*self.yWinSize)), 3)
        pygame.display.flip()

    #Cycles through all of the graphs and their colorings at a defined speed. Press ESC to cancel.
    def visualizeGraphs(self):

        running = True
        while running:

            #Test loop to display the graphs
            for graphNum in range(len(self.graphs)):

                text = self.font.render("Graph " + str(graphNum+1) + " of " + str(len(self.graphs)), 1, (240,240,240))
                self.screen.blit(text, (0, 10))
                self.screen.blit(self.font.render("Press Esc to exit...",1,(240,240,240)), (0,50))
                pygame.display.flip()


                for edge in self.graphs[graphNum].edges:
                    self.displayEdge(edge,(30,30,30))
                for i, vertex in enumerate(self.graphs[graphNum].vertices):
                    self.displayVertex(vertex, i,False)
                    pygame.display.flip()
                for i, vertex in enumerate(self.graphs[graphNum].vVisited):
                        self.displayVertex(vertex, i, True)


                #Allows the window to be closed when ESC or the window X buttonis pressed
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    running=False
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break

                time.sleep(self.speed)
                self.screen.fill(self.bg_color)
            break
            pygame.display.flip()
