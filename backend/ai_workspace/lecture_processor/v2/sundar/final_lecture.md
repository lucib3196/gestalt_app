# Hydrostatics and Fluid Containers: Stability, Acceleration, and Rotational Effects

## Metadata
- **Course:** Transport Phenomena-135  
- **Instructor:** Sundararajan Venkatadriagaram  
- **Term:** Winter 2024  

*This lecture forms part of the foundational module on fluid statics and dynamics, aimed at equipping students with analytical tools to assess the behavior of fluids in containers under various force fields, a key competency in transport phenomena.*

---

## Table of Contents
1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
    - [Buoyancy and Stability: Floating Cylinders](#buoyancy-and-stability-floating-cylinders)
    - [Fluid Surface Behavior Under Acceleration](#fluid-surface-behavior-under-acceleration)
    - [Pressure Distribution in Accelerating and Rotating Fluids](#pressure-distribution-in-accelerating-and-rotating-fluids)
    - [Volumetric Flow Rate](#volumetric-flow-rate)
3. [Mathematical Derivations](#mathematical-derivations)
    - [Criterion for Fluid Spillage in a Rotating Cylinder](#criterion-for-fluid-spillage-in-a-rotating-cylinder)
4. [Conclusion](#conclusion)

---

## Introduction

Hydrostatics and fluid motion within containers are fundamental topics in engineering and physical sciences. This lecture explores the stability of floating bodies, specifically focusing on cylinders, and investigates the impact of linear and rotational acceleration on fluid containers. Understanding these effects is essential for the design and safety analysis of ships, tanks, and centrifuges. In addition, the session introduces the concept of volumetric flow rate, a foundational quantity in fluid dynamics.

Key terms defined in this article include:
- **Buoyancy:** The upward force exerted by a fluid on a submerged object.
- **Metacentric Height:** A measure of the initial static stability of a floating body.
- **Volumetric Flow Rate:** The volume of fluid passing through a surface per unit time.

---

## Core Concepts

### Buoyancy and Stability: Floating Cylinders

Floating bodies (such as cylinders) achieve equilibrium due to the balance between the gravitational force and the buoyant force. The vertical stability of such bodies is determined by the position of the center of gravity (G), the center of buoyancy (B), and the *metacenter* (M).

- **Metacentric Height (GM):**
    - Calculated as:
      $$ GM = \frac{I_c}{V} - BG $$
      where:
      - $I_c$ = Second moment of area of the waterplane $(I_c = \frac{\pi D^4}{64})$
      - $V$ = Submerged volume
      - $BG$ = Vertical distance between the center of buoyancy and the center of gravity

- **Stability Criterion for Cylinders:**
    - For a floating cylinder to be stable:
      $$ L < \frac{\sqrt{2}}{3} D $$
      where $L$ is the length (height) and $D$ is the diameter.

**Intuition:**
- A larger metacentric height suggests greater resistance to tipping.
- This analysis is crucial in naval architecture and the storage of fluids in vertical vessels.

---

### Fluid Surface Behavior Under Acceleration

When a fluid container is subjected to linear acceleration, the free surface of the fluid tilts.

- If a container moves horizontally with acceleration $a_x$ (and vertical acceleration $a_z = 0$), the inclination of the surface is given by:
  $$ \frac{dz}{dx} = -\frac{a_x}{g} $$
  This means the free surface tilts downward in the direction of acceleration.

**Rotational Acceleration:**
- For a container rotating about a vertical axis at angular velocity $\omega$, the free surface assumes a *paraboloidal* shape (a paraboloid of revolution), determined by:
  $$ z - z_0 = \frac{\omega^2 r^2}{2g} $$
  where $r$ is the radial distance from the axis, and $z_0$ is the surface elevation at the center ($r = 0$).

---

### Pressure Distribution in Accelerating and Rotating Fluids

The pressure in a fluid at rest or in situations of uniform acceleration or rotation is governed by:

- **General Hydrostatic Equation (with Accelerations):**
  $$ \nabla p = -\rho \vec{a} $$
  where $\vec{a}$ encompasses gravitational and imposed accelerations.

- In a rotating container, pressure increases outward from the rotational axis due to the centrifugal effect, and the associated free surface takes a parabolic shape.

---

### Volumetric Flow Rate

The volumetric flow rate ($Q$) is a fundamental measure in fluid mechanics, indicating how much fluid passes through a cross-section per unit time:
$$ Q = A v $$
- $A$ is the cross-sectional area
- $v$ is the average velocity of the fluid

This concept underlies the analysis of fluid conveyance in pipes and open channels.

---

## Mathematical Derivations

### Criterion for Fluid Spillage in a Rotating Cylinder

**Purpose:**
- To determine the critical angular velocity ($\omega$) at which a rotating cylindrical container will begin to spill its liquid due to the alteration in free surface profile.

#### Step-by-Step Derivation

1. **Free Surface Equation in a Rotating Cylinder:**
    $$ z - z_0 = \frac{\omega^2 r^2}{2g} $$
    - Paraboloidal profile formed by rotating fluids.

2. **Condition for Spillage:**
    - At the onset of spillage, the height of liquid at the wall ($r = R$) is just equal to the brim height, i.e.,
    $$ z_{\text{wall}} - z_0 = 2H_0 $$
    - Substituting into the profile equation:
    $$ \frac{\omega^2 R^2}{2g} = 2H_0 $$

3. **Solve for Angular Velocity ($\omega$):**
    $$ \omega^2 = \frac{4gH_0}{R^2} $$
    $$ \implies \boxed{\omega = \sqrt{\frac{4gH_0}{R^2}}} $$

4. **Criterion:**
    - If $\omega > \sqrt{\frac{4gH_0}{R^2}}$, liquid will spill from the rotating cylinder.

**Explanation:**
- The balance relates rotational "throw" at the edge to the original fluid height. Greater fluid depths or smaller radii require higher angular speeds before spillage occurs.

---

## Conclusion

This lecture addressed criteria for floating body stability, the characteristic behavior of fluid surfaces in accelerating and rotating containers, and pressure distribution analysis. The case of spillage in rotating cylinders illustrates the practical intersection of hydrostatics and rotational dynamics. Mastery of these concepts allows deeper exploration into advanced topics such as waves in rotating fluids, the design of storage tanks and ship stability, and is foundational for studies in transport phenomena.