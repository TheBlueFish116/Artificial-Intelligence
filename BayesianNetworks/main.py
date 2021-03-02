from variable_attributes import VariableAttributes
from variable import Variable
from bayesian_network import BayesianNetwork
from elimination_method import EliminationMethod
from variable_elimination import VariableElimination
from gibbs_sampling import GibbsSampling
from copy import deepcopy
import pickle
from pprint import pprint

alarm_bn = BayesianNetwork()
child_bn = BayesianNetwork()
hailfinder_bn = BayesianNetwork()
insurance_bn = BayesianNetwork()
win95pts_bn = BayesianNetwork()




alarm_dict = {
        'evidence': {
            'HRBP': 'HIGH',
            'CO': 'LOW',
            'BP': 'HIGH',
            'HRSAT': 'LOW', 'HREKG': 'LOW', 'HISTORY':'TRUE'
        },
        'query_vars' : ['HYPOVOLEMIA','LVFAILURE','ERRLOWOUTPUT']
}

child_dict = {
            'evidence': {
                'LowerBodyO2': '<5',
                'RUQO2': '>=12',
                'CO2Report': '>=7.5', 
                'XrayReport': 'Asy/Patchy',
                'GruntingReport':'Yes', 'LVHreport':'Yes', 'Age':'11-30 Days'
            },
            'query_vars':['Disease']
        }

hailfinder_dict = {
            'evidence': {
                'R5Fcst': 'XNIL',
                'N34StarFcst': 'XNIL',
                'MountainFcst': 'XNIL',
                'AreaMoDryAir': 'VeryWet',
                'CombVerMo': 'Down', 'AreaMeso_ALS': 'Down', 'CurPropConv': 'Strong'
            },
            'query_vars': ['SatContMoist', 'LLIW']
        }
insurance_dict = {
            'evidence': {
                'Age': 'Adolescent',
                'GoodStudent': 'False',
                'SeniorTrain': 'False',
                'DrivQuality': 'Poor',
                #'MakeModel' : 'Luxury', 'CarValue':'FiftyThou', 'DrivHist':'Zero'
            },
            'query_vars': ['MedCost', 'ILiCost', 'PropCost']
        }
win95pts_dict = {
            'evidence': {
                'Problem1': 'No_Output',
                'Problem2': 'Too_Long',
                'Problem3': 'No',
                'Problem4': 'No',
                'Problem5': 'No',
                'Problem6': 'Yes'
            },
            'query_vars': ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6']
        }

