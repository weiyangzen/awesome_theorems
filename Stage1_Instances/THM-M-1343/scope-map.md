# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1343`, the title "Lyapunov's direct method", the gloss "a
stability criterion using a Lyapunov function", attribution to Aleksandr Lyapunov, and the year
1892. Intake preserves the ordinary-differential-equation direct-method family. It does not turn
the attribution into a primary-source citation or the untrusted status into source or kernel
evidence.

## Proposition-changing decisions

An approved source selection must freeze:

- an autonomous equation `x' = f(x)`, a time-dependent equation `x' = f(t,x)`, a discrete-time
  system, a flow, or another dynamical model;
- the time domain, state and scalar spaces, dimensions or universes, topology or norm, system
  domain, and the exact classical, Caratheodory, integral-curve, or flow solution notion;
- an equilibrium point, invariant set, trajectory, or another stability object, together with its
  invariance or equilibrium hypotheses;
- local existence and uniqueness versus global forward existence, and how solutions that approach
  the boundary or escape in finite time are treated;
- the regularity of the vector field and Lyapunov function and whether the orbital derivative is a
  classical derivative, Frechet derivative paired with the field, Dini derivative, or another
  source-defined notion;
- positive definiteness, semidefiniteness, strict local minimum, comparison-function bounds,
  coercivity, properness, or radial unboundedness of the Lyapunov function;
- nonpositive, negative definite, strict-away-from-equilibrium, or another decay condition, and
  whether equality cases invoke an invariance principle;
- Lyapunov, uniform, asymptotic, exponential, local, semiglobal, or global stability and any basin,
  rate, or convergence conclusion; and
- all ordered binders, quantifier dependencies, neighborhoods, sublevel sets, constants, endpoint
  conventions, and degenerate cases.

These choices yield materially different propositions. They are a resolution ledger, not a
canonical statement.

## Candidate families not credited

1. Positive definiteness of `V` and nonincrease of `V` along every nearby solution imply local
   Lyapunov stability of an equilibrium.
2. Positive definiteness plus a source-specified strict decay condition imply local asymptotic
   stability.
3. A proper or radially unbounded Lyapunov function with strict decay, together with global forward
   existence, implies a global conclusion.
4. Nonautonomous uniform-stability, invariant-set, discrete-time, nonsmooth, and LaSalle
   invariance-principle variants.

No family in this list is selected, asserted, or credited at intake.

## Explicit exclusions

- Upgrading an unspecified stability criterion to asymptotic, exponential, or global stability.
- Treating weak nonincrease of `V` as strict decay or as convergence without additional premises.
- Assuming global forward existence, compact sublevel sets, coercivity, or radial unboundedness.
- Replacing the direct method with linearization or the indirect method from `THM-M-1344`.
- Absorbing the general stability-theory topic `THM-M-1342` or the related physics record
  `THM-P-0796` into this target.
- Replacing the target by LaSalle's invariance principle, Chetaev instability, converse Lyapunov
  theorems, input-to-state stability, or numerical Lyapunov-function synthesis.
- Encoding stability or orbital decrease as an assumed structure field and projecting it.
- Crediting the label `已验证`, an API typecheck, or a bounded no-match search as theorem evidence.

## Boundary cases

The statement phase must decide a zero-dimensional or singleton state space, a zero vector field,
constant trajectories, `V = 0`, semidefinite `V`, equality in the orbital derivative away from the
equilibrium, disconnected domains, nonunique solutions, empty neighborhoods or sublevel sets,
finite escape time, boundary equilibria, time-origin dependence, and whether local conditions are
uniform in initial time.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IsIntegralCurveOn`, `IsIntegralCurveAt`,
`HasFDerivAt`, `ContinuousAt`, and `Filter.Tendsto` provide adjacent substrate. A bounded search found no
obvious named Lyapunov direct-method criterion under the searched terms in pinned mathlib. The API
probe and search are discovery inputs only, not an exhaustive anchor audit or proof.
