from variable_attributes import VariableAttributes
from bayesian_network import BayesianNetwork
from gibbs_sampling import GibbsSampling
import pytest

@pytest.fixture
def setup_asia_test():
    child_vars = VariableAttributes()
    child_file = child_vars.open_file("bif_files/asia.bif")
    values_dict = {'evidence': {'bronc': 'yes', 'asia': 'yes'}, 'query_vars': ['either']}
    child_vars.create_variables(child_file)
    child_vars.create_var_dicts()
    child_bn = BayesianNetwork()
    for variable in child_vars.variables:
        child_bn.variables[variable.name] = variable
        child_bn.variable_dicts = child_vars.variable_dicts
    gibbs = GibbsSampling()
    gibbs.set_evidence(child_bn, values_dict)
    gibbs.forward_sampling(child_bn)
    gibbs.prev_bn = child_bn
    return child_bn, gibbs

@pytest.fixture
def helpful_structures():
    factor = {
        'child': 'lung',
        'parents': ['smoke']
    }
    updated_values = {
        'lung': "yes",
        'smoke': "yes" ,
        'tub': "no",
    }
    table = [{'yes': 0.5, 'no': 0.5}, {'yes': 0.25, 'no': 0.75}]
    return (factor, updated_values, table)

@pytest.fixture
def get_query():
    return {'evidence': {'bronc': 'yes', 'asia': 'yes'}, 'query_vars': ['either']}

def test_gibbs_sampling(setup_asia_test):
    bn, gibbs = setup_asia_test
    setup_dict = gibbs.setup_records_dict(bn)
    print(setup_dict)

def test_sample_from_distro(setup_asia_test):
    bn, gibbs = setup_asia_test
    distro = [
        0.1,
        0.9
    ]
    values = ['var_1', 'var_2']
    answer = gibbs.sample_from_distro(distro, values)
    print(answer)

def test_divide_num_by_denom(setup_asia_test):
    bn, gibbs = setup_asia_test
    numerator = [{"var_one": 2, "var_two": 4, "var_three": 6}, {"var_a": 20, "var_b": 40, "var_c": 60}]
    denominator = 2
    ans = gibbs.divide_num_by_denom(numerator, denominator)
    print(ans)

def test_simulated_value(setup_asia_test):
    bn, gibbs = setup_asia_test
    gibbs.forward_sampling(bn)
    var_name = "var_one"
    updated_values = {
        'var_one': "val_one"
    }
    value = gibbs.get_simulated_value(var_name, updated_values)
    assert value == "val_one"

def test_sum_probs_given_value(setup_asia_test, helpful_structures):
    bn, gibbs = setup_asia_test
    factor, updated_values, table = helpful_structures
    gibbs.forward_sampling(bn)
    ans = gibbs.sum_probs_given_value(factor, table, updated_values)
    print(ans)
    assert ans == 0.75

def test_get_parent_values(setup_asia_test, helpful_structures):
    bn, gibbs = setup_asia_test
    factor, updated_values, table = helpful_structures
    gibbs.forward_sampling(bn)
    parent_array = ['smoke', 'tub']
    ans = gibbs.get_parent_values(parent_array, updated_values, [])
    assert ans == ["yes", "no"]

def test_probs_given_parents_voi_child(setup_asia_test, helpful_structures):
    bn, gibbs = setup_asia_test
    factor, updated_values, table = helpful_structures
    factor = {
        'child': 'either',
        'parents': ['lung', 'tub']
    }
    ans = gibbs.get_probs_given_parents(factor, updated_values, [], bn)
    assert ans == [{'yes': 1.0, 'no': 0.0}]

def test_probs_given_parents_voi_child_again(setup_asia_test, helpful_structures):
    bn, gibbs = setup_asia_test
    factor, updated_values, table = helpful_structures
    updated_values = updated_values.copy()
    updated_values['lung'] = 'no'
    factor = {
        'child': 'either',
        'parents': ['lung', 'tub']
    }
    ans = gibbs.get_probs_given_parents(factor, updated_values, [], bn)
    print(ans)
    assert ans == [{'yes': 0.0, 'no': 1.0}]

