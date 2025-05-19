The 5\,\mathrm{kg} pendulum bob is released from rest when \( \theta = 0 \). Determine the initial tension in the cord. Also determine the tension at the instant \( \theta = 45^\circ \). Neglect the size of the bob and assume \( r = 2\,\mathrm{m} \).

Source: Slide 4

## Step 1: Analyze Initial Condition (\(\theta = 0\))

At \(\theta = 0\), the bob is released from rest. The acceleration is zero. The free-body diagram would have the tension \(T\) upwards along the string and weight \(mg\) downwards. Thus, \[ \sum F_x = m a_x \rightarrow T - mg = 0 \rightarrow T = mg \]

## Step 2: Analyze Condition at \(\theta = 45^\circ\)

At \(\theta = 45^\circ\), the forces on the bob have radial (normal) and tangential components. The equation in the radial direction is: \[ \sum F_n = m a_n \implies T - mg \sin\theta = m\frac{v^2}{r} \]

## Step 3: Find Velocity at \(\theta = 45^\circ\)

Use tangential acceleration to determine the velocity: \( a_t = g \cos\theta \). Integrate: \[ \int_0^{\pi/4} g \cos\theta \; r\,d\theta = \int_0^{V} v \, dv \] This gives a symbolic solution for \(V\).

## Step 4: Express the Final Tension Symbolically

Express tension as \[ T = mg\sin\theta + m\frac{v^2}{r} \] at \( \theta = 45^\circ \). Substitute the (symbolic) result for \( v \) from the previous step.

At the instant \( \theta = 45^\circ \), what is the velocity \( V \) of the pendulum bob? Express in terms of \(m\), \(g\), \(r\), and \(\theta\).

Source: Slide 6

## Step 1: Write the Differential Equation for \(a_t\)

Tangential acceleration: \( a_t = g \cos\theta \). For circular motion: \( ds = r d\theta \), use \( a_t ds = v dv \).

## Step 2: Integrate to Solve for \(v\)

\[ \int_0^{\pi/4} g \cos\theta \cdot r\,d\theta = \int_0^{V} v \, dv \]
\[ rg \int_0^{\pi/4} \cos\theta \, d\theta = \frac{1}{2} V^2 \]
Symbolically evaluate the left integral and solve for \(V\).

The smooth block \(b\) having a mass of \(m\) is attached to the vertex \(A\) of the right circular cone using a light cord. The cone is rotating at constant angular speed about the z-axis such that the block attains a speed of \(v\). At this speed, determine the tension in the cord and the reaction the cone exerts on the block. Neglect the size of the block.

Source: Slide 8

## Step 1: Identify All Forces and Set Up Equilibrium Equations

Draw the Free Body Diagram with forces: tension \(T\), normal \(N\), and weight \(mg\).
Write equilibrium equations:
\[ \sum F_y = 0: -mg + N\cos\theta + T\sin\theta = 0 \]
\[ \sum F_x = m\frac{v^2}{r}: T\cos\theta - N\sin\theta = m\frac{v^2}{r} \]
Express \(r\) in terms of cone geometry.

## Step 2: Solve for Tension and Normal Force Symbolically

Solve the above linear system for \(T\) and \(N\) in terms of \(m\), \(g\), \(\theta\), \(r\), and \(v\).

A 0.5-lb ball is guided along the vertical circular path \( r = 2r_c \cos \theta \) using the arm \( OA \). If the arm has an angular velocity \( \dot{\theta} \) and an angular acceleration \( \ddot{\theta} \) at the instant \( \theta = 30^\circ \), determine the force of the arm on the ball. Neglect friction and the size of the ball. Set \( r_c \) as a constant.

Source: Slide 11

## Step 1: Write the Position Vector and Take Derivatives

Position: \( r = 2r_c \cos\theta \)
Velocity: \[ \dot{r} = -2r_c \sin\theta \dot{\theta} \]
Acceleration (radial and transverse components):
\[ \ddot{r} = -2r_c \cos\theta \dot{\theta}^2 - 2r_c \sin\theta \ddot{\theta} \]

## Step 2: Write Force Equations in Polar Coordinates

Radial: \( \sum F_r = m a_r \ ), \( a_r = \ddot{r} - r \dot{\theta}^2 \)
Transverse: \( \sum F_\theta = m a_\theta \), \( a_\theta = r\ddot{\theta} + 2\dot{r}\dot{\theta} \)
Express force components symbolically.

## Step 3: Express Contact Force (Force of Arm on Ball) Symbolically

The force of the arm on the ball is the sum of radial and transverse components computed above, written in polar vectors.

For a general function \( r = f(\theta) \), what is the slope \( \psi \) of the tangent to the path at any point?

Source: Slide 15

## Calculation of the Slope of the Tangent

The slope \( \psi \) of the tangent to the curve described by \( r = f(\theta) \) is given by:
\[ \tan\psi = \frac{r}{\frac{dr}{d\theta}} \]

For a rigid body, what are the equations of motion relating the sum of the forces and the sum of the moments to the acceleration of the center of mass and the angular acceleration (about the center of mass)?

Source: Slides 16-18

## Equations of Motion for a Rigid Body

\[ \sum \vec{F} = m \vec{a}_G \]
\[ \sum M_G = I_G \alpha \]
where \( m \) is mass, \( I_G \) is the moment of inertia about the center of mass, \( \vec{a}_G \) is the acceleration of the center of mass, and \( \alpha \) is the angular acceleration.

Where do we get the equations of motion for a rigid body from?

Source: Slide 19

None

What is the parallel axis theorem for the moment of inertia?

Source: Slide 22

## Statement of the Parallel Axis Theorem

\[ I_P = I_G + m d^2 \]
where \(I_P\) is the moment of inertia about a point \(P\), \(I_G\) is the moment of inertia about the center of mass, \(m\) is the total mass, and \(d\) is the distance between the center of mass and point \(P\).

For planar motion of a rigid body, write the equations of motion relating forces and moments to linear and angular acceleration.

Source: Slides 23-25

## Equations of Planar Motion for a Rigid Body

\[
\sum F_x = m (a_G)_x \\
\sum F_y = m (a_G)_y \\
\sum M_G = I_G \alpha
\]