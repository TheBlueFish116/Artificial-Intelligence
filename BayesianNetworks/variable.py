class Variable():
    def __init__(self):
        '''
        Counstructor for variables.
        Used to initialize values that
        are important.
        '''
        self.name = ""
        self.domain_length = 0
        self.domain = []
        self.parents = []
        self.children = []
        self.probabilites = []
        self.info_dict = {}
        self.given = False
        self.value = None
        self.gibbs_data = {}
        self.marginal_distribution = {}

    def set_name(self, name):
        '''
        Can change the name of variables
        '''
        self.name = name

    def set_domain_length(self, domain_length):
        '''
        Set the length of the domain of variables.
        Useful when reading in variables from .BIF
        files
        '''
        self.domain_length = domain_length

    def set_domain(self, domain):
        '''
        Set's the domain length of a given
        variable.
        '''
        self.domain = domain

    def set_parents(self, parents):
        '''
        Set's the variables parents in
        the Bayesian Network.
        '''
        self.parents = parents

    def set_children(self, children):
        '''
        Sets the children of this variable in
        the Bayesian Network.
        '''
        self.children = children

    def set_probabilities(self, probabilities):
        '''
        Sets the probabilities array
        '''
        self.probabilities = probabilities