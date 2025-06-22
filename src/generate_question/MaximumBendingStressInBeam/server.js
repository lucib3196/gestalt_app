const math = require('mathjs');

const generate = (usePredefinedValues = 0) => {
    const unitSystems = ['si', 'uscs'];

    const units = { 
        "si": { 
            "dist": "m",
            "force": "N"
        },
        "uscs": {
            "dist": "feet",
            "force": "lb"
        }
    }; 

    // Select a random unit system (0 for SI, 1 for USCS)
    const unitSel = math.randomInt(0, 2);
    const unitsDist = units[unitSystems[unitSel]].dist;
    const unitsForce = units[unitSystems[unitSel]].force;

    let params;

    if (usePredefinedValues === 1) {
        // Predefined test values
        params = {
            span: 10,
            pointLoad: 5000,
            width: 0.3,
            height: 0.5,
            unitsSpan: units[unitSystems[unitSel]].dist,
            unitsForce: units[unitSystems[unitSel]].force,
            unitsDist: units[unitSystems[unitSel]].dist
        };
    } else {
        // Random values generation
        params = {
            span: math.randomInt(8, 20),  // Span in meters or feet
            pointLoad: math.randomInt(4000, 10000), // Point load in N or lb
            width: math.randomFloat(0.1, 0.5), // Width in meters or feet
            height: math.randomFloat(0.1, 2), // Height in meters or feet
            unitsSpan: units[unitSystems[unitSel]].dist,
            unitsForce: units[unitSystems[unitSel]].force,
            unitsDist: units[unitSystems[unitSel]].dist
        };
    }

    // Calculate the maximum bending stress
    const moment = (params.pointLoad * params.span) / 4;  // Maximum moment at center for point load
    const I = (params.width * math.pow(params.height, 3)) / 12; // Moment of inertia for rectangular section
    const c = params.height / 2; // Distance from neutral axis to outer fiber

    // Bending stress formula
    const maxBendingStress = moment * c / I; 

    // Initialize maxBendingStressMPa variable
    let maxBendingStressMPa;

    // Convert maxBendingStress based on the unit system
    if (unitSel === 0) {
        // For SI, convert N/m^2 to MPa
        const conversionFactor = 1e6; // N/m^2 to MPa conversion factor
        maxBendingStressMPa = maxBendingStress / conversionFactor;
    } else {
        // For USCS, calculate in psi and convert to MPa
        const maxBendingStressPsi = maxBendingStress * 0.000145038; // Convert bending stress to psi (1 N/m^2 = 0.000145038 psi)
        const psiToMPaConversionFactor = 0.00689476; // 1 psi ≈ 0.00689476 MPa
        maxBendingStressMPa = maxBendingStressPsi * psiToMPaConversionFactor; // Convert from psi to MPa
    }

    return {
        params: params,
        correct_answers: {
            maxBendingStress: math.round(maxBendingStressMPa, 3) // Round to 3 decimal places
        },
        nDigits: 3,
        sigfigs: 3
    };
};

module.exports = { generate };