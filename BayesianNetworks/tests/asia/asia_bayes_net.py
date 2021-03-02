from variable import Variable
from bayesian_network import BayesianNetwork
from tests.asia.asia_dicts import asia_dict, tub_dict, smoke_dict, \
    lung_dict, bronc_dict, either_dict, xray_dict, dysp_dict

# Create variables and assign dictionaries
asia_var = Variable()
asia_var.info_dict = asia_dict
asia_var.name = 'asia'

tub_var = Variable()
tub_var.info_dict = tub_dict
tub_var.name = 'tub'

smoke_var = Variable()
smoke_var.info_dict = smoke_dict
smoke_var.name = 'smoke'

lung_var = Variable()
lung_var.info_dict = lung_dict
lung_var.name = 'lung'

bronc_var = Variable()
bronc_var.info_dict = bronc_dict
bronc_var.name = 'bronc'

either_var = Variable()
either_var.info_dict = either_dict
either_var.name = 'either'

xray_var = Variable()
xray_var.info_dict = xray_dict
xray_var.name = 'xray'

dysp_var = Variable()
dysp_var.info_dict = dysp_dict
dysp_var.name = 'dysp'

# Assign children
asia_var.children = [tub_var]
tub_var.children = [either_var]
smoke_var.children = [lung_var, bronc_var]
lung_var.children = [either_var]
bronc_var.children = [dysp_var]
either_var.children = [xray_var, dysp_var]
xray_var.children = []
dysp_var.children = []

var_dict = {
    'asia': asia_var,
    'tub': tub_var,
    'smoke': smoke_var,
    'lung': lung_var,
    'bronc': bronc_var,
    'either': either_var,
    'xray': xray_var,
    'dysp': dysp_var
}

network = BayesianNetwork()
network.variables = var_dict