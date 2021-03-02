__author__ = "John Dolph, Dylan Rosenbaum"
__date__   = "2-27-2020"

from Agent import Agent
from Visual import Visual

class World:

    def __init__(self, size, world, init_state, arrows):

        self.world = world
        self.size = size
        self.init_state = init_state
        self.agent_y_location, self.agent_x_location = init_state
        self.explorer = Agent(self, init_state, arrows) #creates an agent
        self.reactExplorer = Agent(self, init_state, arrows)

    """Allows the agent to begin solving the world"""
    def solve(self):
        visited = []
        #sets off the agent
        #self.explorer.solve("smart")
        self.explorer.solve("react")

    """updates the agent location"""
    def update_agent_location(self,x,y):
        self.agent_x_location = x
        self.agent_y_location = y

    """returns the number of arrows the agent has"""
    def get_arrows(self):
        return str(self.explorer.arrows)
