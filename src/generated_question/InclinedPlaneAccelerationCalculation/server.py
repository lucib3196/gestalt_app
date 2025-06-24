import random
import math


def generate(use_predefined_values=0):
    # Predefined values for testing
    predefined_values = [
        {"m1": 5, "theta": 30, "mu_s": 0.5, "mu_k": 0.3, "m2_mass": 3},
        {"m1": 7, "theta": 45, "mu_s": 0.6, "mu_k": 0.4, "m2_mass": 4},
        {"m1": 10, "theta": 20, "mu_s": 0.7, "mu_k": 0.5, "m2_mass": 8},
    ]

    # 1. Dynamic Parameter Selection
    if use_predefined_values:
        params = predefined_values[random.randint(0, len(predefined_values) - 1)]
    else:
        params = {
            "m1": round(random.uniform(1, 10), 2),  # mass in kg
            "theta": round(random.uniform(15, 45), 2),  # angle in degrees
            "mu_s": round(random.uniform(0.1, 1.0), 2),  # static friction coefficient
            "mu_k": round(random.uniform(0.1, 1.0), 2),  # kinetic friction coefficient
            "m2_mass": round(random.uniform(1, 10), 2),  # mass of block m2 in kg
        }

    m1 = params["m1"]
    theta = math.radians(params["theta"])  # Convert angle to radians
    mu_k = params["mu_k"]
    m2 = params["m2_mass"]
    g = 9.81  # acceleration due to gravity in m/s²

    # 2. Calculate Forces
    F2 = m2 * g
    F1 = m1 * g * math.sin(theta)  # Down the incline
    F_friction = mu_k * m1 * g * math.cos(theta)  # Friction opposing the motion

    # 3. Determine Net Force and Acceleration
    if F2 > (F1 + F_friction):
        F_net = F2 - (F1 + F_friction)
        a = F_net / (m1 + m2)  # a = F_net / (m1 + m2)
    else:
        a = 0  # No acceleration if F2 is not greater than sum of forces

    # Return the structured data
    return {
        "params": {
            "m1": m1,
            "theta": params["theta"],
            "mu_s": params["mu_s"],
            "mu_k": params["mu_k"],
            "m2": params["m2_mass"],
            "m1_mass": m1,
        },
        "forces": {
            "F1": round(F1, 3),
            "F2": round(F2, 3),
            "F_friction": round(F_friction, 3),
            "F_net": round(F_net, 3) if F2 > (F1 + F_friction) else 0,
        },
        "correct_answers": {"acceleration": round(a, 3)},  # Round to 3 decimal places
        "nDigits": 3,
        "sigfigs": 3,
    }
