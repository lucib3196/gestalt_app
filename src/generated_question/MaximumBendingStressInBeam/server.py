import math


def generate(use_predefined_values=0):
    # Predefined values for testing
    predefined_values = [
        {  # Example 1
            'span': 6.0,  # meters
            'load': 3000.0,  # Newtons
            'width': 0.1,  # meters
            'height': 0.2,  # meters
            'unitsLength': 'm',
            'unitsForce': 'N',
            'unitsWidth': 'm',
            'unitsHeight': 'm'
        },
    ]

    if use_predefined_values:
        params = predefined_values[0]
    else:
        # Dynamic value generation could be added here
        # Example of random generation
        import random
        params = {
            'span': round(random.uniform(4.0, 10.0), 3),
            'load': round(random.uniform(1000.0, 5000.0), 3),
            'width': round(random.uniform(0.05, 0.3), 3),
            'height': round(random.uniform(0.1, 0.5), 3),
            'unitsLength': 'm',
            'unitsForce': 'N',
            'unitsWidth': 'm',
            'unitsHeight': 'm'
        }

    # Calculate the maximum bending stress using the formula:
    # sigma_max = (M*c) / I
    # where M = load * (span / 4), c = height / 2, I = (width * height^3) / 12

    span = params['span']
    load = params['load']
    width = params['width']
    height = params['height']

    # Calculate M, c, I
    M = load * (span / 4)  # Bending moment at center
    c = height / 2  # Distance from neutral axis to outer fiber
    I = (width * height ** 3) / 12  # Moment of inertia

    sigma_max = (M * c) / I  # Bending stress in Pascals
    sigma_max_mpa = sigma_max / 1e6  # Convert to MPa

    return {
        'params': params,
        'correct_answers': {'bendingStress': round(sigma_max_mpa, 3)},
        'nDigits': 3,
        'sigfigs': 3
    }