def setup():
    '''
    This method sets up all of the data
    for running the tests
    '''
    alarm_vars = VariableAttributes()
    child_vars = VariableAttributes()
    hailfinder_vars = VariableAttributes()
    insurance_vars = VariableAttributes()
    win95pts_vars = VariableAttributes()

    alarm_file = alarm_vars.open_file("bif_files/alarm.bif")
    child_file = child_vars.open_file("bif_files/child.bif")
    hailfinder_file = hailfinder_vars.open_file("bif_files/hailfinder.bif")
    insurance_file = insurance_vars.open_file("bif_files/insurance.bif")
    win95pts_file = win95pts_vars.open_file("bif_files/win95pts.bif")

    alarm_vars.create_variables(alarm_file)
    child_vars.create_variables(child_file)
    hailfinder_vars.create_variables(hailfinder_file)
    insurance_vars.create_variables(insurance_file)
    win95pts_vars.create_variables(win95pts_file)

    alarm_vars.create_var_dicts()
    child_vars.create_var_dicts()
    hailfinder_vars.create_var_dicts()
    insurance_vars.create_var_dicts()
    win95pts_vars.create_var_dicts()

    #print(child_vars.variable_dicts['HypoxiaInO2_dict'])

    '''
    The example above produces:

    {'name': 'HypoxiaInO2',
    'children': ['LowerBodyO2', 'RUQO2'], 
    'factors': {'CardiacMixing,LungParench': 
    {'None,Normal': 
    {'Mild': 0.93, 'Moderate': 0.05, 'Severe': 0.02}, 'Mild,Normal': 
    {'Mild': 0.1, 'Moderate': 0.8, 'Severe': 0.1}, 'Complete,Normal': 
    {'Mild': 0.1, 'Moderate': 0.7, 'Severe': 0.2}, 'Transp.,Normal': 
    {'Mild': 0.02, 'Moderate': 0.18, 'Severe': 0.8}, 'None,Congested': 
    {'Mild': 0.15, 'Moderate': 0.8, 'Severe': 0.05}, 'Mild,Congested': 
    {'Mild': 0.1, 'Moderate': 0.75, 'Severe': 0.15}, 'Complete,Congested': 
    {'Mild': 0.05, 'Moderate': 0.65, 'Severe': 0.3}, 'Transp.,Congested': 
    {'Mild': 0.1, 'Moderate': 0.3, 'Severe': 0.6}, 'None,Abnormal': 
    {'Mild': 0.7, 'Moderate': 0.2, 'Severe': 0.1}, 'Mild,Abnormal': 
    {'Mild': 0.1, 'Moderate': 0.65, 'Severe': 0.25}, 'Complete,Abnormal': 
    {'Mild': 0.1, 'Moderate': 0.5, 'Severe': 0.4}, 'Transp.,Abnormal': 
    {'Mild': 0.02, 'Moderate': 0.18, 'Severe': 0.8}}},
    'values': 
    {'Mild': 'None', 'Moderate': 'None', 'Severe': 'None'}}
    '''

    for variable in alarm_vars.variables:
        alarm_bn.variables[variable.name] = variable
    alarm_bn.variable_dicts = alarm_vars.variable_dicts

    for variable in child_vars.variables:
        child_bn.variables[variable.name] = variable
    child_bn.variable_dicts = child_vars.variable_dicts

    for variable in hailfinder_vars.variables:
        hailfinder_bn.variables[variable.name] = variable
    hailfinder_bn.variable_dicts = hailfinder_vars.variable_dicts

    for variable in insurance_vars.variables:
        insurance_bn.variables[variable.name] = variable
    insurance_bn.variable_dicts = insurance_vars.variable_dicts

    for variable in win95pts_vars.variables:
        win95pts_bn.variables[variable.name] = variable
    win95pts_bn.variable_dicts = win95pts_vars.variable_dicts

