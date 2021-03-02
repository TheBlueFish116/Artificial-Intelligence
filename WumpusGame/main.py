"""CSCI 446 - Artificial Inteligence - Spring 2020"""

__author__ = "John Dolph, Dylan Rosenbaum"
__date__   = "2-27-20"

import random as rand
import numpy as np
import time
from Visual import Visual
from World import World

#class variables
worlds = []
p_pit = 0.075
p_obs = 0.075
p_wumpus = 0.05
num_worlds = 10

#statistics (all agents combined)
num_cells_explored = 0
num_w_killed = 0
num_w_agent_death = 0
num_p_agent_death = 0
num_gold_found = 0

"""Generates a wumpus world"""
def generate_world(p_pit, p_obs, p_wumpus):

    #setup 2D cell array
    world_size = rand.randint(1,5) * 5
    world_array = [[0 for n in range(world_size)] for m in range(world_size)]

    #populates the world using the provided probabilities
    arrows = 0
    for n in range(world_size):
        for m in range(world_size):
            prob_select = np.random.choice(4,1,p=[p_pit, p_obs, p_wumpus, 1-(p_pit+p_obs+p_wumpus)])
            selection = ""

            if(prob_select == 0):
                selection = "pi"
            elif(prob_select == 1):
                selection = "bl"
            elif(prob_select == 2):
                selection = "wu"
                arrows += 1
            elif(prob_select == 3):
                selection = "em"

            world_array[n][m] = selection

    #select random empty cell and place gold, select initial state
    empty_cells = []
    for n in range(world_size):
        for m in range(world_size):
            if(world_array[n][m] == "em"):
                empty_cells.append((n,m))

    #Places gold in a random empty cell
    select = rand.randint(0,len(empty_cells)-1)
    s_one, s_two = empty_cells[select]
    world_array[s_one][s_two] = "go"
    empty_cells.remove((s_one,s_two))

    #Creates the explorer intial state
    select = rand.randint(0,len(empty_cells)-1)
    init_state = empty_cells[select]

    #Create and return a world instance using the generated world_array
    world = World(world_size, world_array, init_state, arrows)
    return world

"""Evaluates the agent performance based on collected statistics"""
def evaluate():
    global num_cells_explored
    global num_w_killed
    global num_w_agent_death
    global num_p_agent_death
    global num_gold_found

    #Combines the statistics of each agent
    for w in worlds:
        num_cells_explored += w.explorer.stats[4]
        num_w_killed += w.explorer.stats[1]
        num_w_agent_death += w.explorer.stats[3]
        num_p_agent_death += w.explorer.stats[2]
        num_gold_found += w.explorer.stats[0]

    #Takes the statistics averages
    average_one = num_cells_explored / num_worlds
    average_two = num_w_killed / num_worlds
    average_three = num_w_agent_death / num_worlds
    average_four = num_p_agent_death / num_worlds
    average_five = num_gold_found / num_worlds

    #Prints the averages
    print("Number of Cells Explored Average: " + str(average_one))
    print("Number of Wumpus' Killed: " + str(average_two))
    print("Number of Agents Killed by a Wumpus: " + str(average_three))
    print("Number of Agents Killed by a Pit: " + str(average_four))
    print("Number of Times Gold was Found: " + str(average_five))

#populates the worlds array with the generated worlds
for i in range(num_worlds):
    worlds.append(generate_world(p_pit, p_obs, p_wumpus))
    worlds[i].solve()
    time.sleep(0.5)

#begins world evaluation
evaluate()
