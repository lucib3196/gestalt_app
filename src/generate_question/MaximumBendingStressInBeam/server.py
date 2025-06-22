import random


def generate(use_predefined_values=0):
    # Define unit systems
    unitSystems = ['si', 'uscs']
    units = { 
        'si': { 
            'span': 'm', 
            'force': 'N', 
            'dist': 'm', 
        },
        'uscs': { 
            'span': 'feet', 
            'force': 'lb', 
            'dist': 'in',
        }
    }

    # Randomly select unit system
    unitSel = random.randint(0, 1)  # 0 for 'si', 1 for 'uscs'
    unitsSpan = units[unitSystems[unitSel]]['span']
    unitsForce = units[unitSystems[unitSel]]['force']
    unitsDist = units[unitSystems[unitSel]]['dist']

    # Predefined values for testing
    if use_predefined_values:
        span = 6  # meters or feet
        pointLoad = 10000  # Newtons or pounds
        width = 30  # cm or in
        height = 60  # cm or in
    else:
        # Generate random values for parameters using appropriate ranges
        span = round(random.uniform(2, 5), 2)  # spanning between 2 to 5 m or ft
        pointLoad = round(random.uniform(10000, 30000), 2)  # load range 10kN to 30kN or lb
        width = round(random.uniform(20, 60), 2)  # width between 20 to 60 cm or in
        height = round(random.uniform(30, 80), 2)  # height between 30 to 80 cm or in

    # Check if USCS is selected and convert span to inches
    if unitSel == 1:
        span_in_inches = span * 12  # Convert feet to inches (1 foot = 12 inches)
    else:
        span_in_inches = span  # span remains same for SI

    # Calculate the moment of inertia (I) for rectangular section: I = (b*h^3)/12
    I = (width * (height ** 3)) / 12  # in cm^4 if width and height are in cm

    # Calculate maximum bending moment (M) at the center using the formula: M = P * L / 4
    M = pointLoad * (span_in_inches / 4)  # Maximum moment at center (unit consistent)

    # Calculate distance from neutral axis to outer fiber (c): c = h / 2
    c = height / 2  # Distance from neutral axis to outer fiber

    # Calculate bending stress using the formula: sigma_max = (M * c) / I
    sigma_max = (M * c) / I  # Bending stress in N/m^2 or lb/in^2

    # Conversion for SI units
    if unitSel == 0:
        # Convert sigma_max to MPa if SI system is used (1 MPa = 1e6 N/m^2)
        sigma_max = sigma_max / 1e6  # Convert to MPa for SI units
    else:
        # Convert to psi for USCS (1 psi = 6894.76 N/m^2)
        sigma_max = sigma_max / 6894.76  # Convert to psi for USCS units

        # Convert sigma_max from psi to MPa for output (1 MPa = 145.038 psi)
        sigma_max = sigma_max * 0.00689476  # Convert psi to MPa

    # Prepare data to return
    data = {
        'params': {
            'span': span,
            'pointLoad': pointLoad,
            'width': width,
            'height': height,
            'unitsSpan': unitsSpan,
            'unitsForce': unitsForce,
            'unitsDist': unitsDist
        },
        'correct_answers': {
            'maxBendingStress': round(sigma_max, 3)
        },
        'nDigits': 3,
        'sigfigs': 3
    }

    return data

# Example usage
print(generate(0))  # First argument is for using random values