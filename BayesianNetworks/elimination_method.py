from query_method import QueryMethod
from variable import Variable
import random as rand

class EliminationMethod():
        
    def __init__(self, vars, bn, values_dict):
        self.values_dict = values_dict
        self.bn = bn
        self.variables = []
        self.marked = []
        self.optimalOrder = []
        self.convert(vars)
        self.orderVarsToEliminate(self.variables[rand.randint(0, len(self.variables)-1)])

    """ Orders the vars from least number of parents to most.
        It is based on max cardinality function"""

    def orderVarsToEliminate(self, variable):
        self.marked.append(variable)
        if(len(self.marked) == len(self.variables)):
            for var in self.marked:
                self.optimalOrder.insert(0, var)
            self.factorInEvidence()
            return self.optimalOrder
        topCount = 0
        bestVar = variable
        for var in self.variables:
            count = 0
            if(var not in self.marked):
                for parent in var.parents:
                    for mkd in self.marked:
                        if(mkd.name == parent):
                            count += 1
                for child in var.children:
                    for mkd in self.marked:
                        if(mkd.name == child):
                            count += 1
            if(count > topCount):
                topCount = count
                bestVar = var
        return self.orderVarsToEliminate(bestVar)
    
    """gets data into desired format"""
    def convert(self, vars):
        for var in self.bn.variables:
            if(var in vars):
                self.variables.append(self.bn.variables[var])

    """deals with evidence"""
    def factorInEvidence(self):
        for var in self.optimalOrder:
            if(var.name in self.values_dict['evidence']):
                self.optimalOrder.remove(var)
                self.optimalOrder.insert(0, var)
