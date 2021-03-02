asia_dict = {
    'factors': {},
    'values': {
        'yes': 0.01,
        'no': 0.99
    }
}

tub_dict = {
    # Parents
    'factors':{
        # Parent names
        'asia': {
            # Parent value
            'yes': {
                # Probabilities for tub values based on those values
                'yes': 0.05,
                'no': 0.95
            },
            # Parent value
            'no': {
                # Probabilities for tub values based on those values
                'yes': 0.01,
                'no': 0.99
            }
        }
    },
    # Values for tub
    'values': {
        # Values for tub and probabilities that we will find when this var is queried
        'yes': None,
        'no': None
    }
}

smoke_dict = {
    'factors': {},
    'values': {
        'yes': 0.5,
        'no': 0.5
    }
}

lung_dict = {
    'factors': {
        'smoke': {
            'yes': {
                'yes': 0.1,
                'no': 0.9
            },
            'no': {
                'yes': 0.01,
                'no': 0.99
            }
        }
    },
    'values':{
        'yes': None,
        'no': None
    }
}

bronc_dict = {
    'factors': {
        'smoke': {
            'yes': {
                'yes': 0.6,
                'no': 0.4
            },
            'no': {
                'yes': 0.3,
                'no': 0.7
            }
        }
    },
    'values': {
        'yes': None,
        'no': None
    }
}

either_dict = {
    # Parents
    'factors': {
        # Parent names
        'lung_tub': {
            # Parent values (value_for_lung_value_for_tub => yes_yes)
            'yes_yes': {
                # Probabilities for either based on parent vals
                'yes': 1.0,
                'no': 0.0
            },
            # Parent values (value_for_lung_value_for_tub => no_yes)
            'no_yes': {
                # Probabilities for either based on parent vals
                'yes': 1.0,
                'no': 0.0
            },
            # Parent values (value_for_lung_value_for_tub => yes_no)
            'yes_no': {
                # Probabilities for either based on parent vals
                'yes': 1.0,
                'no': 0.0
            },
            # Parent values (value_for_lung_value_for_tub => no_no)
            'no_no': {
                # Probabilities for either based on parent vals
                'yes': 0.0,
                'no': 1.0
            }
        }
    },
    # Values for either and probabilities that we will find when this var is queried
    'values': {
        'yes': None,
        'no': None
    }
}

xray_dict = {
    'factors': {
        'either': {
            'yes': {
                'yes': 0.98,
                'no': 0.02
            },
            'no': {
                'yes': 0.05,
                'no': 0.95
            }
        }
    },
    'values': {
        'yes': None,
        'no': None
    }
}

dysp_dict = {
    'factors': {
        'bronc_either': {
            'yes_yes': {
                'yes': 0.9,
                'no': 0.1
            },
            'no_yes': {
                'yes': 0.7,
                'no': 0.3
            },
            'yes_no': {
                'yes': 0.8,
                'no': 0.2
            },
            'no_no': {
                'yes': 0.1,
                'no': 0.9
            },
        }
    },
    'values': {
        'yes': None,
        'no': None
    }
}