def test_probs_given_parents_voi_parent(setup_asia_test, helpful_structures):
    bn, gibbs = setup_asia_test
    factor, updated_values, table = helpful_structures
    updated_values = updated_values.copy()
    updated_values['asia'] = 'no'
    updated_values.pop('tub')
    factor = {
        'child': 'tub',
        'parents': ['asia']
    }
    ans = gibbs.get_probs_given_parents(factor, updated_values, [], bn)
    assert ans == [{'yes': 0.01, 'no': 0.99}]

def test_probs_given_parents_voi_parent_lung(setup_asia_test, helpful_structures):
    bn, gibbs = setup_asia_test
    factor, updated_values, table = helpful_structures
    updated_values = updated_values.copy()
    updated_values['tub'] = 'no'
    factor = {
        'child': 'either',
        'parents': ['lung', 'tub']
    }
    ans = gibbs.get_probs_given_parents(factor, updated_values, [], bn)
    assert ans == [{'yes': 1.0, 'no': 0.0}]

def test_create_denominator(setup_asia_test, helpful_structures):
    bn, gibbs = setup_asia_test
    factor, updated_values, table = helpful_structures
    updated_values = updated_values.copy()
    updated_values = updated_values.copy()
    updated_values.pop('lung')
    updated_values['either'] = 'yes'
    updated_values['tub'] = 'no'
    factors = [
        {
            'child': 'either',
            'parents': ['lung', 'tub']
        },
        {
            'child': 'lung',
            'parents': ['smoke']
        }
    ]
    voi = 'lung'
    ans = gibbs.create_denominator(voi, factors, updated_values, [], bn)
    assert ans == 0.1

def test_create_numerator_voi_child(setup_asia_test, helpful_structures):
    bn, gibbs = setup_asia_test
    factor, updated_values, table = helpful_structures
    updated_values = updated_values.copy()
    updated_values = updated_values.copy()
    updated_values.pop('lung')
    updated_values['either'] = 'yes'
    updated_values['tub'] = 'no'
    factors = [
        {
            'child': 'either',
            'parents': ['lung', 'tub']
        },
        {
            'child': 'lung',
            'parents': ['smoke']
        }
    ]
    voi = 'lung'
    ans = gibbs.create_numerator(voi, factors, updated_values, [], bn)
    assert ans == [0.1, 0]

def test_break_numerator(setup_asia_test, helpful_structures):
    bn, gibbs = setup_asia_test
    factor, updated_values, table = helpful_structures
    updated_values = updated_values.copy()
    updated_values = {
        'asia': 'yes',
        'smoke': 'yes',
        'either': 'yes',
        'lung': 'yes'
    }
    factors = [
        {
            'child': 'tub',
            'parents': ['asia']
        },
        {
            'child': 'either',
            'parents': ['lung', 'tub']
        }
    ]
    voi = 'tub'
    ans = gibbs.create_numerator(voi, factors, updated_values, [], bn)
    print(ans)

def test_break_denominator(setup_asia_test, helpful_structures):
    bn, gibbs = setup_asia_test
    factor, updated_values, table = helpful_structures
    updated_values = updated_values.copy()
    updated_values = updated_values.copy()
    updated_values['either'] = 'yes'
    updated_values = {
        'asia': 'yes',
        'smoke': 'yes',
        'either': 'yes',
        'lung': 'yes    '
    }
    factors = [
        {
            'child': 'tub',
            'parents': ['asia']
        },
        {
            'child': 'either',
            'parents': ['tub', 'lung']
        }
    ]
    voi = 'tub'
    ans = gibbs.create_denominator(voi, factors, updated_values, [], bn)
    print(ans)


def test_get_all_factors(setup_asia_test, helpful_structures):
    bn, gibbs = setup_asia_test
    factor, updated_values, table = helpful_structures
    ans = gibbs.get_all_factors(bn, 'either')
    assert ans == [{'child': 'either', 'parents': ['tub', 'lung']}, {'child': 'xray', 'parents': ['either']}, {'child': 'dysp', 'parents': ['bronc', 'either']}]

def test_gibbs_sampling(setup_asia_test, get_query):
    bn, gibbs = setup_asia_test
    query_dict = get_query
    ans = gibbs.gibbs_sampling(bn, query_dict)
    print(ans)