def generate():
    import numpy as np
    import sympy as sp
    import random

    # Define constants for gravitational acceleration (in m/s² and ft/s²)
    g_si = 9.81  # m/s²
    g_uscs = 32.2  # ft/s²

    # Dynamic Parameter Selection and Unit Selection
    height_units = random.choice(['meters', 'feet'])
    speed_units = random.choice(['m/s', 'ft/s'])

    # Random generation of building height and initial speed
    building_height = random.uniform(10, 50)  # between 10-50 meters or feet
    initial_speed = random.uniform(5, 25)     # between 5-25 m/s or ft/s

    # Calculations for time to reach the ground (ignoring air resistance)
    if height_units == 'meters':
        time_to_ground = sp.sqrt(2 * building_height / g_si)
    else:
        time_to_ground = sp.sqrt(2 * building_height / g_uscs)

    # Return result and parameters as dictionary entries
    return {
        'params': {
            'buildingHeight': building_height,
            'unitsDist': height_units,
            'initialSpeed': initial_speed,
            'unitsSpeed': speed_units,
        },
        'correct_answers': {
            'time': round(time_to_ground.evalf(), 3),
        },
        'nDigits': 3,  # Decimal places
        'sigfigs': 3   # Significant figures
    }


# Example Usage
# result = generate()
# print(result)