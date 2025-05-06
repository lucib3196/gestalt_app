The 5\,\mathrm{kg} pendulum bob is released from rest when \(\theta = 0\). Determine the initial tension in the cord. Also, determine the tension at the instant \(\theta = 45^\circ\). Neglect the size of the bob and assume \(r = 2\,\mathrm{m}\).

Source: Image 1 (Page 3)

## Free Body Diagram and Initial Tension (\(\theta = 0\))

At \(\theta = 0\), the bob is at rest. Consider forces:
- Tension \(T\) upward along the cord
- Weight \(mg\) downward
\(\sum F_x = ma_x\) (where \(x\) is radial direction)
At the start, acceleration is zero since the bob is not moving:
$$T - mg = 0 \implies T = mg$$
Thus, the initial tension is the weight of the bob.

## Tension at \(\theta = 45^\circ\) (General Solution)

At \(\theta = 45^\circ\), the forces on the bob are:
- Tension \(T\)
- Weight \(mg\)
- The acceleration includes centripetal acceleration due to velocity:
\(T - mg\sin\theta = m\frac{v^2}{r}\)
Thus,
$$T = mg\sin\theta + m\frac{v^2}{r}$$

## Velocity at \(\theta = 45^\circ\) (General Expression)

The tangential acceleration \(a_t = g \cos \theta\). To find \(v\) at \(\theta = 45^\circ\), use energy or integrate:
\(a_t = g\cos\theta\)
For differential arc:
$$a\,ds = v\,dv \to r g\cos\theta\,d\theta = v\,dv$$
Integrate both sides from \(\theta = 0\) to \(\theta = \pi/4\) and \(v = 0\) to \(v = v\):
$$\int_0^{\pi/4} r g \cos\theta\, d\theta = \int_0^v v\,dv$$
$$rg\sin\theta \bigg|_0^{\pi/4} = \frac{v^2}{2} \bigg|_0^v$$
This gives a general symbolic solution for \(v\) as a function of \(r, g, \theta\).

Describe the process for determining the general tension in the cord of a pendulum at an arbitrary angle \(\theta\), assuming the bob is released from rest at \(\theta=0\) and swings to angle \(\theta\), neglecting air resistance and assuming massless cord.

Source: Images 2-3 (Pages 4-5)

## Free Body Diagram at Angle \(\theta\)

Draw FBD:
- Tension \(T\) acts along the cord toward the pivot
- Weight \(mg\) acts vertically downward

Radial (normal) equation:
\(\sum F_n = ma_n\)
\(T - mg\sin\theta = m \frac{v^2}{r}\)
Tangential equation:
\(mg\cos\theta = m a_t \implies a_t = g\cos\theta\)

## Velocity Calculation via Integration

Integrate tangential acceleration:
- Relate arc length \(ds\) and angle: \(ds = r\,d\theta\)
- Use work-energy principle or integrate:
\(a_t ds = v\,dv\)
\(r g \cos\theta\, d\theta = v\,dv\)
Integrate from \(\theta=0, v=0\) to \(\theta, v\):
$$\int_0^{\theta} r g \cos \theta' d\theta' = \int_0^{v} v dv$$
$$rg\sin\theta = \frac{v^2}{2}$$
Solve for \(v\):
$$v = \sqrt{2r g \sin\theta}$$

## General Expression for Tension

Substitute \(v\) into tension equation:

$$T = mg\sin\theta + m\frac{v^2}{r}$$
Using \(v^2 = 2rg\sin\theta\):
$$T = mg\sin\theta + m\frac{2rg\sin\theta}{r}$$
$$T = mg\sin\theta + 2mg\sin\theta$$
$$T = 3mg\sin\theta$$

The smooth block $b$ having a mass $m$ is attached to the vertex $A$ of the right circular cone using a light cord. The cone is rotating at constant angular speed about the $z$-axis such that the block attains a speed $v$. At this speed, determine symbolically (in terms of $m, g, v, r, \theta$): (a) the tension $T$ in the cord, and (b) the normal reaction $N$ that the cone exerts on the block. Neglect the size of the block.

Source: Image 1 (top left), original problem statement

## Free-Body Diagram (FBD) and Forces

Draw a free-body diagram of the block, identifying the following forces: tension $T$ in the cord (along the cord at angle $\theta$), normal force $N$ from the cone (perpendicular to the cone surface at angle $\theta$), and gravitational force $mg$ (downwards). The block is rotating horizontally with speed $v$ about the $z$-axis, at radius $r$ from the axis.

## Force Equilibrium in the Vertical Direction ($y'$)

