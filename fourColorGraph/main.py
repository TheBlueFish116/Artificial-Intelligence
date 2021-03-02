"""CSCI 446 - Artificial Inteligence - Spring 2020"""
"""The main class houses each of the search algorithms and a list containing each of the generated graphs"""


__author__ = "John Dolph, Dylan Rosenbaum"
__date__   = "2-4-20"

import random as rand
from Graph import Graph
from Visual import Visual
import math
import numpy as np
import copy                 #creates copies without referencing the original

graphs = [] #a list containing each generated graph
n = 20 #the number of nodes in each graph
numGraphs = 10 #The number of graphs
k = 4 #The coloring number (number of possible colors)

"""Creates numGraphs graphs on the unit square with n vertices, then appends them to a list G."""
def createGraphs():
    for i in range(numGraphs):
    #    graph = Graph(10 * rand.randint(1,10),k)
        graph = Graph(n,k)
        graph.construct()
        graphs.append(graph)

"""Checks whether or not a solution was found"""
def solutionCheck(graph, i):
    solution = True
    for v in graph.vertices: #iterates thorugh the graph vertices, checks whether or not vertex v was assigned a color
        if(v.color == None):
            solution = False
            break
        for n in v.neighbors: #iterates through each graph vertex neighbors, determines whether or not they are different colors
            if(n.color ==v.color):
                solution = False
                break

    if(solution): #print the results
        print("Graph " + str(i+1) + " - Found Solution for k = " + str(k) )
    else:
        print("Graph " + str(i+1) + " - No Solutions found for k = " + str(k) )

"""Simple backtracking function"""
def simpleBacktracking(graph, v, visited):

    visited.append(v) #visits a node
    violation = v.setColor() #sets the node color and checks constraint.
    print("Vertex " + str(v.id) + " Assigned Color " + str(v.color))
    for n in v.neighbors: #cycles thorugh each of the node neighbors
        if n not in visited: #determines whether or not a node is visited
            print("From Vertex " + str(v.id) + " --> Vertex " + str(n.id))
            simpleBacktracking(graph, n, visited) #recursively moves throigh the graph when a node is not visited



"""checks immediate neighbors of visit to see if they have an empty domain"""
def forwardCheck(visit):
    valid = True                                    #stays true if all domains aren't empty
    for vert in visit.neighbors:                    #visit every neighbor
        if(len(vert.domain) == 0):                  #if they don't have a domain
            valid = False                           #valid is false
    return valid                                    #return valid

"""recieves vertex you are visiting the color you are reverting and visited nodes
    reverts a decision that lead to a failure"""
def failed(visit, color, visited):                  #recieves vertex you are visiting the color you are reverting and visited nodes
    visit.defaultDomain(k)                          #visit goes back to a full domain
    visit.color = None                              #firsts removes the color from the vertex you made a decision on
    for neighbor in visit.neighbors:                #goes to all neighbors
        if(neighbor not in visited):                #when this is true the neighbor does not have a color assigned
            x = 0                                   #evaluates if we should add the color back into the neighbors domain
            for neighbor2 in neighbor.neighbors:    #to do so we go to each of the neighbors neighbor
                if(neighbor2.color == color):       # if they border another vertex that is assigned the color
                    x += 1                          #X>0 and the color stays off the neighbors domain
            if(x==0):                               
                neighbor.domain.append(color)       #doesn't border the color anymore so you can add it back into the domain
        else:
            if(neighbor.color in visit.domain):     #the immediate neighbor has a color assigned
                visit.domain.remove(neighbor.color) #remove the color from the node that was reverted

"""recursive function that recieves the graph with the vertex we are visiting and a list of visited nodes
count evaluates efficiency"""
def backtrackingForwardCheck(graph, visit, visited):
    visited.append(visit)                               #"visit it"
    success = False                                     #Used to evaluated success
    tempDomain = visit.domain                           #tempdomain since coloring it destroys the domain and therefor the for function
    for color in tempDomain:                     #this makes it go through each possible color for every vertex
        visit.colorIt(color)   #colorIt() is in Vertex.py
        if(len(visited) == n):                   #only true when the search is all done and the four color constraint is satisfied
            return True                          #base case
        if(forwardCheck(visit)):                #checks to see if any of the neighbors domains are empty
            y = 0                                # I use this to make sure i don't get trapped anywhere
            for i in visit.neighbors:            #visits all neighbors... depth first search
                if i not in visited:
                    success = backtrackingForwardCheck(graph, i, visited)  #The bool this returns tells me if it was successfull or not
                    if(not success):
                        break                    # this break makes it so it tries the other colors when the forward check fails
                else:                            # whithout the break it would move to the next neighor even though it knows that the assigned color won't work
                    y += 1                      
                    if(y == len(visit.neighbors)):      #when all neighbors have been visited leave and go on to the next unvisited area
                        return True
            if(success == True):
                return success                    #all neighbors and their branching neighbors are assigned a color
            else:                                   #the color doesn't work for one of the later neighbors
                failed(visit, color, visited)    #failed() is above this function
        else:
            failed(visit, color, visited)           #the color causes an immediate neighbor to have an empty domain
    visited.remove(visit)                           #if you get to here none of the colors worked

    return success                                     #could be true or false

