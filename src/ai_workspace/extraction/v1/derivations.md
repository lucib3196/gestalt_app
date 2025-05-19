# Pendulum Bob Tension Analysis
 
Source: Slides 4--7 (Pendulum problem) 

## Extracted Questions

1. The 5 kg pendulum bob is released from rest when \( \theta = 0 \). 
   (a) Determine the initial tension in the cord. 
   (b) Also determine the tension at the instant \( \theta = 45^{\circ} \). 
   Neglect the size of the bob and assume \( r = 2\text{ m} \).

## Solution Steps (as present in images)

(a) For \( \theta = 0 \):
\[ \sum F_x = m a_x \implies T = 0 \]

(b) For \( \theta = 45^{\circ} \):
\[ \sum F_n = m a_n \]
\[ T - mg \sin\theta = \frac{m v^2}{r} \]
\[ T = mg\sin\theta + \frac{mv^2}{r} \]

To find \( v \) for \( \theta = 45^{\circ} \):
- Use \( a_t = g \cos\theta \), integrate tangential acceleration:
\[ a_t ds = v dv \implies \int_0^{\pi/4} (g \cos\theta) r d\theta = \int_0^{v} v dv \]
- For \( r = 2 \), this gives (up to symbolic relational expression):
\[ r g \sin\theta |_{0}^{\pi/4} = \frac{v^2}{2} |_{0}^{v} \]
- Thus:
\[ T = mg\sin\theta + \frac{mv^2}{r} \] for \( \theta = 45^{\circ} \).

**Note:** Numerical substitution is visible in images, but omitted here per instructions.

## Image and Diagram Analysis

Yes, images are necessary to comprehend the: (1) pendulum geometry and (2) force diagrams (free-body and kinetic diagram) for proper breakdown of forces and accelerations as \( \theta \) changes. 

These images clarify how to resolve forces (tension, gravity), how the acceleration projects along normal/tangential axes, and the path of the pendulum bob.

## External Data Considerations

No external data is required; all parameters and relationships are given symbolically or described in the images. However, if the mass was not specified, a variable \( m \) could be used.

# Cone and Rotating Cord Tension Analysis
 
Source: Slides 8--9 (Cone/block problem) 

## Extracted Questions

The smooth block b having mass \( m = 0.2 \) kg is attached to the vertex A of the right circular cone using a light cord. The cone is rotating at constant angular speed about the z-axis such that the block attains a speed of \( v = 0.5 \) m/s. At this speed:
(a) Determine the tension in the cord. 
(b) Determine the reaction the cone exerts on the block.
Neglect the size of the block.

## Solution Steps (from images)

Let \( \theta \) denote the cone's apex angle. 
- Set up force balances in y-direction and x-direction:
\[ -mg + N \cos\theta + T \sin\theta = 0 \]
\[ T \cos\theta - N \sin\theta = \frac{mv^2}{r} \]
- Geometry of the cone:
\[ r = 200 \frac{3}{5} \] (using similar triangles; parameterize as \( r = h \frac{\text{base}}{\text{hypotenuse}} \) if needed for symbolic answer)
- Solve for \( T \) and \( N \) (symbolically):
\[ T = ... \text{(in terms of } m, v, r, \theta, g \text{)} \]
\[ N = ... \text{(in terms of } m, v, r, \theta, g \text{)} \]
Certain numerical values have been filled in but should be replaced by variables.

## Image and Diagram Analysis

The problem depends critically on the cone diagram to define geometry, the force diagram (showing \( T, N, mg \)), and the velocity/axes relationship. These images are needed to:
- Express \( r \) in terms of \( \theta \) and known dimensions,
- Resolve forces in the proper directions relative to \( \theta \).
Sketches should include:
- The cone with labeled height, base, radius, and apex angle
- The block position, velocity vector, and all forces.

## External Data Considerations

No external data is required. If cone dimensions were not given, a general relation for \( r \) in terms of \( \theta \) and the cone's height and base would be required.

# Force on a Ball Guided Along a Path (Cylindrical Coordinates)
 
Source: Slides 10--12 (Cylindrical coordinates ball/arm) 

## Extracted Questions

The 0.5-lb ball is guided along the vertical circular path \( r = 2r_c \cos\theta \) using the arm OA. If the arm has an angular velocity \( \dot{\theta} = 0.4 \) rad/s and an angular acceleration \( \ddot{\theta} = 0.8 \) rad/s² at the instant \( \theta = 30^{\circ} \):
Determine the force of the arm on the ball. Neglect friction and the size of the ball. Set \( r_c = 0.4 \) ft.

## Solution Steps (from images)

In cylindrical coordinates:
- \( r = 2r_c\cos\theta \)
- \( \dot{r} = 2r_c(-\sin\theta)\dot{\theta} \)
- \( \ddot{r} = 2r_c(-\cos\theta)\dot{\theta}^2 + 2r_c(-\sin\theta)\ddot{\theta} \)

Force equations (slide 13):
\[ \sum F_r = m a_r \]
\[ \sum F_\theta = m a_\theta \]
Where:
\[ a_r = \ddot{r} - r \dot{\theta}^2 \]
\[ a_{\theta} = r \ddot{\theta} + 2\dot{r}\dot{\theta} \]

Resolve forces on FBD:
\[ \sum F_r = N \cos\theta - W \sin\theta = m a_r \]
\[ \sum F_\theta = F_{OA} + N \sin\theta - W \cos\theta = m a_{\theta} \]
Solving for \( F_{OA} \) yields the force of the arm on the ball.

Numerical substitutions from image are omitted; keep all variables symbolic.

## Image and Diagram Analysis

Use is made of (1) the physical diagram showing the guided arm OA and the circular path, and (2) the force/acceleration diagrams showing the r/\( \theta \) coordinate system and force resolution. These are essential for:
- Defining \( r, \theta \), and all acceleration components,
- Visualizing all forces and directions for correct setup.

Diagrams should include:
- Circular path with \( r(\theta) \), O/A locations,
- Ball with \( F_{OA} \), Normal, and Weight vector decompositions,
- Unit vectors \( u_r, u_{\theta} \) at \( \theta \).

## External Data Considerations

The calculation employs only the symbols defined in the problem (\( r_c, \theta, m, W, F_{OA}, N, \dot{\theta}, \ddot{\theta} \)). No external tables or datasets are required.

# Where do we get these Equations?
 
Source: Slide 15 

## Extracted Questions

Where do we get these equations? (refers to equations of motion for rigid bodies)
No explicit mathematical or physics problem is presented; this is a conceptual prompt.

## Solution Steps

No solution provided.