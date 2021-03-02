import copy
from query_method import QueryMethod
from variable import Variable
from elimination_method import EliminationMethod
from bayesian_network import BayesianNetwork

class VariableElimination(QueryMethod):
    def __init__(self, bn):
        self.bn = bn
        self.variables = self.bn.variables
        self.evidence_visited = {}

    """queries the system"""
    def query(self, values_dict):
        '''
        values_dict = {
            evidence: {
                'var_name': 'value_to_sub_in',
                'var_name_two': 'value_to_sub_in'
            },
            query_vars:['var_name_one', 'var_name_two', 'var_name_three']
        }
        '''
        super().query(values_dict)
        self.sub_obs(self.variables, values_dict['evidence']) 
        rel_factors = self.find_rel_factors(values_dict)
        return self.variableElimFun(rel_factors, values_dict)

    """finds all factors that are conditionally dependant to the query variable"""
    def find_rel_factors(self, values_dict):
        self.evidence_visited = {}
        return_tree = {}
        all_vars = self.variables.keys()
        query_vars = values_dict['query_vars'].copy()
        evidence_vars = (list(values_dict['evidence'].keys()))
        for query_var in query_vars:
            return_tree[query_var] = []
        ancestral_tree = self.get_ancestral_tree(all_vars)
        evidence_pot = {}
        for evidence_var in evidence_vars:
            if evidence_pot == {}:
                evidence_pot = set(ancestral_tree[evidence_var]['ancestors'])
            else:
                evidence_pot.update(ancestral_tree[evidence_var]['ancestors'].copy())
            self.evidence_visited[evidence_var] = {
                'visited': False,
                'visited_by': []
            }

        for query_var in query_vars:
            melting_pot = {}
            query_ancestors = set(ancestral_tree[query_var]['ancestors'])
            if melting_pot == {}:
                melting_pot = query_ancestors.copy()
            else:
                melting_pot.update(query_ancestors.copy())
            melting_pot.update(evidence_pot.copy())
            for gen_var in all_vars:
                gen_ancestors = set(ancestral_tree[gen_var]['ancestors'])
                melting_pot.update(gen_ancestors)
                this_batch = {}
                self.set_neighbors(this_batch, melting_pot.copy())
                self.eliminate_evidence(this_batch, values_dict)
                if self.search(this_batch, query_var, query_var, gen_var, []):
                    return_tree[query_var].append(gen_var)
                melting_pot = melting_pot.difference(gen_ancestors)
                if melting_pot == {}:
                    melting_pot = query_ancestors.copy()
                else:
                    melting_pot.update(query_ancestors.copy())
                if melting_pot == {}:
                    melting_pot = evidence_pot.copy()
                else:
                    melting_pot.update(evidence_pot.copy())
                
        self.add_evidence_vars(return_tree)
        return return_tree




    """Given a bayesian network this functiongoes through the vars in an
    efficient order then sumsout or eliminates each variable one at a time
    untill it has the final probability of the query."""
    def variableElimFun(self, rel_factors, values_dict):
        for query in rel_factors:
            relBn = copy.deepcopy(self.bn)
            evidence = values_dict['evidence']
            elimOrder = EliminationMethod(rel_factors[query], relBn, values_dict).optimalOrder          #gets the optimal ordering
            for var in elimOrder:
                if(var.name == query):
                    elimOrder.remove(var)
                    elimOrder.append(var)
            tempElimOrder = copy.deepcopy(elimOrder)
            self.handleEvidence(values_dict, tempElimOrder)
            print(query)
            i = 0
            for var in elimOrder:
                dependants = []
                for variable in tempElimOrder:
                    if(variable.name in var.children):
                        dependants.append(variable)
                if(var.name != query):
                    if(var.name in evidence):
                        self.sumOutEvidence(var, tempElimOrder)
                    else:
                        self.sumOut(var, tempElimOrder)
                    for vars in tempElimOrder:
                        if(vars.name == var.name):
                            tempElimOrder.remove(vars)
                else:                                                                                     
                    for queryVar in tempElimOrder:
                        for key in queryVar.probabilities:
                            for prob in queryVar.probabilities[key]:
                                print(prob + ": " + str(queryVar.probabilities[key][prob]))

                            
    """gives the evidence the new given property"""
    def handleEvidence(self,values_dict, variables):
        for var in variables:
            if(var.name in values_dict['evidence']):
                for prob in var.probabilities:
                    newProb = {values_dict['evidence'][var.name] : 1}
                    var.probabilities[prob] = newProb
                var.domain = [values_dict['evidence'][var.name]]

    """sums out variables that are evidence"""
    def sumOutEvidence(self, observed, varsToElim):
        dependants = []
        for var in varsToElim:
            if(observed.name in var.parents):
                dependants.append(var)
        for dependant in dependants:
            x = 1
            parents = []
            for parent in dependant.parents:
                for var in varsToElim:
                    if(var.name in parent):
                        parents.append(var)
            for parent in parents:
                x *= len(parent.domain)
            if(x != 1):
                y = x  
                key = [""]*x
                keyWithEvidence = [""]*x
                comma = ""            
                for parent in parents:
                    y /= len(parent.domain)
                    domainNum = -1
                    for i in range(x):
                        if(i%y == 0):
                            if(domainNum+1 != len(parent.domain)):
                                domainNum += 1
                            else:
                                domainNum = 0
                        if(parent.name != observed.name):
                            if(len(key[i]) > 0):
                                key[i] += comma
                            key[i] += parent.domain[domainNum]

                        keyWithEvidence[i] += comma
                        keyWithEvidence[i] += parent.domain[domainNum]
                    comma = ","
                tempDict = {}
                newKey = ""
                j = 0
                for i in range(len(key)):
                    for obj in key:
                        if(i == j):
                            newKey = obj
                            j = 0
                            break
                        j += 1
                    for obj in keyWithEvidence:
                        if(i == j):
                            oldKey = obj
                            j = 0
                            break
                        j += 1
                    tempDict[newKey] = dependant.probabilities[oldKey]
                dependant.probabilities = tempDict

    """Sums out the variables given as well and also
    changes the probabilities of other variables that are
    related"""
    def sumOut(self, varToElim, variables):
        dependants = []
        for var in variables:
            if(varToElim.name in var.parents):
                dependants.append(var)
        for dependant in dependants:
            x = 1
            parents = []
            varLocation = -1
            for parent in dependant.parents:
                for var in variables:
                    if(var.name == parent):
                        parents.append(var)
            j = 0
            for parent in parents:
                if(parent.name == varToElim.name):
                    varLocation = j
                x *= len(parent.domain)
                j += 1 
            if(x != 1):     
                y = x       
                key = [""]*x
                keyWithEvidence = [""]*x
                comma = ""
                for parent in parents:
                    y /= len(parent.domain)
                    domainNum = -1
                    for i in range(x):
                        if(i%y == 0):
                            if(domainNum+1 != len(parent.domain)):
                                domainNum += 1
                            else:
                                domainNum = 0
                        if(parent.name != varToElim.name):
                            if(len(key[i]) > 0):
                                key[i] += comma                            
                            key[i] += parent.domain[domainNum]
                        keyWithEvidence[i] += comma
                        keyWithEvidence[i] += parent.domain[domainNum]
                    comma = ","
            asdf = 0
            if(len(key[0]) == 0):
                key = [""]
            keyInList = []
            keyInListEv = []
            for obj in key:
                split = obj.split(',')
                keyInList.append(split)
            for obj in keyWithEvidence:
                split = obj.split(',')
                keyInListEv.append(split)
            if(len(key[0]) == 0):
                key = ['table']
            tempList = []
            for obj in keyInList:
                if(obj not in tempList):
                    tempList.append(obj)
            keyInList = tempList
            tempDict = {}
            for obj in keyInList:
                newProb = []
                newDict = {}
                for domain in varToElim.domain: 
                    tempKey = ""
                    comma = ""
                    j = 0
                    for i in range(len(obj) + 1):
                        if(varLocation == i):
                            tempKey += comma
                            tempKey += domain
                            comma = ","
                        elif(len(obj[j]) != 0):
                            tempKey +=  comma
                            tempKey += obj[j]
                            j += 1
                            comma = ","                            
                    k = 0
                    for prob in dependant.probabilities[tempKey]:
                        if(len(newProb) != len(dependant.probabilities[tempKey])):
                            newProb.append(dependant.probabilities[tempKey][prob])
                        else:
                            newProb[k] += dependant.probabilities[tempKey][prob]
                            k+= 1
                newKey = ""
                comma = ""
                for thing in obj:
                    newKey += comma
                    newKey += thing
                    comma = ","
                normalization = 0
                for prob in newProb:
                    normalization += prob
                for i in range(len(newProb)):
                    newProb[i] /= normalization
                for i in range(len(dependant.domain)):
                    newDict[dependant.domain[i]] = newProb[i]
                tempDict[newKey] = newDict
            dependant.probabilities = tempDict

                
    def get_ancestral_tree(self, vars_to_get_graphs_for):
        ancestor_graph = {}
        for var in vars_to_get_graphs_for:
            ancestor_graph[var] = {
                'ancestors': [],
                'neighbors': []
            }
            # Returns the ancestrial graph for the query node
            self.get_connected_no_evidence(ancestor_graph[var], var)
        return ancestor_graph

    def set_neighbors(self, graph, variables):
        variable_objs = []
        for variable in variables:
            variable_objs.append(self.bn.variables.get(variable, None))
        for var in variable_objs:
            # Just strings
            graph[var.name] = {
                'ancestors': [],
                'neighbors': []
            }
            children = self.get_children(var)
            parents = self.get_parents(var)
            spouses = self.get_spouses(var, children, parents)
            for child in children:
                if child in variables:
                    graph[var.name]['neighbors'].append(child)
            for parent in parents:
                if parent in variables:
                    graph[var.name]['neighbors'].append(parent)
            for spouse in spouses:
                if spouse in variables:
                    graph[var.name]['neighbors'].append(spouse)
    def eliminate_evidence(self, graph, values_dict):
        for evidence_var in values_dict.get('evidence', None).keys():
            keys = graph.keys()
            if evidence_var in keys:
                graph.pop(evidence_var)
            else:
                for key in keys:
                    neighbors = graph[key]['neighbors']
                    ancestors = graph[key]['ancestors']
                    if evidence_var in neighbors:
                        neighbors.remove(evidence_var)
                    if evidence_var in ancestors:
                        ancestors.remove(evidence_var)

    def sub_obs(self, variables, subs):
        '''
        subs = {
            var_name: value_to_sub_in,
            var_name_two: value_to_sub_in
        }
        '''
        for sub_var in subs.keys():
            value_to_sub = subs[sub_var]
            info_dict = variables[sub_var].info_dict['values']
            for val in info_dict.keys():
                info_dict[val] = 0.0
            variables[sub_var].info_dict['values'][value_to_sub] = 1.0
            variables[sub_var].given = True

    def get_children(self, var):
        return var.children
    
    def get_parents(self, var):
        string_array_parents = var.info_dict['factors'].keys()
        parents_array = []
        for set_of_parents in string_array_parents:
            parents_array.extend(set_of_parents.split(','))
        return parents_array

    def get_spouses(self, var, kids, parents):
        '''
        - var is a Variable
        - kids is an array of strings
        - parents is an array of strings
        - returns an array of strings
        '''
        assert isinstance(var, Variable)
        assert isinstance(kids, list)
        assert isinstance(parents, list)
        parents_set = set(parents)
        spouses = set()
        for kid in kids:
            parents = self.get_parents(self.variables.get(kid, None))
            spouses.update(parents)
        spouses.difference(parents_set)
        spouses = list(spouses)
        if var.name in spouses:
            spouses.remove(var.name)
        return spouses

    def add_evidence_vars(self, graph):
        for key in self.evidence_visited.keys():
            for var in self.evidence_visited[key]['visited_by']:
                graph[var].append(key)

    def search(self, graph, orig_node, curr_node, node_to_find, checked_nodes):
        assert isinstance(graph, dict)
        assert isinstance(curr_node, str)

        if curr_node == node_to_find:
            return True

        neighbors = graph[curr_node]['neighbors']
        for node_name in neighbors:
            if node_name not in checked_nodes:
                checked_nodes.append(node_name)
                if node_name in self.evidence_visited.keys():
                    self.evidence_visited[node_name]['visited'] = True
                    visited_by_set = set(self.evidence_visited[node_name]['visited_by'])
                    visited_by_set.add(orig_node)
                    self.evidence_visited[node_name]['visited_by'] = list(visited_by_set)
                elif self.search(graph, orig_node, node_name, node_to_find, checked_nodes):
                    return True
        return False

    def get_connected_no_evidence(self, graph, curr_node):
        assert isinstance(graph, dict)

        graph['ancestors'].append(curr_node)
        node_var = self.variables[curr_node]
        graph['neighbors'] = self.get_parents(node_var)

        parents = graph['neighbors']
        for parent_name in parents:
            if parent_name not in graph['ancestors']:
                self.get_connected_no_evidence(graph, parent_name)
                graph['neighbors'] = []
