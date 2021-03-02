import pytest
from variable_elimination import VariableElimination
from tests.asia.asia_bayes_net import either_var
from tests.asia.asia_bayes_net import network
from bayesian_network import BayesianNetwork
from variable_attributes import VariableAttributes

@pytest.fixture
def setup_data():
    variables = network.variables
    subs = {
        'asia': 'yes',
        'smoke': 'no'
    }
    return (variables, subs)

@pytest.fixture
def setup_child():
    child_vars = VariableAttributes()
    child_file = child_vars.open_file("bif_files/child.bif")
    child_vars.create_variables(child_file)
    child_vars.create_var_dicts()
    child_bn = BayesianNetwork()
    for variable in child_vars.variables:
        child_bn.variables[variable.name] = variable
        child_bn.variable_dicts = child_vars.variable_dicts
    return child_bn

@pytest.fixture
def setup_asia():
    child_vars = VariableAttributes()
    child_file = child_vars.open_file("bif_files/asia.bif")
    child_vars.create_variables(child_file)
    child_vars.create_var_dicts()
    child_bn = BayesianNetwork()
    for variable in child_vars.variables:
        child_bn.variables[variable.name] = variable
        child_bn.variable_dicts = child_vars.variable_dicts
    return child_bn

@pytest.fixture
def setup_values_dict():
    evidence_dict = {
        'evidence': {
            'tub': 'yes'
        },
        'query_vars': ['either']
    }
    graph = {
        'nodes': {
            'asia': {
                'neighbors': []
            },
            'smoke': {
                'neighbors': ['lung', 'bronc']
            },
            'lung': {
                'neighbors': ['either', 'smoke']
            },
            'bronc': {
                'neighbors': ['either', 'dysp', 'smoke']
            },
            'either': {
                'neighbors': ['bronc', 'xray', 'dysp', 'lung']
            },
            'xray': {
                'neighbors': ['either']
            },
            'dysp': {
                'neighbors': ['bronc']
            }
        },
        'dependent_query_vars': {},
        'tree_members': []
    }
    return (evidence_dict, graph)

@pytest.fixture
def setup_no_data():
    evidence_dict = {
        'evidence': {},
        'query_vars': ['either']
    }
    graph = {
        'nodes': {
            'asia': {
                'neighbors': ['tub']
            },
            'tub': {
                'neighbors': ['asia', 'either']
            },
            'smoke': {
                'neighbors': ['lung', 'bronc']
            },
            'lung': {
                'neighbors': ['either', 'smoke']
            },
            'bronc': {
                'neighbors': ['either', 'dysp', 'smoke']
            },
            'either': {
                'neighbors': ['bronc', 'xray', 'dysp', 'lung', 'tub']
            },
            'xray': {
                'neighbors': ['either']
            },
            'dysp': {
                'neighbors': ['bronc']
            }
        },
        'dependent_query_vars': {},
        'tree_members': []
    }
    return (evidence_dict, graph)

@pytest.fixture
def setup_blank_graph():
    return {
        'nodes': {},
        'tree_members': []
    }

def test_subbing(setup_data):
    ve = VariableElimination(network)
    variables, subs = setup_data
    ve.sub_obs(variables, subs)
    assert variables['asia'].info_dict['values']['yes'] == 1.0
    assert variables['asia'].info_dict['values']['no'] == 0.0
    assert variables['smoke'].info_dict['values']['yes'] == 0.0
    assert variables['smoke'].info_dict['values']['no'] == 1.0

def test_find_rel_factors(setup_asia, setup_values_dict):
    network = setup_asia
    ve = VariableElimination(network)
    values_dict, graph = setup_values_dict
    connected_graphs = ve.find_rel_factors(values_dict)
    print(connected_graphs)
    assert connected_graphs == {'either': ['smoke', 'lung', 'bronc', 'either', 'xray', 'dysp', 'tub']}

def test_find_rel_factors_given_either_querying_bronc(setup_values_dict, setup_asia):
    network = setup_asia
    ve = VariableElimination(network)
    values_dict, graph = setup_values_dict
    values_dict['evidence'] = {'either': "yes"}
    values_dict['query_vars'] = [
        'bronc'
    ]
    connected_graphs = ve.find_rel_factors(values_dict)
    print(connected_graphs)
    assert connected_graphs == {'bronc': ['asia', 'tub', 'smoke', 'lung', 'bronc', 'dysp', 'either']}

def test_find_rel_factors_independent(setup_values_dict, setup_asia):
    network = setup_asia
    ve = VariableElimination(network)
    values_dict, graph = setup_values_dict
    values_dict['query_vars'] = [
        'bronc'
    ]
    connected_graphs = ve.find_rel_factors(values_dict)
    print(f'Connected graphs: {connected_graphs}')
    assert connected_graphs == {'bronc': ['smoke', 'lung', 'bronc', 'either', 'xray', 'dysp']}

def test_find_rel_factors_given_lung_bronc(setup_values_dict, setup_asia):
    network = setup_asia
    ve = VariableElimination(network)
    values_dict, graph = setup_values_dict
    values_dict['evidence'] = {
        'bronc': 'yes',
        'lung': 'yes'
    }
    connected_graphs = ve.find_rel_factors(values_dict)
    print(f'Connected graphs: {connected_graphs}')
    assert connected_graphs == {'either': ['asia', 'tub', 'either', 'xray', 'dysp', 'bronc', 'lung']}

