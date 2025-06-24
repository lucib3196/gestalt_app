const math = require('mathjs');

const generate = (usePredefinedValues = 0) => {
    const unitSystems = ['si', 'uscs'];

    const units = { 
        "si": { 
            "dist": "m",
            "force": "N",
        },
        "uscs": {
            "dist": "ft",
            "force": "lb",
        }
    };

    // Predefined values for testing
    const predefinedValues = [
        { span: 6, force: 2000, width: 0.1, height: 0.2 }, // SI
        { span: 20, force: 4500, width: 4, height: 6 },  // USCS
    ];

    // Select unit system and generate values
    const unitSel = math.randomInt(0, 2);
    const unitsDist = units[unitSystems[unitSel]].dist;
    const unitsForce = units[unitSystems[unitSel]].force;
    
    let span, force, width, height;

    if (usePredefinedValues) {
        // Use predefined values for testing
        ({ span, force, width, height } = predefinedValues[unitSel]);
    } else {
        // Generate random values if not using predefined values
        span = math.randomInt(5, 20);  // span in meters or feet
        force = math.randomInt(1000, 5000); // load in N or lb
        width = math.random(0.05, 0.15); // width in meters or feet
        height = math.random(0.1, 0.3); // height in meters or feet
    }

    // Calculate moment of inertia (I) for rectangular cross-section
    const I = (width * math.pow(height, 3)) / 12;
    // Maximum bending moment for a point load at center
    const moment = force * (span / 4);
    // Maximum bending stress (sigma)
    const sigma = moment * (height / 2) / I;

    const data = {
        params: {
            span,
            force,
            width,
            height,
            unitsForce,
            unitsDist,
        },
        correct_answers: {
            maxBendingStress: math.round(sigma, 3),
        },
        nDigits: 3,
        sigfigs: 3
    };

    console.log(data);
    return data;
};

module.exports = { generate };