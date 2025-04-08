const math = require('mathjs');

const generate = () => {
    // Define available unit systems
    const units = {
        si: {
            dist: 'm',
            speed: 'm/s',
            acceleration: -9.81 // Acceleration due to gravity in m/s²
        },
        uscs: {
            dist: 'ft',
            speed: 'ft/s',
            acceleration: -32.2 // Acceleration due to gravity in ft/s²
        }
    };

    // Randomly select a unit system
    const unitSystemKeys = Object.keys(units);
    const selectedUnitSystem = units[unitSystemKeys[math.randomInt(0, unitSystemKeys.length)]];

    // Generate random building height and initial speed
    const buildingHeight = math.randomInt(10, 101); // Height in selected units (10 to 100)
    const initialSpeed = math.randomInt(10, 51);   // Speed in selected units (10 to 50)

    // Calculate the time it takes for the ball to hit the ground using the equation:
    // s = ut + 0.5 * a * t², where u = 0 for horizontal throw
    // Therefore, t = sqrt(2 * height / g)
    const time = math.sqrt((-2 * buildingHeight) / selectedUnitSystem.acceleration);

    // Return the generated data
    return {
        params: {
            buildingHeight: buildingHeight,
            unitsDist: selectedUnitSystem.dist,
            initialSpeed: initialSpeed,
            unitsSpeed: selectedUnitSystem.speed
        },
        correct_answers: {
            time: time.toFixed(3) // Return time rounded to 3 decimal places
        },
        nDigits: 3,  // Number of digits after the decimal point
        sigfigs: 3   // Number of significant figures
    };
};

module.exports = {
    generate
};

// Example usage:
console.log(generate());