def test_given_lung_dysp_want_either_bronc(setup_values_dict, setup_asia):
    network = setup_asia
    ve = VariableElimination(network)
    values_dict, graph = setup_values_dict
    values_dict['evidence'] = {
        'bronc': 'yes',
        'lung': 'yes'
    }
    values_dict['query_vars'] = [
        'either',
        'dysp'
    ]
    connected_graphs = ve.find_rel_factors(values_dict)
    print(f'Connected graphs: {connected_graphs}')
    assert connected_graphs == {'either': ['asia', 'tub', 'either', 'xray', 'dysp', 'bronc', 'lung'], 'dysp': ['asia', 'tub', 'either', 'xray', 'dysp', 'bronc', 'lung']}

def test_given_dysp_want_bronc(setup_values_dict, setup_asia):
    network = setup_asia
    ve = VariableElimination(network)
    values_dict, graph = setup_values_dict
    values_dict['evidence'] = {
        'dysp': 'yes'
    }
    values_dict['query_vars'] = [
        'bronc'
    ]
    connected_graphs = ve.find_rel_factors(values_dict)
    print(f'Connected graphs: {connected_graphs}')
    assert connected_graphs == {'bronc': ['asia', 'tub', 'smoke', 'lung', 'bronc', 'either', 'xray', 'dysp']}

def test_given_bronc_want_dysp(setup_values_dict, setup_asia):
    network = setup_asia
    ve = VariableElimination(network)
    values_dict, graph = setup_values_dict
    values_dict['evidence'] = {
        'dysp': 'yes'
    }
    values_dict['query_vars'] = [
        'bronc'
    ]
    connected_graphs = ve.find_rel_factors(values_dict)
    print(f'Connected graphs: {connected_graphs}')
    assert connected_graphs == {'bronc': ['asia', 'tub', 'smoke', 'lung', 'bronc', 'either', 'xray', 'dysp']}

def test_find_rel_factors_no_evidence_two(setup_no_data, setup_asia):
    network = setup_asia
    ve = VariableElimination(network)
    values_dict, subs = setup_no_data
    values_dict['query_vars'].append('xray')
    connected_graphs = ve.find_rel_factors(values_dict)
    print(connected_graphs)
    assert connected_graphs == {'either': ['asia', 'tub', 'smoke', 'lung', 'bronc', 'either', 'xray', 'dysp'], 'xray': ['asia', 'tub', 'smoke', 'lung', 'bronc', 'either', 'xray', 'dysp']}

def test_find_rel_factors_no_evidence_independent(setup_no_data, setup_asia):
    network = setup_asia
    ve = VariableElimination(network)
    values_dict, subs = setup_no_data
    values_dict['query_vars'] = ['dysp', 'xray']
    connected_graphs = ve.find_rel_factors(values_dict)
    print(connected_graphs)
    #assert connected_graphs == {'dysp': {'dysp': ['dysp'], 'bronc': ['dysp'], 'smoke': ['dysp'], 'either': ['dysp'], 'lung': ['dysp'], 'tub': ['dysp'], 'asia': ['dysp']}, 'xray': {'xray': ['xray'], 'either': ['xray'], 'lung': ['xray'], 'smoke': ['xray'], 'tub': ['xray'], 'asia': ['xray']}}

def test_find_rel_factors_no_evidence_independent_and_dependent(setup_no_data):
    ve = VariableElimination(network)
    values_dict, subs = setup_no_data
    values_dict['query_vars'] = ['dysp', 'either', 'xray']
    connected_graphs = ve.find_rel_factors(values_dict)
    print(connected_graphs)
    #assert connected_graphs == {'dysp': {'dysp': ['dysp'], 'bronc': ['dysp'], 'smoke': ['dysp'], 'either': ['dysp'], 'lung': ['dysp'], 'tub': ['dysp'], 'asia': ['dysp']}, 'either': {'either': ['either'], 'lung': ['either'], 'smoke': ['either'], 'tub': ['either'], 'asia': ['either']}, 'xray': {'xray': ['xray'], 'either': ['xray'], 'lung': ['xray'], 'smoke': ['xray'], 'tub': ['xray'], 'asia': ['xray']}}

def test_we_can_read_in_a_graph(setup_child):
    child_bn = setup_child
    ve = VariableElimination(child_bn)
    values_dict = {}
    values_dict['evidence'] = {
        'GruntingReport': 'yes'
    }
    values_dict['query_vars'] = [
        'CO2'
    ]
    connected_graphs = ve.find_rel_factors(values_dict)
    print(connected_graphs)

def test_we_can_read_in_win95():
    #bn = setup_win95pts

    child_vars = VariableAttributes()
    child_file = child_vars.open_file("bif_files/win95pts.bif")
    child_vars.create_variables(child_file)
    child_vars.create_var_dicts()
    child_bn = BayesianNetwork()
    for variable in child_vars.variables:
        child_bn.variables[variable.name] = variable
        child_bn.variable_dicts = child_vars.variable_dicts

    ve = VariableElimination(child_bn)
    values_dict = {}
    values_dict['evidence'] = {
        'DrvSet': 'Correct'
    }
    values_dict['query_vars'] = [
        'PrtDriver'
    ]
    connected_graphs = ve.find_rel_factors(values_dict)
    print(connected_graphs)