import math

def generate(use_predefined_values=0):
    # Unit definitions
    unitSystems = ['si', 'uscs']
    units = { 
        'si': { 
            'dist': 'm',
            'force': 'N'
        },
        'uscs': {
            'dist': 'feet',
            'force': 'lb'
        }
    }

    # Random unit selection
    unitSel = math.floor(math.random() * 2)
    unitsSpan = units[unitSystems[unitSel]]['dist']
    unitsForce = units[unitSystems[unitSel]]['force']

    # Predefined values for testing
    if use_predefined_values == 1:
        span = 6.0  # meters or feet
        force = 5000.0  # N or lb
        width = 0.3  # meters or feet
        height = 0.5  # meters or feet
    else:
        # Generate random values
        span = round(4 + math.random() * 6, 2)  # Random span between 4 and 10
        force = round(2000 + math.random() * 4000, 2)  # Random force between 2000 and 6000
        width = round(0.1 + math.random() * 0.4, 2)  # Random width between 0.1 and 0.5
        height = round(0.1 + math.random() * 0.4, 2)  # Random height between 0.1 and 0.5

    # Calculate the moment at the center
    moment = (force * span) / 4  # Moment formula (P*L)/4 for simply supported beam

    # Calculate the maximum bending stress
    # Formula: sigma = (M*c)/I, for a rectangular section:
    # c = height/2 and I = (b*h^3)/12
    c = height / 2
    I = (width * height**3) / 12
    sigma = (moment * c) / I

    # Prepare data for return
    data = {
        'params': {
            'span': span,
            'force': force,
            'width': width,
            'height': height,
            'unitsSpan': unitsSpan,
            'unitsForce': unitsForce,
            'unitsDist': units['si']['dist'] if unitSel == 0 else units['uscs']['dist'],
        },
        'correct_answers': {
            'maxBendingStress': round(sigma, 3)
        },
        'nDigits': 3,
        'sigfigs': 3
    }

    return data

# Example usage
print(generate(0))  # Generate random values
print(generate(1))  # Use predefined values