"""Backtracking with arc consistency function"""
def backtrackingArcConsistency(graph,visited):
    for v in graph.vertices: #iterates through each vertex in the graph
        A = v
        print("Visited node " + str(v.id))
        visited.append(A) #visits node A
        if(len(A.neighbors) > 0): #if node A has neighbors
            for B in A.neighbors: #for every neighbor of node A
                if(A.color in B.domain): #if the color of node A is in the domain of node B
                    B.domain.remove(A.color) #remove the color of A from the domain of neighbor B
        simpleBacktracking(graph,v,visited) #continue to move thorugh the graph



"""Local search with simulated annealing function"""
def localSearchAnnealing(graph, domain, constraints):
#    #color domain and not visited list
    notVisited=[]
    visited=[]

    #random Initialization (total graph color assignment)
    for n in graph.vertices:
        n.color = domain[rand.randint(0,len(domain)-1)]
        notVisited.append(n)

    while(len(notVisited) > 0):

        #conflicts numbers for each descision
        conflicts = 0
        newConflicts = 0

        #select a random node and visit it
        node = notVisited[rand.randint(0,len(notVisited)-1)]
        print("Selected node " + str(node.id))
        notVisited.remove(node)
        visited.append(node)

        #randomly select a color for the node
        colorInd=rand.randint(0,len(domain)-1)
        color=domain[colorInd]
        print("Current node color: " + str(node.color))
        print("Tentative node color: " + str(color))

        #conflict check (accept if conflicts not increased)
        for n in node.neighbors:
            if(n.color == node.color):
                conflicts += 1
            if(n.color == color):
                newConflicts += 1

        if(newConflicts <= conflicts): #heuristic check (checks to see if the current color created more conflicts)
            print("Setting node color to " + str(color))
            node.color = color
        elif(newConflicts - conflicts > 0): #accept assignment with probability
            #attempting to reach complete visitation
            if(len(notVisited)>0):
                prob = math.pow(math.e,-(newConflicts-conflicts)/len(notVisited)) #probability of selecting the current color
                select = np.random.binomial(1,prob) #determines whether or not to select the current color for the graph solution

                if(select==1):
                    node.color = color #The current node color is selected for the solution
                    print("Set node color " + str(color) + " based on a Boltzmann distribution...")
                else:
                    print("Keeping original node color...")
            else:
                print("Keeping original node color...")

    return visited #returns the visited node list

"""Creates a population that has k random assignments"""
def population(graph, k):
    population = []
    
    for i in range(k):                              #population size of k loops through k times
        tempGraph = copy.deepcopy(graph)            #can't be an actual reference to tempGraph so I imported copy so i could have "holow" copies of the class
        for vert in tempGraph.vertices:             #colors every vertices
            randNum = rand.randint(0, 3)            #an equally random color
            vert.color =  vert.domain[randNum]
        population.append(tempGraph)                #adds each graph to the population
    return population                               #returns the population

"""mutates a child"""
def mutate(child, s):
    for vert in child.vertices:                         #goes through every vertice in child
        if(rand.randint(1, 100)/100 <= s):              #s percent chance of mutating
            while(True):                            
                rgb = rand.randint(0, len(vert.domain)-1)    
                if(rgb != vert.domain.index(vert.color)):
                    vert.color = vert.domain[rgb]       #makes sure that when it mutates it actually mutates to a new color
                    break





