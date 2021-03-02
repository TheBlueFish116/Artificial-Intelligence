__author__ = "John Dolph"
__date__   = "2-27-2020"

import pygame
import time

class Visual:

    def __init__(self, world, step_speed, x_window, y_window):

        #class instance variables
        self.world = world
        self.step_speed = step_speed
        self.x_window = x_window
        self.y_window = y_window

        #Display window setup
        pygame.init()
        self.bg_color = (100,100,100)
        self.screen = pygame.display.set_mode((self.x_window, self.y_window))
        pygame.display.set_caption('Wumpus World (Press "Space" to Exit)')
        self.screen.fill(self.bg_color)
        self.font = pygame.font.SysFont('system',30)

    """Refreshes the screen with new world data"""
    def refresh(self, wait):
        self.screen.fill(self.bg_color)
        for n in range(self.world.size):
            for m in range(self.world.size):
                pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(35*m, 35*n, 35, 35), 3 )
                contents = self.world.world[n][m]
                contents = contents[0].capitalize()
                if(contents != "E" or (n == self.world.agent_y_location and m == self.world.agent_x_location)):
                    color = (0,0,0)
                    if(n == self.world.agent_y_location and m == self.world.agent_x_location):
                        contents = "A"
                        color = (50, 250, 50)
                    if(contents == "P"):
                        color = (150,150,250)
                    elif(contents == "G"):
                        color = (250,250,150)
                    elif(contents == "W"):
                        color = (250, 150, 150)
                    elif(contents == "B"):
                        color = (150, 150, 150)
                    self.screen.blit(self.font.render(str(contents),1,color), (35*m,35*n))
        if(wait):
            time.sleep(self.step_speed)
        pygame.display.flip()

    """Ends the visualization"""
    def end(self):
        while(True):

            #Allows the window to be closed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] or keys[pygame.K_SPACE]:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

        pygame.display.quit()
        pygame.quit()