def run_gibbs():
    '''
    This runs all of the queries that
    we need using Gibbs sampling
    '''

    # Setup all of the Bayesian Networks
    # for the tests
    alarm_bn_one = deepcopy(alarm_bn)
    alarm_bn_two = deepcopy(alarm_bn)
    child_bn_one = deepcopy(child_bn)
    child_bn_two = deepcopy(child_bn)
    hailfinder_bn_one = deepcopy(hailfinder_bn)
    hailfinder_bn_two = deepcopy(hailfinder_bn)
    insurance_bn_one = deepcopy(insurance_bn)
    insurance_bn_two = deepcopy(insurance_bn)
    win_bn_one = deepcopy(win95pts_bn)
    win_bn_two = deepcopy(win95pts_bn)
    win_bn_three = deepcopy(win95pts_bn)
    win_bn_four = deepcopy(win95pts_bn)
    win_bn_five = deepcopy(win95pts_bn)
    win_bn_six = deepcopy(win95pts_bn)

    # Setup all of the dictionaries
    queries = {
        'alarm_no_evidence': {
            'evidence': {},
            'query_vars': ['HYPOVOLEMIA', 'LVFAILURE', 'ERRLOWOUTPUT'],
            'bn': alarm_bn_one
        },

        'alarm_little_evidence': {
            'evidence': {'HRBP': 'HIGH', 'CO': 'LOW', 'BP': 'HIGH'},
            'query_vars': ['HYPOVOLEMIA', 'LVFAILURE', 'ERRLOWOUTPUT'],
            'bn': alarm_bn_one
        },

        'alarm_moderate_evidence': {
            'evidence': {'HRBP':'HIGH', 'CO': 'LOW', 'BP': 'HIGH', 'HRSAT': 'LOW', 'HREKG': 'LOW', 'HISTORY': 'TRUE'},
            'query_vars': ['HYPOVOLEMIA', 'LVFAILURE', 'ERRLOWOUTPUT'],
            'bn': alarm_bn_two
        },

        'child_no_evidence': {
            'evidence': {},
            'query_vars': ['Disease'],
            'bn': child_bn_one
        },

        'child_little_evidence': {
            'evidence': {'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'},
            'query_vars': ['Disease'],
            'bn': child_bn_one
        },

        'child_moderate_evidence': {
            'evidence': {'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy', 'GruntingReport': 'yes', 'LVHReport': 'yes', 'Age': '11-30_days'},
            'query_vars': ["Disease"],
            'bn': child_bn_two
        },

        'hailfinder_no_evidence': {
            'evidence': {},
            'query_vars': ['SatContMoist', 'LLIW'],
            'bn': hailfinder_bn_one
        },

        'hailfinder_little_evidence': {
            'evidence': {'RSFcst': 'XNIL', 'N32StarFcst': 'XNIL', 'MountainFcst': 'XNIL', 'AreaMoDryAir': 'VeryWet'},
            'query_vars': ['SatContMoist', 'LLIW'],
            'bn': hailfinder_bn_one
        },

        'hailfinder_moderate_evidence': {
            'evidence': {'RSFcst': 'XNIL', 'N32StarFcst': 'XNIL', 'MountainFcst': 'XNIL', 'AreaMoDryAir': 'VeryWet', 'CombVerMo': 'Down', 'AreaMeso_ALS': 'Down', 'CurPropConv': 'Strong'},
            'query_vars': ['SatContMoist', 'LLIW'],
            'bn': hailfinder_bn_two
        },

        'insurance_no_evidence': {
            'evidence': {},
            'query_vars': ['MedCost', 'ILiCost', 'PropCost'],
            'bn': insurance_bn_one
        },

        'insurance_little_evidence': {
            'evidence': {'Age': 'Adolescent', 'GoodStudent': 'False', 'SeniorTrain': 'False', 'DrivQuality': 'Poor'},
            'query_vars': ['MedCost', 'ILiCost', 'PropCost'],
            'bn': insurance_bn_one
        },

        'insurance_moderate_evidence': {
            'evidence': {'Age': 'Adolescent', 'GoodStudent': 'False', 'SeniorTrain': 'False', 'DrivQuality': 'Poor', 'MakeModel': 'Luxury', 'CarValue': 'FiftyThou', 'DrivHistory': 'Zero'},
            'query_vars': ['MedCost', 'ILiCost', 'PropCost'],
            'bn': insurance_bn_two
        },

        'win95pts_no_evidence': {
            'evidence': {},
            'query_vars': ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6'],
            'bn': win_bn_one
        },

        'win95pts_one_evidence': {
            'evidence': {'Problem1': 'No_Output'},
            'query_vars': ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6'],
            'bn': win_bn_one
        },

        'win95pts_two_evidence': {
            'evidence': {'Problem2': 'Too_Long'},
            'query_vars': ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6'],
            'bn': win_bn_two
        },

        'win95pts_three_evidence': {
            'evidence': {'Problem3': 'No'},
            'query_vars': ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6'],
            'bn': win_bn_three
        },

        'win95pts_four_evidence': {
            'evidence': {'Problem4': 'No'},
            'query_vars': ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6'],
            'bn': win_bn_four
        },

        'win95pts_five_evidence': {
            'evidence': {'Problem5': 'No'},
            'query_vars': ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6'],
            'bn': win_bn_five
        },

        'win95pts_six_evidence': {
            'evidence': {'Problem6': 'Yes'},
            'query_vars': ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6'],
            'bn': win_bn_six
        }
    }

    report = {}
    for key in queries.keys():
        report[key] = {
            'output': None,
            'steps': 0
        }

    # Run the qureries and gather results
    gibbs = GibbsSampling()
    for key in queries.keys():
        query_dict = {}
        query_dict['evidence'] = queries[key]['evidence']
        query_dict['query_vars'] = queries[key]['query_vars']
        bn = queries[key]['bn']
        output, steps = gibbs.gibbs_sampling(bn, query_dict)
        report[key]['output'] = output
        report[key]['steps'] = steps
        print(f'{key}')

    with open('gibbs_output.pickle', 'wb') as output_file:
        pickle.dump(report, output_file)
    
    pprint(f'{report}')

if __name__ == '__main__':
    '''
    Main entry point for our
    program
    '''
    setup()
    run_gibbs()
    bayesnet = alarm_bn
    test = VariableElimination(alarm_bn)
    test.query(alarm_dict)