"""crosses 2 graphs vertices over index i"""
def crossOver(p1, p2):                                      
    i = rand.randint(1, len(p1.vertices))                   #random point to "cut" graphs
    leftHalf1 = []
    leftHalf2 = []

    for j in range(i):
        leftHalf1.append(copy.deepcopy(p1.vertices[j]))     #just takes left half of each child
        leftHalf2.append(copy.deepcopy(p2.vertices[j]))
    for j in range(i):
        p1.vertices[j] = leftHalf2[j]                       #and switches them
        p2.vertices[j] = leftHalf1[j]                               
    for j in range(i):
        for vert in p1.vertices:
            if(vert.id == j):
                for neighbor in vert.neighbors:             #have to fix neighbors colors
                    p2.vertices[j].neighbors[vert.neighbors.index(neighbor)] = p2.vertices[neighbor.id]
                    p1.vertices[j].neighbors[vert.neighbors.index(neighbor)] = p1.vertices[neighbor.id]
            for neighbor in vert.neighbors:
                if (neighbor.id == j):
                    p2.vertices[vert.id].neighbors[vert.neighbors.index(neighbor)] = p2.vertices[j]
                    p1.vertices[vert.id].neighbors[vert.neighbors.index(neighbor)] = p1.vertices[j]
    

"""This takes in the graph mutation rate (s) and the size of the population
It is basically brutte force with natural selection and evolution"""
def localSearchGenetic(graph, s, size):                       
    pop = population(graph, size)                             #Creates population... code is above
    localMax = 0                                              #this is my attempt to get out of local maximums basically it half resets the temperature to allow some diverse graphs
    T = 1                                                     #temperature starts at one and when it goes up the selective process is more greedy
    numOfGenerations = 0                                      #This is used to evaluate the effectiveness of the algorithm
    while(True):                                              
        for fam in pop:                                       #fam is short for family... its each graph in the population
            success = 0                                       #only stays zero when a graph satifies the graph coloring problem
            for vert in fam.vertices:
                for neighbor in vert.neighbors:
                    if(neighbor.color == vert.color):
                        success += 1
            if(success == 0):                                 #It's done
                graph = fam
                print(numOfGenerations)
                return fam.vertices
        npop = []                                                       #going to be new population
        for i in  range(int(size/2)):                                   #enough times to replace population
            child1 = copy.deepcopy(randomSelection(pop, T, localMax))   #RandomSelection is the tournament code
            child2 = copy.deepcopy(randomSelection(pop, T, localMax))   #the code is below
            crossOver(child1,child2)                                    #takes half of one graph and half of the other for both children. Code is above
            mutate(child1, s)                           #mutates code is above
            mutate(child2, s)                           #mutates
            npop.append(child1)
            npop.append(child2)
        pop = npop
        if(T<4):                                            #helps you get off of local maximums
            T += .25
        localMax += 1
        if(localMax == 15):
            T = 2.5
            localMax = 0
        numOfGenerations+=1
    


"""Randomly selects a parent from a matingpool built from probability of success
population, Temperature, localMax is more for visualizing the code working"""
def randomSelection(population, T, localMax):               
    matingPool = []                                          
    for pop in population:
        fitness = pop.calcFitness(T, localMax)              #fitness funcion is in graph.py
        fitness *= 100                                      #multiply fitness value by 100
        for i in range(int(fitness)):                       #and put that many copies into a list do simulate probability
            matingPool.append(pop)
    return matingPool[rand.randint(0,len(matingPool)-1)]    #pick a graph from the mating pool

createGraphs() #Generates the list of grpahs.

if(k==4): #sets up the domain of colors given k
    domain = [(255,0,0),(0,255,0),(0,0,255),(230,150,0)]
else:
    domain = [(255,0,0),(0,255,0),(0,0,255)]

for i in range(numGraphs): #iterates thorugh each graph and performs the search algorithms
    graph = graphs[i]
    vertex = graph.pairXY()

    print("Graph " + str(i))


    #Simple Backtracking
#    visited = []
#    simpleBacktracking(graph, vertex, visited)
#    graph.vVisited = visited
#    solutionCheck(graph,i)

    #Backtracking with Forward Checking
    visited = []
    print(backtrackingForwardCheck(graph, vertex, visited))
    graph.vVisited = visited
    solutionCheck(graph,i)

    #Backtracking with Arc Consistency
#    visited = []
#    backtrackingArcConsistency(graph,visited)
#    graph.vVisited = visited
#    solutionCheck(graph,i)

    #Local Search Annealing
#    graph.vVisited = localSearchAnnealing(graph,domain,[])
#    solutionCheck(graph,i)

#    visited = []
#    popSize = 100
#    graph.vVisited = localSearchGenetic(graph, .01, popSize)
#    solutionCheck(graph,i)


#Sets up the graph visualizer
vis = Visual(graphs, .7, 0.2, True, 900, 900)
