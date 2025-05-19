# Kinetics of Particles & Rigid Bodies: Equations of Motion, Tensions, and Dynamics

## Metadata
- **Course Title**: Dynamics-103
- **Instructor**: Thomas Stahovich
- **Term**: Spring 2025
- **Institution**: [Institution not specified]

_This lecture is part of the foundational module on particle and rigid body dynamics. It emphasizes Newton’s second law, equations of motion, and free-body diagrams for modeling mechanical systems, forming a basis for advanced studies in analytical dynamics and mechanical engineering._

---

## Table of Contents
1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
    1. [Newton’s Second Law](#newtons-second-law)
    2. [Equations of Motion for Rigid Bodies](#equations-of-motion-for-rigid-bodies)
    3. [Moment of Inertia and Parallel Axis Theorem](#moment-of-inertia-and-parallel-axis-theorem)
    4. [Tangential and Normal Directions](#tangential-and-normal-directions)
    5. [Free-Body and Kinetic Diagrams](#free-body-and-kinetic-diagrams)
3. [Mathematical Derivations](#mathematical-derivations)
    1. [Moment Equations for a Rigid Body](#moment-equations-for-a-rigid-body)
4. [Example Problems & Solutions](#example-problems--solutions)
    1. [Pendulum Tension Analysis](#pendulum-tension-analysis)
    2. [Tension and Normal Force on a Block in a Rotating Cone](#tension-and-normal-force-on-a-block-in-a-rotating-cone)
    3. [Forces on a Ball on a Guided Arm](#forces-on-a-ball-on-a-guided-arm)
    4. [Symbolic Derivatives in Polar Coordinates](#symbolic-derivatives-in-polar-coordinates)
    5. [Polar Acceleration Components](#polar-acceleration-components)
    6. [Equilibrium in Polar Components](#equilibrium-in-polar-components)
5. [Conclusion](#conclusion)

---

## Introduction

Kinetics, a branch of classical mechanics, studies the relationship between forces acting on a system and the resulting motion. In engineering and physics, understanding the equations of motion for both particles and rigid bodies is crucial. This lecture explores Newton’s second law, applies it to both particles and rigid bodies, and demonstrates systematic approaches using free-body diagrams and mathematical modeling. Special focus is given to the analysis of forces (tensions, normal reactions) in mechanical systems including pendulums, rotating conical surfaces, and guided tracks, alongside the computation and application of moment of inertia using the parallel axis theorem. Mastery of these topics underpins advanced modules in mechanical system dynamics and design.

---

## Core Concepts

### Newton’s Second Law

Newton’s second law is fundamental to all of dynamics, relating force, mass, and acceleration. For a particle,

$$
\vec{F} = m\vec{a}
$$

where $\vec{F}$ is the net external force, $m$ is the mass, and $\vec{a}$ is the acceleration. In analyzing rigid bodies, the principle extends to include rotational effects:

- **Translational motion of the mass center $G$:**
  $$
  \sum \vec{F} = m \vec{a}_G
  $$

- **Rotational motion about $G$:**
  $$
  \sum \vec{M}_G = I_G \alpha
  $$

where $I_G$ is the moment of inertia about the center of mass and $\alpha$ the angular acceleration.

### Equations of Motion for Rigid Bodies

Rigid body planar motion can be categorized as:
- **Translation:** No rotation; all points move with the same velocity and acceleration.
- **Rotation about a fixed axis:** Every point moves in a circle about the axis.
- **General planar motion:** A combination of translation and rotation.

Key equations:
- For translation:
  $$\sum \vec{F} = m \vec{a}_G$$
- For rotation about mass center $G$:
  $$\sum \vec{M}_G = I_G \alpha$$

### Moment of Inertia and Parallel Axis Theorem

The **moment of inertia** quantifies the distribution of mass in a body with respect to a chosen axis. It is defined as
$$
I_P = \int r^2 dm
$$
where $r$ is the perpendicular distance from the axis $P$ to the mass element $dm$.

When the axis is not through the center of mass, use the **parallel axis theorem**:
$$
I_P = I_G + m d^2
$$
where $d$ is the distance from $G$ to $P$.

### Tangential and Normal Directions

Motion along a curved path is analyzed by decomposing acceleration into tangential and normal (radial) components:

- **Tangential acceleration:** $a_t = g\cos\theta$ (e.g., for a pendulum)
- **Normal (radial) acceleration:** $a_n = \frac{v^2}{r}$

For angle $\psi$ between the radius and the tangent:
$$
\tan\psi = \frac{r}{\frac{dr}{d\theta}}
$$

### Free-Body and Kinetic Diagrams

**Free-body diagrams (FBDs)** illustrate all external forces on a body. **Kinetic diagrams** complement these, showing inertial (ma) terms. These tools allow systematic setup of equations of motion for unknown forces, tensions, and accelerations in dynamic problems.

---

## Mathematical Derivations

### Moment Equations for a Rigid Body

**Purpose:** To extend Newton’s second law to include not only translation ($\vec{F} = m\vec{a}$) but also rotation for rigid bodies, leading to $\sum \vec{M}_G = I_G \alpha$.

The derivation employs vector calculus and reference point selection:
- Summing moments about a point $G$ (usually center of mass)
- Using kinematic relations for planar or three-dimensional motion

*Note: The supplied slides do not present explicit questions, but the diagrams clarify the definitions and role of terms such as the moment arm, angular acceleration, and mass center. These form the foundation for all subsequent analysis of rigid body kinetics.*

---

## Example Problems & Solutions

### 1. Pendulum Tension Analysis

> **Problem:**
> The 5 kg pendulum bob is released from rest at $\theta = 0$. Determine the initial tension in the cord, and the tension at $\theta = 45^\circ$. Cord length $r = 2$ m; neglect the size of the bob.

**Solution:**

**At $\theta = 0$ (rest, start position):**
- The only forces on the bob are tension ($T$) upward along the cord and weight ($mg$) downward.
- Since there is no motion yet, net force is zero ($T - mg = 0$), so
  $$T = mg = 5 \times 9.81 = 49.05\ \text{N}$$
- *Key concept*: At rest, the cord simply supports the full weight.

**At $\theta = 45^\circ$ (in motion):**
- The bob has picked up speed, so the tension must also supply centripetal force in addition to balancing a component of the weight.
- Radial (normal) equation of motion:
  $$T - mg \sin \theta = m \frac{v^2}{r}$$
  $$T = mg \sin \theta + m \frac{v^2}{r}$$

- To find $v$ as a function of $\theta$ (since initial velocity is zero):

  - Tangential acceleration: $a_t = g \cos \theta$
  - Use $a_t ds = v dv$ (work-energy principle)
  - Since $ds = r d\theta$, $a_t ds = r g \cos \theta d\theta = v dv$.
  - Integrating:
    $$
    \int_0^{\theta} r g \cos \theta' d\theta' = \int_0^{v} v dv
    $$
    $$
    rg \sin \theta = \frac{v^2}{2}
    $$
    $$v = \sqrt{2r g \sin \theta}$$

- Substitute back:

  $$T = mg \sin \theta + m \frac{2r g \sin \theta}{r} = mg \sin \theta + 2mg \sin \theta = 3 m g \sin \theta$$

  For $\theta = 45^\circ$,
  $$T = 3 \times 5 \times 9.81 \times \sin 45^\circ = 3 \times 5 \times 9.81 \times \frac{1}{\sqrt{2}} \approx 104\ \text{N}$$

- *Educational Note*: This problem illustrates the use of dynamic force analysis and the energy principle to find velocity at any angle.

---

### 2. Tension and Normal Force on a Block in a Rotating Cone

> **Problem:**
> A smooth block ($m$) attached by a cord to vertex $A$ of a right circular cone rotates at constant speed $v$ at radius $r$ from the axis ($z$), with cone half-angle $\theta$. Determine (a) the tension $T$ in the cord, and (b) the normal force $N$ from the cone.

**Solution:**
- Draw FBD: Tension $T$ (along cord at angle $\theta$), Normal force $N$ (normal to cone), Weight $mg$ (downward).

**Force equilibrium, vertical ($y’$):**
$$ -mg + N \cos \theta + T \sin \theta = 0 $$

**Centripetal force, horizontal ($x’$):**
$$ T \cos \theta - N \sin \theta = m \frac{v^2}{r} $$

**Solving for $T$ and $N$:**

1. $T = \frac{m \frac{v^2}{r} + N \sin \theta}{\cos \theta}$
2. Substitute into the vertical equilibrium and solve for $N$:
   - Plug values from (1) into the vertical equation.
   - Solve the resulting equation for $N$, then substitute back to get $T$.

- *Educational Note*: This symbolic solution requires simultaneous equations, highlights the interplay between vertical and horizontal force balances, and is common in rotating systems.

---

### 3. Forces on a Ball on a Guided Arm (Polar Coordinates)

> **Problem:**
> 0.5-lb ball follows $r = 2 r_c \cos\theta$ on arm $OA$. At $\theta$, arm angular velocity $\dot{\theta}$, acceleration $\ddot{\theta}$; find the force of the arm on ball symbolically.

**Solution:**

Given:
$$
\begin{align*}
r &= 2 r_c \cos \theta \\
\dot{r} &= -2 r_c \sin \theta \dot{\theta} \\
\ddot{r} &= -2 r_c \cos \theta \dot{\theta}^2 - 2 r_c \sin \theta \ddot{\theta}
\end{align*}
$$

**Acceleration Components (Polar):**
- Radial: $a_r = \ddot{r} - r \dot{\theta}^2$
- Transverse: $a_{\theta} = r \ddot{\theta} + 2 \dot{r} \dot{\theta}$

**Force Equilibrium:**
- $N \cos \theta - W \sin \theta = m a_r$
- $F_{OA} + N \sin \theta - W \cos \theta = m a_{\theta}$

Solve these simultaneously for $F_{OA}$ and $N$. All expressions remain symbolic for generality.

- *Educational Note*: This problem demonstrates the systematic procedure for expressing dynamics in non-Cartesian coordinates and builds proficiency in handling variable-radius motion.

---

### 4. Symbolic Derivatives in Polar Coordinates

> **Problem:**
> For $r = 2 r_c \cos \theta$, with $\theta = \theta(t)$, express $\dot{r}$ and $\ddot{r}$.

**Solution:**
$$
\dot{r} = -2 r_c \sin \theta \dot{\theta}
$$
$$
\ddot{r} = -2 r_c \cos \theta \dot{\theta}^2 - 2 r_c \sin \theta \ddot{\theta}
$$

- *Educational Note*: This reinforces applications of the [chain rule](#core-concepts) in implicit variable scenarios, fundamental to advanced coordinate transformations.

---

### 5. Polar Acceleration Components

> **Problem:**
> Write symbolic expressions for $a_r$ and $a_{\theta}$ for any $r = r(\theta(t))$.

**Solution:**
$$
\begin{align*}
a_r &= \ddot{r} - r \dot{\theta}^2 \\
 a_{\theta} &= r \ddot{\theta} + 2 \dot{r} \dot{\theta}
\end{align*}
$$

- *Educational Note*: Familiarity with these forms is essential for analyzing rotational and oscillatory systems, as encountered in advanced mechanics.

---

### 6. Equilibrium in Polar Components

> **Problem:**
> Write the symbolic system of equations for a particle in equilibrium under $N$, $f_{OA}$, and $W$ in polar coordinates.

**Solution:**
$$
\begin{align*}
 N \cos \theta - W \sin \theta &= m (\ddot{r} - r\dot{\theta}^2) \\
 f_{OA} + N \sin \theta - W \cos \theta &= m (r\ddot{\theta} + 2\dot{r}\dot{\theta})
\end{align*}
$$

- *Educational Note*: Articulating multi-component force balances in symbolic form aids in generalizing solutions for a wide range of kinematics problems.

---

## Conclusion

This lecture introduced the core principles and mathematical models of particle and rigid body kinetics. Students should now be able to:
- Apply Newton’s second law to both particles and rigid bodies
- Systematically construct and interpret free-body and kinetic diagrams
- Solve dynamic problems involving force, tension, and acceleration in linear and rotational contexts
- Compute moment of inertia and use the parallel axis theorem
- Express accelerations and forces in generalized coordinates (e.g., polar form)

**Further Reading:**
- Analytical Dynamics (Greenwood)
- Engineering Mechanics: Dynamics (Meriam & Kraige)

These techniques are foundational for advanced study in vibration analysis, multibody dynamics, and machine design.