import random


def generate(use_predefined_values=0):
    unitSystems = ['si', 'uscs']
    units = { 
        'si': { 
            'length': 'm',
            'force': 'N',
            'pressure': 'Pa',
        },
        'uscs': {
            'length': 'in',  
            'force': 'lb',
            'pressure': 'psi',
        }
    }

    # Randomly select a unit system
    unit_sel = random.randint(0, 1)
    unitsDistance = units[unitSystems[unit_sel]]['length']
    unitsForce = units[unitSystems[unit_sel]]['force']
    
    if use_predefined_values:
        # Predefined values for testing
        span = 20  # meters or inches
        load = 1000  # Newtons or pounds
        width = 0.3  # meters or inches
        height = 0.5  # meters or inches
    else:
        # Generate random values within specified ranges
        span = round(random.uniform(5, 15), 3)  # Random length between 5 and 15 meter/inches
        load = round(random.uniform(1000, 5000), 2)  # Random load between 1000 and 5000 N/lbs
        width = round(random.uniform(0.1, 0.4), 3)  # Width range 0.1 to 0.4 meters/inches
        height = round(random.uniform(0.2, 0.6), 3)  # Height range 0.2 to 0.6 meters/inches

    # Calculate maximum bending stress
    # Bending stress formula: sigma = (M*c)/I
    # Where M is the moment, c is the distance from the neutral axis, I is the moment of inertia
    I = (width * height**3) / 12  # Moment of inertia for a rectangle
    c = height / 2  # Distance from neutral axis to the outer fiber
    M = load * (span / 4)  # Maximum bending moment at the center for simply supported beam
    max_bending_stress = (M * c) / I  # Bending stress in N/m² (Pa)

    # Convert to appropriate units
    if unit_sel == 1:  # Convert to psi if USCS is selected
        max_bending_stress /= 6894.76  # Convert Pa to psi
    else:
        max_bending_stress /= 1e6  # Convert Pa to MPa if SI is selected

    # Formatting to return 3 significant figures or decimal places
    max_bending_stress = round(max_bending_stress, 3)

    return {
        'params': {
            'span': span,
            'load': load,
            'width': width,
            'height': height,
            'unitsDistance': unitsDistance,
            'unitsForce': unitsForce
        },
        'intermediate_values': {
            'moment': M,
            'moment_of_inertia': I,
            'distance_from_neutral_axis': c
        },
        'correct_answers': {
            'maxBendingStress': max_bending_stress
        },
        'nDigits': 3,
        'sigfigs': 3
    }