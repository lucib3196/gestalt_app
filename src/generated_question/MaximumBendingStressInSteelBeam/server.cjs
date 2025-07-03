const math = require('mathjs');

const generate = (usePredefinedValues = 0) => {
    const unitSystems = ['si', 'uscs'];
    const units = { 
        'si': { 
            'dist': 'm', 
            'force': 'N', 
            'stress': 'MPa'
        },
        'uscs': {
            'dist': 'ft', 
            'force': 'lb', 
            'stress': 'psi'
        }
    };

    const unitSel = math.randomInt(0, 2);
    const unitsDistance = units[unitSystems[unitSel]].dist;
    const unitsForce = units[unitSystems[unitSel]].force;
    const stressUnit = units[unitSystems[unitSel]].stress;

    let span, load, width, height;

    if (usePredefinedValues === 1) {
        // Predefined values for testing
        span = 6; // meters or feet depending on the unit
        load = 10000; // Newtons or lbs
        width = 0.2; // meters or feet
        height = 0.3; // meters or feet
    } else {
        // Random value generation
        span = math.random(4, 10); // span length in meters/feet
        load = math.random(5000, 15000); // load in Newtons/pounds
        width = math.random(0.1, 0.5); // width in meters/feet
        height = math.random(0.1, 0.5); // height in meters/feet
    }

    // Calculating maximum bending stress
    const I = (width * math.pow(height, 3)) / 12; // moment of inertia
    const c = height / 2; // distance from the neutral axis to the outer fiber
    const M = (load * span) / 4; // maximum moment
    const sigmaMax = (M * c) / I; // bending stress calculation
    
    // Convert stress to MPa/psi based on unit system
    const convertedSigmaMax = unitSel === 0 ? sigmaMax / 1e6 : sigmaMax / 144;
    
    // Providing intermediate values
    const intermediateValues = {
        moment: M, // Maximum moment
        momentOfInertia: I, // Moment of inertia
        distance: c // Distance from neutral axis
    };
    
    const data = {
        params: {
            span: span,
            load: load,
            width: width,
            height: height,
            unitsDistance: unitsDistance,
            unitsForce: unitsForce,
        },
        correct_answers: {
            maxBendingStress: convertedSigmaMax,
        },
        intermediate_values: intermediateValues, // Adding the intermediate values here
        nDigits: 3,
        sigfigs: 3
    };

    // Explanation of conversion factors:
    // 1 MPa = 1,000,000 Pascals and 1 psi = 144 pounds per square inch.
    // The computed maximum bending stress is provided in the unit corresponding to the selected unit system.
    // Ensure that if USCS system is selected, the computed 'maxBendingStress' is expressed in psi,
    // even though the derived calculations are based on a requirement for unit analysis in MPa.

    return data;
}
console.log(generate())
module.exports = { generate };