Sum forces along the vertical ($y'$) direction:

$$\sum F_{y'} = 0 \implies -mg + N \cos \theta + T \sin \theta = 0$$

## Centripetal Force in the Horizontal Direction ($x'$)

Sum forces along horizontal ($x'$) (radial) direction, provide the required centripetal force:

$$\sum F_{x'} = m\frac{v^2}{r} \implies T \cos \theta - N \sin \theta = m \frac{v^2}{r}$$

## Solving the Two Equations Symbolically

Solve for $T$ and $N$ using the two simultaneous equations:

1. $-mg + N \cos \theta + T \sin \theta = 0$
2. $T \cos \theta - N \sin \theta = m \frac{v^2}{r}$

Isolate $T$ and $N$ in terms of $m, g, v, r, \theta$:

- From (2): $T = \frac{m \frac{v^2}{r} + N \sin \theta}{\cos \theta}$
- Substitute into (1) and solve for $N$, then back-solve for $T$.

The 0.5-lb ball is guided along the vertical circular path $r = 2 r_c \cos \theta$ using the arm $OA$. If the arm has an angular velocity $\dot{\theta}$ and an angular acceleration $\ddot{\theta}$ at the instant $\theta$, determine the force of the arm on the ball. Neglect friction and the size of the ball. Set $r_c=0.4\ \text{ft}$.

Given at the instant $\theta=30^\circ$:
- $\dot{\theta} = 0.4\ \text{rad/s}$
- $\ddot{\theta} = 0.8\ \text{rad/s}^2$

Determine the force of the arm on the ball at this instant.

Source: Page 9 (first image)

## Restating the Problem Symbolically

We are given:
\begin{itemize}
    \item The ball mass (express in general as $m$ instead of the given value).
    \item The path: $r = 2r_c \cos\theta$
    \item Arm's angular velocity: $\dot{\theta}$
    \item Arm's angular acceleration: $\ddot{\theta}$
    \item At an instant $\theta$
    \item Find: The force of the arm on the ball, i.e., all components of the force acting on the ball at that instant.
\end{itemize}

## Kinematics in Polar Coordinates

Given $r = 2 r_c \cos \theta$

Compute the first and second time derivatives symbolically:
\[
\dot{r} = \frac{d}{dt}(2 r_c \cos \theta) = 2 r_c ( -\sin \theta ) \dot{\theta}
\]
\[
\ddot{r} = \frac{d}{dt}(\dot{r}) = 2 r_c ( -\cos \theta ) \dot{\theta}^2 + 2 r_c ( -\sin \theta ) \ddot{\theta}
\]

## Equations of Motion and Force Components

The polar force balance in the $r$ and $\theta$ directions:
\[
\sum F_r = m a_r, \quad\quad \sum F_{\theta} = m a_{\theta}
\]
Where:
\[
 a_r = \ddot{r} - r \dot{\theta}^2 \\
 a_{\theta} = r\ddot{\theta} + 2\dot{r} \dot{\theta}
\]

The free-body diagram (from the annotated sketch):
\[
\sum F_r = N \cos \theta - W \sin \theta = m a_r
\]
\[
\sum F_{\theta} = F_{OA} + N \sin \theta - W \cos \theta = m a_{\theta}
\]

### $N$ and $F_{OA}$

Solve the two equations symbolically for $N$ and $F_{OA}$:

\[
N \cos \theta - W \sin \theta = m (\ddot{r} - r\dot{\theta}^2)
\]
\[
F_{OA} + N\sin \theta - W \cos \theta = m(r\ddot{\theta} + 2\dot{r}\dot{\theta})
\]
Where $W = mg$

## Summary of Necessary Expressions

For a fully symbolic solution, the force of the arm on the ball, $F_{OA}$, is found by first solving for $N$ using the equations above, where:
\begin{align*}
 r &= 2 r_c \cos \theta \\
 \dot{r} &= 2 r_c ( -\sin \theta ) \dot{\theta} \\
 \ddot{r} &= 2 r_c ( -\cos \theta ) \dot{\theta}^2 + 2 r_c ( -\sin \theta ) \ddot{\theta}
\end{align*}
Insert these expressions into the equations for $a_r$ and $a_{\theta}$, then into the force equations for $\sum F_r$ and $\sum F_{\theta}$.
Do not substitute any specific values for $\theta$, $\dot{\theta}$, $\ddot{\theta}$, $m$, or $r_c$ unless explicitly requested.

What are the symbolic expressions for $\dot{r}$ and $\ddot{r}$ given $r = 2 r_c \cos \theta$ and $\theta = \theta(t)$?

Source: Page 9 (first image, annotated calculations)

## Time Derivatives of $r$

Given $r = 2 r_c \cos \theta$, with $\theta$ a function of time $t$, apply the chain rule:
\[
\dot{r} = \frac{d}{dt}(2 r_c \cos \theta) = 2 r_c ( -\sin \theta ) \dot{\theta}
\]
\[
\ddot{r} = \frac{d}{dt}(\dot{r}) = 2 r_c ( -\cos \theta ) \dot{\theta}^2 + 2 r_c ( -\sin \theta ) \ddot{\theta}
\]

Write the symbolic expressions for the radial and transverse acceleration components, $a_r$ and $a_{\theta}$, for a particle moving in polar coordinates with position vector $r = r(\theta(t))$.

Source: Page 11 (third image, equations for $ma_r$ and $ma_{\theta}$)

## Acceleration in Polar Coordinates

General expressions for the radial and transverse (angular) acceleration components:
\[
a_r = \ddot{r} - r \dot{\theta}^2 \qquad a_{\theta} = r \ddot{\theta} + 2 \dot{r} \dot{\theta} \n\]
With $r(t)$ and $\theta(t)$ general.

Symbolically, write the system of equations for equilibrium in the $r$ and $\theta$ directions for the free-body diagram of the ball on the path, neglecting friction and ball size.

Source: Page 12 (fourth image, bottom red equations)

## System of Equations (No numerical substitutions)

The force equilibrium equations in the $r$ and $\theta$ directions:
\begin{align*}
N \cos \theta - W \sin \theta &= m (\ddot{r} - r\dot{\theta}^2) \\
f_{OA} + N \sin \theta - W \cos \theta &= m (r\ddot{\theta} + 2 \dot{r} \dot{\theta})
\end{align*}
Where $W = mg$, and all derivatives are in terms of $\theta$ and $r_c$ as previously derived.