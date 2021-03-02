__author__ = "John Dolph, Dylan Rosenbaum"
__date__   = "3-1-2020"

from Visual import Visual
import random as rand
import time
import copy

class Agent:

    def __init__(self, world, init_state, arrows):
        self.kb = []
        self.y_location, self.x_location = init_state
        self.world = world
        self.arrows = arrows

        #frontier update
        self.frontier = []
        if(self.y_location > 0):
            self.frontier.append((self.x_location, self.y_location-1))
        if(self.y_location < self.world.size-1):
            self.frontier.append((self.x_location, self.y_location+1))
        if(self.x_location < self.world.size-1):
            self.frontier.append((self.x_location+1, self.y_location))
        if(self.x_location > 0):
            self.frontier.append((self.x_location-1, self.y_location))

        #Sets up the visualizer
        self.visual = Visual(self.world,0.1,self.world.size*35,self.world.size*35)
        self.visual.refresh(False)

        #statistics and death
        self.stats = [0,0,0,0,0] #gold found, wumpus killed, falls into pits, wumpus kills explorer, cells explored (respectively)
        self.death = False
        self.wuDeath = False
        self.piDeath = False
        self.visited = []


        #hardcoded agent rules
        self.kb.append("+wu(x, y) <= +st(x, y) * 4 | +st(x, y) & -wu(x, y) * 3")
        self.kb.append("-wu(x, y) <> -st(x, y)")
        self.kb.append("-st(x, y) <> -wu(x, y)")
        self.kb.append("+pi(x, y) <= +br(x, y) * 4 | +br(x, y) & -pi(x, y) * 3")
        self.kb.append("-pi(x, y) <> -br(x, y)")

        #visit start node and determine it to be safe
        self.kb.append("+vi(" + str(self.x_location) + ", " + str(self.y_location) + ")")
        self.kb.append("+sa(" + str(self.x_location) + ", " + str(self.y_location) + ")")
        self.kb.append("-wu(" + str(self.x_location) + ", " + str(self.y_location) + ")")
        self.kb.append("-pi(" + str(self.x_location) + ", " + str(self.y_location) + ")")


    """Function to detect percepts from the agent's surroundings"""
    def detect_percepts(self):
        percepts = []
        percept = False
        #these are true if it detects anything in another cell
        if(self.y_location != self.world.size-1):
            if(self.world.world[self.y_location+1][self.x_location] != "em"):
                self.add_to_kb(self.world.world[self.y_location+1][self.x_location], self.y_location+1, self.x_location)
                percepts.append(self.world.world[self.y_location+1][self.x_location])
        if(self.y_location != 0):
            if(self.world.world[self.y_location-1][self.x_location] != "em"):
                self.add_to_kb(self.world.world[self.y_location-1][self.x_location], self.y_location-1, self.x_location)
                percepts.append(self.world.world[self.y_location-1][self.x_location])
        if(self.x_location != self.world.size-1):
            if(self.world.world[self.y_location][self.x_location+1] != "em"):
                self.add_to_kb(self.world.world[self.y_location][self.x_location+1], self.y_location, self.x_location+1)
                percepts.append(self.world.world[self.y_location][self.x_location+1])
        if(self.x_location != 0):
            if(self.world.world[self.y_location][self.x_location-1] != "em"):
                self.add_to_kb(self.world.world[self.y_location][self.x_location-1], self.y_location, self.x_location-1)
                percepts.append(self.world.world[self.y_location][self.x_location-1])
        #this adds any blocked rooms to the knowledge base
        percepts = list(filter(lambda x: x != "bl", percepts))
        if("pi" not in percepts):
            self.add_to_kb("-br", 0, 0)
        if("wu" not in percepts):
            self.add_to_kb("-st", 0, 0)
        if("pi" not in percepts and "wu" not in percepts):
            self.add_to_kb("+sa", 0, 0)

        return percept

    def move(self, instruction):

        #if(len(self.frontier) > 0):
        if(instruction == "north"):
            self.y_location = self.y_location-1
        elif(instruction == "south"):
            self.y_location =  self.y_location+1
        elif(instruction == "east"):
            self.x_location = self.x_location+1
        if(instruction == "west"):
            self.x_location = self.x_location-1

        #updates the frontier
        self.frontier = []
        if(self.y_location > 0):
            self.frontier.append((self.x_location, self.y_location-1))
        if(self.y_location < self.world.size-1):
            self.frontier.append((self.x_location, self.y_location+1))
        if(self.x_location < self.world.size-1):
            self.frontier.append((self.x_location+1, self.y_location))
        if(self.x_location > 0):
            self.frontier.append((self.x_location-1, self.y_location))

        #cells explorer stat update
        self.stats[4] += 1

        #adds the agents's new cell to the visited cells
        self.visited.append((self.x_location, self.y_location))

        #keeps track of safe cells and adds obvious facts to the knowledge base
        if(self.world.world[self.y_location][self.x_location] == "em" and "+sa(" + str(self.x_location) + ", " + str(self.y_location) + ")" not in self.kb):
            self.kb.append("+sa(" + str(self.x_location) + ", " + str(self.y_location) + ")")
            self.kb.append("-wu(" + str(self.x_location) + ", " + str(self.y_location) + ")")
            self.kb.append("-pi(" + str(self.x_location) + ", " + str(self.y_location) + ")")

        #Determines whether or not the agent is killed
        if(self.world.world[self.y_location][self.x_location] == "wu" or self.world.world[self.y_location][self.x_location] == "pi"):
            self.death = True
            if(self.world.world[self.y_location][self.x_location] == "wu"):
                self.wuDeath = True
            if(self.world.world[self.y_location][self.x_location] == "pi"):
                self.piDeath = True

        #communicates the agent location to its world
        self.world.update_agent_location(self.x_location, self.y_location)

        #refreshes thed visualizer
        self.visual.refresh(True)

    def shootArrow(self, cell):
        if(self.world.world[cell[1]][cell[0]] == "wu" and self.arrows > 0):
            print("RAAAWWWRRRR")                                                #we got em
            self.arrows -= 1
            self.stats[1] += 1
            self.world.world[cell[1]][cell[0]] = "em"
            return True
        elif(self.arrows > 0):
            self.arrows -= 1
        return False


    """Adds new information to the agent knowledge base"""
    """takes info of bordering rooms and adds the knowledge of a percept in the current room
        a percept includes a stench a breeze as well as the lack of stenches and breezes"""
    def add_to_kb(self, percept, y, x):
        clause = ""
        if(percept == "bl"):
            clause = "+bl(" + str(x) + ", " + str(y) + ")"
        elif(percept == "wu"):
            clause = "+st(" + str(self.x_location) + ", " + str(self.y_location) + ")"
        elif(percept == "-st"):
            clause = "-st(" + str(self.x_location) + ", " + str(self.y_location) + ")"
            for front in self.frontier:
                if("-wu(" + str(front[0]) + ", " + str(front[1]) + ")" not in self.kb):
                    self.kb.append("-wu(" + str(front[0]) + ", " + str(front[1]) + ")")
        elif(percept == "pi"):
            clause = "+br(" + str(self.x_location) + ", " + str(self.y_location)+ ")"
        elif(percept == "-br"):
            clause = "-br(" + str(self.x_location) + ", " + str(self.y_location) + ")"
            for front in self.frontier:
                if("-pi(" + str(front[0]) + ", " + str(front[1]) + ")" not in self.kb):
                    self.kb.append("-pi(" + str(front[0]) + ", " + str(front[1]) + ")")
        elif(self.world.world[self.y_location][self.x_location] ==  "go"):
            clause = "+go(" + str(self.x_location) + ", " + str(self.y_location) + ")"
        
        elif(percept == "+sa"):
            for front in self.frontier:
                if("+sa(" + str(front[0]) + ", " + str(front[1]) + ")" not in self.kb):
                    self.kb.append("+sa(" + str(front[0]) + ", " + str(front[1]) + ")")
                    self.kb.append("-wu(" + str(front[0]) + ", " + str(front[1]) + ")")
                    self.kb.append("-pi(" + str(front[0]) + ", " + str(front[1]) + ")")
        
        if(clause not in self.kb and clause == "+bl(" + str(x) + ", " + str(y) + ")"):
            self.kb.append("-pi(" + str(x) + ", " + str(y) + ")")
            self.kb.append("-wu(" + str(x) + ", " + str(y) + ")")            

        if(clause not in self.kb and clause != ""):
            self.kb.append(clause)
        return True

    """goes through surrounding rooms and checks logic"""
    def multiples(self, query, G, index, num):
        occurances = 0
        Spercepts = []
        x_index2 = 5
        y_index1 = 7
        y_index2 = 8

        if(query[5] != ","):
            x_index2= 6
            y_index1 = 8
            y_index2 = 9
        if(query[y_index2] != ")"):
            y_index2 += 1
        subString = self.unify(G[index:index+4] + str(int(query[4:x_index2])+1) + ", " + str(query[y_index1:y_index2])+")", G[index:index+9])       #unifys the query with g using UNIFY()
        if(G[index:index+4] + subString[1][1] + ", " + subString[0][1]+")" in self.kb):
            if(num == 1):
                Spercepts.append(G[index:index+4] + subString[1][1] + ", " + subString[0][1]+")")
            if(subString[0] != int(query[4:x_index2] and subString[1] != int(query[y_index1:y_index2]))):
                occurances += 1
        subString = self.unify(G[index:index+4] + str(int(query[4:x_index2])-1) + ", " + str(query[y_index1:y_index2])+")", G[index:index+9])
        if(G[index:index+4] + subString[1][1] + ", " + subString[0][1]+")" in self.kb):
            if(num == 1):
                Spercepts.append(G[index:index+4] + subString[1][1] + ", " + subString[0][1]+")")
            if(subString[0] != int(query[4:x_index2] and subString[1] != int(query[y_index1:y_index2]))):
                occurances += 1
        subString = self.unify(G[index:index+4] + str(query[4:x_index2]) + ", " + str(int(query[y_index1:y_index2])+1)+")", G[index:index+9])
        if(G[index:index+4] + subString[1][1] + ", " + subString[0][1]+")" in self.kb):
            if(num == 1):
                Spercepts.append(G[index:index+4] + subString[1][1] + ", " + subString[0][1]+")")
            if(subString[0] != int(query[4:x_index2] and subString[1] != int(query[y_index1:y_index2]))):
                occurances += 1
        subString = self.unify(G[index:index+4] + str(query[4:x_index2]) + ", " + str(int(query[y_index1:y_index2])-1)+")", G[index:index+9])
        if(G[index:index+4] + subString[1][1] + ", " + subString[0][1]+")" in self.kb):
            if(num == 1):
                Spercepts.append(G[index:index+4] + subString[1][1] + ", " + subString[0][1]+")")
            if(subString[0] != int(query[4:x_index2] and subString[1] != int(query[y_index1:y_index2]))):
                occurances += 1
        if(num == 1):
            return Spercepts
        if(occurances == int(num)):
            return True
        else:
            return False

    """Resolves data in the knowledge base"""
    def resolution(self, query):
        G = []
        index = 23
        for known in self.kb:
            if(query[0:3] == known[0:3]):               #checks if we already know
                if(known == query):
                    return True

        for known in self.kb:
            if(query[0:3] == known[0:3]):               #assumes query is true
                if(known[4:8] == "x, y"):
                    G = known
                    if(G[10:12] == "<="):
                        if(G[index] == "*"):
                            if(self.multiples(query, G, 13, 4)):        #multiples parses out the rule
                                return True                             #UNIFY IS CALLED IN MULTIPLES
                            elif(index + 4 < len(G)):
                                if(G[index+4] == "|"):                      #the code reaches here if there is multiple rules pertaining to the query
                                    G = G.replace((G[12:index+6]), " ")
                                    string = self.multiples(query, G, 13, 1)
                                    for point in string:
                                        if(self.multiples(point, G, index+2, len(self.frontier)-1)):
                                            return True

                            else:
                                return False
                    else:
                        return False

        return False

    """Unifies two terms, returning creating a unifier"""
    def unify(self, t_one, t_two):
        predicates = ["+","-"]

        #create equality statements for term parameters
        equalities = []
        i_t_one = self.kb_interpret(t_one,False)
        i_t_two = self.kb_interpret(t_two,False)
        equalities.append((i_t_one[1], i_t_two[1]))
        equalities.append((i_t_one[2], i_t_two[2]))

        unifier = []

        #begins unification
        while(len(equalities) > 0):
            #takes an equality from the list of equality statements
            e = equalities.pop()
            e_one, e_two = e

            #if the two variables in the equality are not equal
            if(e_one != e_two):

                eqs = []
                if(e_one == "x" or e_one == "y"): #if e_one is one of the possible variables x or y

                    #while equality statements still exist, create a substitution
                    while(len(equalities) > 0):
                        eq = equalities.pop()
                        a,b = eq
                        if(a == e_one):
                            a = e_two
                        if(b == e_one):
                            b = e_two
                        eqs.append((a,b))
                    equalities = eqs
                    unifier.append((e_one, e_two))

                elif(e_two == "x" or e_two == "y"): # if e_two is one of the possible variables x or y

                    #while equality statements still exist, create a substitution
                    while(len(equalities) > 0):
                        eq = equalities.pop()
                        a,b = eq
                        if(a == e_two):
                            a = e_one
                        if(b == e_two):
                            b = e_one
                        eqs.append((a,b))
                    equalities = eqs
                    unifier.append((e_two, e_one))


                elif((e_one[0] in predicates) and (e_two[0] in predicates)): #determines whether or not a predicate is embedded as a variable
                    i_e_one = self.kb_interpret(e_one)
                    i_e_two = self.kb_interpret(e_two)
                    eqs.append((i_e_one[1], i_e_two[1]))
                    eqs.append((i_e_one[2], i_e_two[2]))
                    equalities = eqs
                else:
                    return None #returns None (signifies that unification failed)

        return unifier #returns the unifier when one exists


    """Reconstructs knowledge base string representations into lists for use"""
    def kb_interpret(self,kb_term, truth):

        #Determines the indices of the x and y coordinate values within the kb_term string
        ind_x_start = kb_term.index("(")+1
        ind_x_end = kb_term.index(",")
        ind_y_end = kb_term.rfind(")")

        #Allows embedded predicates (predicates as variables) to be interpretted
        predicates = ["+","-"]
        if(kb_term[ind_x_start] in predicates): #for embedded predicates
            ind_x_end = kb_term.index(")") +1

        #obtains the x and y variable values
        x_loc = kb_term[ind_x_start:ind_x_end]
        y_loc = kb_term[ind_x_end+2:ind_y_end]

        #creates and interpretation tuple that is returned
        i = (kb_term[0:2],x_loc,y_loc,truth)
        return i


    """Allows the agent to ask its knowledge base questions and receive information relating to the questions"""
    def query(self, cell):
        if(self.resolution("+bl(" + str(cell[0]) + ", " + str(cell[1]) + ")")):                                 #is the area blocked
            return False
        if(self.resolution("-br(" + str(self.x_location) + ", " + str(self.y_location) + ")")):                 #does your current location have a breaze
            if(self.resolution("-st(" + str(self.x_location) + ", " + str(self.y_location) + ")")):             #or a stench?
                return True
        if(self.resolution("+sa(" + str(cell[0]) + ", " + str(cell[1]) + ")")):                                 #is the area already known to be safe
            return True
        elif(self.resolution("+wu(" + str(cell[0]) + ", " + str(cell[1]) + ")")):                               #is the area wumpus
            self.kb.append("+wu(" + str(cell[0]) + ", " + str(cell[1]) + ")")
            if(self.shootArrow(cell)):                                                                          #if it is a wumpus... shoot it!
                return True
            else:
                return False
        elif(self.resolution("+pi(" + str(cell[0]) + ", " + str(cell[1]) + ")")):                               #is the area a pit?
            self.kb.append("+pi(" + str(cell[0]) + ", " + str(cell[1]) + ")")
            return False
        return False


    """Determines whether or not the goal state is reached"""
    def check_goal(self):
        if(self.world.world[self.y_location][self.x_location] == "go"):
            print("The explorer found the gold...")
            self.stats[0]+=1
            return True
        return False

    """Displays general information in the IDE console."""
    def show_info(self):
        print("Frontier: " + str(self.frontier))
        print("Visited: " + str(self.visited))
        print("Knowledge Base: " + str(self.kb))


    """sends out the intellegent agent with depth first search"""
    def recursiveSolve(self, nFront, visited):
        visited.append(nFront)
        if(self.x_location < int(nFront[0])):
            self.move("east")
            move = "east"
        elif(self.x_location > int(nFront[0])):
            self.move("west")
            move = "west"
        elif(self.y_location > int(nFront[1])):
            self.move("north")
            move = "north"
        elif(self.y_location < int(nFront[1])):
            self.move("south")
            move = "south"
        frontier = copy.deepcopy(self.frontier)
        if(self.check_goal()):                              #stops when it has found gold
            return True
        if(self.death):                                     #stops when it dies
            return False
        self.detect_percepts()
        for front in frontier:                              #DFS to find every possible move
            if(front not in visited):
                if(self.query(front)):                          #evaluates move
                    if(self.recursiveSolve(front, visited)):       #moves
                        return True
        if(move == "east"):
            self.move("west")
        elif(move == "west"):
            self.move("east")
        elif(move == "north"):
            self.move("south")
        elif(move == "south"):
            self.move("north")
        

    """sends out the reactive agent with depth first search"""
    def reactiveSolve(self, nFront, visited):
        visited.append(nFront)
        if(self.x_location < int(nFront[0])):
            self.move("east")
            move = "east"
        elif(self.x_location > int(nFront[0])):
            self.move("west")
            move = "west"
        elif(self.y_location > int(nFront[1])):
            self.move("north")
            move = "north"
        elif(self.y_location < int(nFront[1])):
            self.move("south")
            move = "south"
        frontier = copy.deepcopy(self.frontier)
        if(self.check_goal()):
            return True                                             #quits if the goal is True
        if(self.death):
            return False                                            #quits if the agent dies
        self.detect_percepts()
        if("+br("+str(self.x_location) + ", " + str(self.y_location) + ")" in self.kb):
            pass
        elif("+st(" + str(self.x_location) + ", " + str(self.y_location) + ")" in self.kb):
            self.shootArrow(frontier[0])
            self.reactiveSolve(frontier[0], visited)
        else:
            for front in frontier:
                if(front not in visited):                                                       #goes through all possible moves
                    if("+bl(" + str(front[0]) + ", " + str(front[1]) + ")" not in self.kb):  
                        if(self.reactiveSolve(front, visited)):
                            return True

        if(not self.death):             #backtracks
            if(move == "east"):
                self.move("west")
            elif(move == "west"):
                self.move("east")
            elif(move == "north"):
                self.move("south")
            elif(move == "south"):
                self.move("north")

    
    """Function to begin solving the wumpus world."""
    def solve(self, type):
        if(type == "react"):
            visited = []
            self.detect_percepts()
            if("+bl(" + str(self.frontier[0][0]) + ", " + str(self.frontier[0][1]) + ")" not in self.kb):
                if(self.reactiveSolve(self.frontier[0], visited)):
                    print("success")
            elif("+bl(" + str(self.frontier[1][0]) + ", " + str(self.frontier[1][1]) + ")" not in self.kb):
                if(self.reactiveSolve(self.frontier[1], visited)):
                    print("success")
            elif("+bl(" + str(self.frontier[2][0]) + ", " + str(self.frontier[2][1]) + ")" not in self.kb):
                if(self.reactiveSolve(self.frontier[2], visited)):
                    print("success")
            else:
                if(self.reactiveSolve(self.frontier[3], visited)):
                    print("success")            


        else:
            visited = []
            self.detect_percepts()
            if("+bl(" + str(self.frontier[0][0]) + ", " + str(self.frontier[0][1]) + ")" not in self.kb):
                if(self.recursiveSolve(self.frontier[0], visited)):
                    print("success")
            elif("+bl(" + str(self.frontier[1][0]) + ", " + str(self.frontier[1][1]) + ")" not in self.kb):
                if(self.recursiveSolve(self.frontier[1], visited)):
                    print("success")
            elif("+bl(" + str(self.frontier[2][0]) + ", " + str(self.frontier[2][1]) + ")" not in self.kb):
                if(self.recursiveSolve(self.frontier[2], visited)):
                    print("success")
            else:
                if(self.recursiveSolve(self.frontier[3], visited)):
                    print("success")

        if(self.death):
            if(self.wuDeath):
                self.stats[3] += 1
            if(self.piDeath):
                self.stats[2] += 1

        #ends the visualizer
        self.visual.end()
