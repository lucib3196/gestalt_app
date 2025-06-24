const math = require('mathjs');

const generate = (usePredefinedValues = 0) => {
    // Predefined values for testing
    const predefinedValues = [
        { m1: 5, theta: 30, mu_s: 0.5, mu_k: 0.3, m2_mass: 10 },
        { m1: 10, theta: 45, mu_s: 0.4, mu_k: 0.2, m2_mass: 15 }
    ];

    // 1. Dynamic Parameter Selection
    const params = usePredefinedValues ? predefinedValues[0] : {
        m1: math.randomInt(1, 21), // mass in kg between 1 and 20
        theta: math.randomInt(10, 41), // angle between 10 and 40 degrees
        mu_s: math.random(0.1, 0.6), // static friction coefficient
        mu_k: math.random(0.1, 0.6), // kinetic friction coefficient
        m2_mass: math.randomInt(5, 21) // mass of block m2 between 5 and 20 kg
    };

    // Constants
    const g = 9.81; // acceleration due to gravity in m/s²

    // 2. Calculate Forces
    const F2 = params.m2_mass * g; // Downward force from m2
    const F1 = params.m1 * g * math.sin(math.unit(params.theta, 'deg')); // Force along incline
    const frictionForce = params.m1 * g * math.cos(math.unit(params.theta, 'deg')) * params.mu_k; // Frictional force

    // 3. Determine Net Force and Acceleration
    const netForce = F2 - (F1 + frictionForce);
    const totalMass = params.m1 + params.m2_mass;
    const acceleration = netForce > 0 ? netForce / totalMass : 0; // Prevent negative acceleration if forces are balanced

    // Return the structured data
    return {
        params: {
            m1: params.m1,
            theta: params.theta,
            mu_s: params.mu_s,
            mu_k: params.mu_k,
            m2: params.m2_mass,
            m1_mass: params.m1, // Added m1_mass to return object
            m2_mass: params.m2_mass // Added m2_mass to return object
        },
        correct_answers: {
            acceleration: math.round(acceleration, 3)
        },
        nDigits: 3,
        sigfigs: 3
    };
};

module.exports = { generate };