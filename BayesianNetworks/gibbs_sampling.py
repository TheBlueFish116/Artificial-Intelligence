from variable import Variable
from random import choices, uniform
from copy import deepcopy

class GibbsSampling():
    '''
    This is the GibbsSampling class.
    It is responsible for handling
    everything related to GibbsSampling.
    '''
    def __init__(self):
        '''
        Init class with no necessary
        parameters
        '''
        self.evidence = []
        self.num_of_samples = 1000
        self.prev_bn = None
        self.counter = 0

    def set_evidence(self, bn, values_dict):
        '''
        Used to set which variables are evidence
        '''
        for var_name in bn.variables:
            for evidence_name in values_dict['evidence']:
                if(var_name == evidence_name):
                    self.evidence.append(var_name)
                    bn.variables[var_name].value = values_dict['evidence'][evidence_name]

    def is_fs_done(self, bn):
        '''
        Checks if forward checking has completed.
        Allows us to avoid a topological sort.
        '''
        for var in bn.variables:
            if(bn.variables[var].value == None):
                return False
        return True

    def forward_sampling(self, bn):
        '''
        Forward sampling algorithm used to create
        the first sample so that we can build off
        of it in Gibbs Sampling
        '''
        while(self.is_fs_done(bn) == False):
            for var in bn.variables:

                is_evidence = False
                for variable in self.evidence:
                    if(variable == bn.variables[var].name):
                        is_evidence = True
                
                if(is_evidence == False): 
                    domain_values = []
                    probs = []
                    if(bn.variables[var].parents[0] == "No parents"):       #assigns initial root nodes a value
                        for value in bn.variables[var].domain:
                            domain_values.append(value)
                            probs.append(bn.variables[var].info_dict['values'][value])
                        sample_choice = str(choices(domain_values, probs)).replace("'", "")     #uses probability distribution to make choice
                        sample_choice = sample_choice.replace("[", "")
                        sample_choice = sample_choice.replace("]", "")
                        if(bn.variables[var].value == None):
                            bn.variables[var].value = sample_choice

                    else:
                        can_be_assigned = True
                        for parent in bn.variables[var].parents:
                            if(bn.variables[parent].value == None):     #following rule of only sampling from a node in which we have the parent values
                                can_be_assigned = False   

                        if(can_be_assigned):        #if all parents are assigned a value
                            parent_value_string = ""
                            for parent in bn.variables[var].parents:
                                if(parent_value_string == ""):
                                    parent_value_string += bn.variables[parent].value
                                else:
                                    parent_value_string += "," + bn.variables[parent].value

                            for value in bn.variables[var].domain:
                                domain_values.append(value)
                                probs.append(bn.variables[var].probabilities[parent_value_string][value])

                            sample_choice = str(choices(domain_values, probs)).replace("'", "")
                            sample_choice = sample_choice.replace("[", "")
                            sample_choice = sample_choice.replace("]", "")
                            bn.variables[var].value = sample_choice

    '''
    evidence example:
    values_dict = {evidence: {'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'}, query_vars: ['Disease']}
    '''

    def gibbs_sampling(self, bn, values_dict):
        '''
        This is the main function responsible for
        Gibbs Sampling. It handles all aspects of
        the algorithm, from generating the initial data
        to actually sampling from the created distribution.
        '''
        unobserved_vars = []
        self.counter = 0
        records_dict = self.setup_records_dict(bn)
        evidence = list(values_dict['evidence'].keys())
        self.prev_bn = {}
        self.prev_bn = self.handle_forward_checking(bn)
        bn_unobs = self.get_unobs(bn, evidence)
        updated_values = {}
        for value in evidence:
            updated_values[value] = values_dict['evidence'][value]

        # Go through this process enough times to generate a distribution
        for i in range(self.num_of_samples):
            for unobs_key in bn_unobs.keys():
                factors = self.get_all_factors(self.prev_bn, unobs_key)
                numerator = self.create_numerator(unobs_key, factors, updated_values, list(self.prev_bn.variables.keys()), self.prev_bn)
                denominator = self.create_denominator(unobs_key, factors, updated_values, list(self.prev_bn.variables.keys()), self.prev_bn)
                normalized_distro = self.divide_num_by_denom(numerator, denominator)
                sampled_value = self.sample_from_distro(normalized_distro, list(self.prev_bn.variables[unobs_key].info_dict['values'].keys()))
                records_dict[unobs_key][sampled_value] += 1
                updated_values[unobs_key] = sampled_value
        return_dict = {}

        # Process final data before returning it to the user
        for query_var in values_dict['query_vars']:
            return_dict[query_var] = records_dict[query_var]
        for key in return_dict.keys():
            for val in return_dict[key].keys():
                return_dict[key][val] = return_dict[key][val]/self.num_of_samples
            if key not in values_dict['query_vars']:
                return_dict.pop(key)

        # Return final values to user
        return (return_dict, self.counter)

    def handle_forward_checking(self, bn):
        '''
        Utility function to help with accessing
        the forward_sampling function()
        '''
        bn_copy = deepcopy(bn)
        self.forward_sampling(bn_copy)
        return bn_copy

    def get_unobs(self, bn, evidence):
        '''
        Retrieves all of the variables
        that we do not have evidence for
        '''
        bn_copy = bn
        bn_unobs = {}
        for var in bn_copy.variables:
            if var not in evidence:
                bn_unobs[var] = deepcopy(bn.variables[var])
        return bn_unobs

    def get_all_factors(self, bn, voi):
        '''
        Gets the factors that the variables make up
        For example:
            P(var_one|var_two, var_three)
        '''
        bn_copy = bn
        variables = bn_copy.variables
        parents = []
        children = []
        for variable in variables:
            children_names = [child for child in variables[variable].children]
            parent_names = list(variables[variable].info_dict['factors'].keys())
            if voi in children_names and variable != voi:
                parents.append(deepcopy(variable))
            for names in parent_names:
                name_array = names.split(",")
                if voi in name_array and variable != voi:
                    children.append(deepcopy(variable))
        return self.make_factors_from(parents, children, voi, bn)
    
    def make_factors_from(self, parents, children, voi, bn):
        '''
        Puts the factors into dictionaries so that we can
        clearly keep track of relationships
        '''
        bn_copy = bn
        array_of_factors = []
        '''
        Factors array will hold factors that each follow this form
        factor = {
            'child': 'child_name',
            'parents': ['parent_name_one', 'parent_name_two']
        }
        '''
        parent_array = parents.copy()
        array_of_factors.append({
            'child': voi,
            'parents': parent_array
        })
        for child in children:
            this_childs_parents = set()
            this_childs_parents.add(voi)
            for parents_string in bn_copy.variables[child].info_dict['factors'].keys():
                parents_array = parents_string.split(",")
                this_childs_parents.update(parents_array)
            this_childs_parents = list(this_childs_parents)
            array_of_factors.append({
                'child': child,
                'parents': this_childs_parents
            })
        return array_of_factors
    
    def create_numerator(self, voi, factors, updated_values, original_values, bn):
        '''
        Creates the numerator for our probability function by grabbing
        values from parents and their children and creating tables from them
        '''
        bn_copy = bn
        voi_values = list(bn_copy.variables[voi].info_dict['values'].keys())
        # Stores the table that we have to multiply by
        multiply_arr = []
        for voi_value in voi_values:
            multiply_arr.append(1)
        # Stores the numbers that we have to multiply by
        for factor in factors:
            if voi == factor['child']:
                table_array_dict = self.get_probs_given_parents(factor, updated_values, original_values, bn)
                table_value = []
                for table_dict in table_array_dict:
                    table_value.extend(list(table_dict.values()))
            else:
                table_value = []
                for voi_value in voi_values:
                    updated_values[voi] = voi_value
                    child_table = self.get_probs_given_parents(factor, updated_values, original_values, bn)
                    sum_answer = self.sum_probs_given_value(factor, child_table, updated_values)
                    table_value.append(sum_answer)
            for i, operand in enumerate(table_value):
                    multiply_arr[i] *= operand

        return multiply_arr

    def create_denominator(self, voi, factors, updated_values, original_values, bn):
        '''
        Creates the denominator that we use to normalize the numerator. Uses 'summing-out'
        to do this.
        '''
        bn_copy = bn
        voi_values = list(bn_copy.variables[voi].info_dict['values'].keys())
        additions = 0
        for value in voi_values:
            # Do this so that we can pull this value when we get the parent values below
            updated_values[voi] = value
            multiplier = 1
            for factor in factors:
                child_table = self.get_probs_given_parents(factor, updated_values, original_values, bn)
                sum_answer = self.sum_probs_given_value(factor, child_table, updated_values)
                multiplier *= sum_answer
            additions += multiplier
        return additions

    def get_probs_given_parents(self, factor, updated_values, original_values, bn):
        '''
        This gets a variable's values based off of the given values of its parents.
        It is actually kind of a tricky process.
        '''
        self.counter += 1
        bn_copy = bn
        child_name = factor['child']
        child_var = bn_copy.variables[child_name]
        child_dict = child_var.info_dict
        # If child has no parents, just grab its values
        if bn_copy.variables[child_name].parents[0] == "No parents":
            child_vals = bn_copy.variables[child_name].info_dict['values'].copy()
            return_dict = {}
            for val in child_vals.keys():
                return_dict[val] = child_vals[val]
            return [return_dict]
        # Get parent string and split it into something we can use
        parent_string = list(child_dict['factors'].keys())[0]
        parent_array = parent_string.split(",")
        values_strings = list(child_dict['factors'][parent_string].keys())
        values_arrays = [value_array.split(",") for value_array in values_strings]

        given_parent_values = self.get_parent_values(parent_array, updated_values, original_values)
        valid_values = []
        for value_combination in values_arrays:
            combi_copy = value_combination.copy()
            if combi_copy == given_parent_values:
                valid_values.append(combi_copy)
        
        separator = ","
        valid_keys = [separator.join(value_combination) for value_combination in valid_values]

        valid_probs = []
        for key in valid_keys:
            valid_probs.append(bn_copy.variables[child_name].info_dict['factors'][parent_string][key].copy())
        
        # [{'val_one': 0.5, 'val_two': 0.5}, {'val_one': 0.25, 'val_two': 0.75}]
        return valid_probs

    def get_parent_values(self, parent_array, updated_values, original_values):
        '''
        Gets the values of a node's parents
        '''
        return_array = []
        for parent in parent_array:
            return_array.append(self.get_simulated_value(parent, updated_values))
        return return_array
    
    def get_simulated_value(self, var_name, updated_values):
        '''
        Handles grabbing values from the original distribution or the updated
        dictionary depending on whether values exist in the updated dictionary
        '''
        updated_value_names = list(updated_values.keys())
        if var_name in updated_value_names:
            return updated_values[var_name]
        return self.prev_bn.variables[var_name].value

    def sum_probs_given_value(self, factor, table, updated_values):
        '''
        Grabs the probability of a variable having a specific value
        '''
        child_name = factor['child']
        child_value = self.get_simulated_value(child_name, updated_values)
        sum_answer = 0
        for val in table:
            sum_answer += val[child_value]
        return sum_answer

    def divide_num_by_denom(self, numerator, denominator):
        '''
        Handles dividing the numerator table by the denominator
        value
        '''
        numerator_copy = numerator.copy()
        for i, value_dict in enumerate(numerator):
            if denominator != 0:
                numerator_copy[i] = numerator[i]/denominator
            else:
                assert numerator[i] == 0
                numerator_copy[i] = 0
        return numerator_copy

    def sample_from_distro(self, distro, values_array):
        '''
        This handles sampling values from a created distribution.
        We set the variable to have this value for future rounds,
        until it is changed again.
        '''
        curr_distance = 0
        upper_bounds = []
        for val in distro:
            curr_distance += val
            upper_bounds.append(curr_distance)
        random_val = uniform(0, 1)
        answer = 10000
        for upper_bound in upper_bounds:
            if upper_bound >= random_val and answer == 10000:
                answer = upper_bounds.index(upper_bound)
        if answer < len(values_array):
            chosen_key = values_array[answer]
        else:
            chosen_key = values_array[-1]
        return chosen_key
    
    def setup_records_dict(self, bn):
        '''
        This handles setting up the dictionary that we
        use to keep track of which values get selected,
        and how many times.
        '''
        setup_dict = {}
        for key in bn.variables.keys():
            setup_dict[key] = {}
            values = bn.variables[key].info_dict['values'].keys()
            for value in values:
                setup_dict[key][value] = 0
        return setup_dict