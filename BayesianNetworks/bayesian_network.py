from variable import Variable

class BayesianNetwork():
    '''
    This is the BayesianNetwork class.
    Basically, its only job is to hold
    Variable objects in a dictionary.
    '''
    def __init__(self):
        self.variables = {}
        self.variables_dicts = {}