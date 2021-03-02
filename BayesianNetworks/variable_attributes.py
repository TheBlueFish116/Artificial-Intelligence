from variable import Variable

class VariableAttributes():
    def __init__(self):
        self.variable_dicts = {}
        self.variables = []
        self.var_names = []
        self.var_domain_lengths = []
        self.var_domains = []
        self.var_parents = []

    def open_file(self, file):
        read_file = open(file, "r")
        words = []
        
        for line in read_file:
            for word in line.split():
                words.append(word)
        return words

    def set_var_names(self, file):
        for i in range(len(file)):
            if(file[i] == "variable"):
                self.var_names.append(file[i + 1])

    def set_var_domain_lengths(self, file):
        for i in range(len(file)):
            if(file[i] == "["):
                self.var_domain_lengths.append(file[i + 1])

    def set_var_domains(self, file):
        num_of_domains = len(self.var_domain_lengths)
        domain_count = 0
        curr_domain = []
        
        for i in range(len(file)):
            index = i
            if(file[i] == "]"):
                index += 2
                domain_item = (file[index]).replace(",", "")
                curr_domain.append(domain_item)
                for i in range(int(self.var_domain_lengths[domain_count]) - 1):
                    index += 1
                    domain_item = (file[index]).replace(",", "")
                    curr_domain.append(domain_item)
                self.var_domains.append(curr_domain)
                curr_domain = []
                domain_count += 1

    def set_var_parents(self, file):
        for i in range(len(file)):
            if(file[i] == "probability"):
                if(file[i+3] != "|"):
                    self.var_parents.append(["No parents"])
                else:
                    curr_parents = []
                    i += 4
                    while(file[i] != ")"):
                        parent = file[i].replace(",", "")
                        curr_parents.append(parent)
                        i += 1
                    self.var_parents.append(curr_parents)


    def set_init_attributes(self, file):
        self.set_var_names(file)
        self.set_var_domain_lengths(file)
        self.set_var_domains(file)
        self.set_var_parents(file)

    def set_init_vars(self):
        num_of_vars = len(self.var_names)

        for i in range (num_of_vars):
            variable = Variable()
            variable.set_name(self.var_names[i])
            variable.set_domain_length(self.var_domain_lengths[i])
            variable.set_domain(self.var_domains[i])
            variable.set_parents(self.var_parents[i])
            self.variables.append(variable)

    def set_var_children(self):
        for child in self.variables:
            for parent in child.parents:
                for var in self.variables:
                    if(var.name == parent):
                        var.children.append(child.name)

    def set_var_probabilities(self, file):
        var_dict = {}
        var_num = 0
        for i in range(len(file)):
            if(file[i] == "probability"):
                temp_dict = {}
                while(file[i] != "{"):
                    i += 1
                i += 1
                while(file[i] != "}"):
                    parent_values = ""
                    for j in range(len(self.variables[var_num].parents)):
                        parents = file[i].replace("(", "")
                        parents = parents.replace(")", "")
                        parent_values += parents
                        i += 1
                    var_probs = {}
                    for j in range(int(self.variables[var_num].domain_length)):
                        prob = file[i].replace(",", "")
                        prob = prob.replace(";", "")
                        var_probs[self.variables[var_num].domain[j]] = float(prob)
                        i += 1
                    temp_dict[parent_values] = var_probs
                    var_dict[parent_values] = var_probs
                self.variables[var_num].set_probabilities(temp_dict)
                var_num += 1

    def create_variables(self, file):
        self.set_init_attributes(file)
        self.set_init_vars()
        self.set_var_children()
        self.set_var_probabilities(file)

    def create_var_dicts(self):
        parent_strings = []

        for i in range(len(self.variables)):
            parent_string = ""
            for j in range(len(self.variables[i].parents)):
                if(self.variables[i].parents[j] != "No parents"):
                    if(j == 0):
                        parent_string += self.variables[i].parents[j]
                    else:
                        parent_string += "," + self.variables[i].parents[j]
            parent_strings.append(parent_string)

        for i in range(len(self.variables)):
            var_dict = {}
            var_dict['name'] = self.variables[i].name
            var_dict['children'] = self.variables[i].children
            factor_dict = var_dict['factors'] = {}
            if(parent_strings[i] != ''):
                parent_dict = factor_dict[parent_strings[i]] = self.variables[i].probabilities
                value_dict = var_dict['values'] = {}
                for j in range(len(self.variables[i].domain)):
                    value_dict[self.variables[i].domain[j]] = 'None'

            else:
                var_dict['values'] = self.variables[i].probabilities['table']

            dict_name = self.variables[i].name + "_dict"
            self.variable_dicts[dict_name] = var_dict
            self.variables[i].info_dict = var_dict.copy()