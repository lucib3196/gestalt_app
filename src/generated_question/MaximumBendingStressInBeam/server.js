const math = require('mathjs');

const generate = (usePredefinedValues = 0) => {
    const unitSystems = ['si', 'uscs'];
    const units = { 
        "si": { 
            "length": "m",
            "force": "N",
            "width": "m",
            "height": "m"
        },
        "uscs": {
            "length": "ft",
            "force": "lb",
            "width": "in",
            "height": "in"
        }
    };
    const unitSel = math.randomInt(0, 2);
    const unitsLength = units[unitSystems[unitSel]].length;
    const unitsForce = units[unitSystems[unitSel]].force;
    const unitsWidth = units[unitSystems[unitSel]].width;
    const unitsHeight = units[unitSystems[unitSel]].height;

    let span, load, width, height;
    if (usePredefinedValues) {
        // Predefined values for quick testing 
        span = 5;  // example span (in m or ft)
        load = 10000;  // example load (in N or lb)
        width = 0.3;  // example width (in m or in)
        height = 0.5;  // example height (in m or in)
    } else {
        // Generate random values 
        span = math.random(4, 6);  // 4 to 6 meters or ft
        load = math.random(8000, 12000);  // Load between 8000 and 12000 N or lb
        width = math.random(0.2, 0.4);  // width between 0.2 and 0.4 meters or in
        height = math.random(0.3, 0.7);  // height between 0.3 and 0.7 meters or in
    }

    // Calculating the moment of inertia, I = (b*h^3)/12 for rectangular cross-section
    const momentOfInertia = (width * math.pow(height, 3)) / 12;
    // Maximum bending moment for a point load at center: M = (P*L)/4
    const bendingMoment = (load * span) / 4;
    // Maximum bending stress: sigma_max = (M*c)/I where c is distance from neutral axis, c = h/2
    const c = height / 2;
    const sigmaMax = (bendingMoment * c) / momentOfInertia;  // Result will be in N/m^2 or lb/in^2 based on units

    return {
        params: {
            span: span,
            load: load,
            width: width,
            height: height,
            unitsLength: unitsLength,
            unitsForce: unitsForce,
            unitsWidth: unitsWidth,
            unitsHeight: unitsHeight,
        },
        correct_answers: {
            bendingStress: math.round(sigmaMax / (unitSel === 0 ? 1e6 : 1), 3)  // Convert to MPa
        },
        nDigits: 3,
        sigfigs: 3
    };
};
console.log(generate())
module.exports = { generate };