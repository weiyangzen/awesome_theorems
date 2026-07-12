# Scope map

## Received scope

The repository fixes only the title `Hartman-Grobman定理`, the attribution to Philip Hartman and
David Grobman, the year 1960, and the gloss `双曲平衡点的局部线性化` ("local linearization of a
hyperbolic equilibrium"). It supplies no citation, definition, ordered binder, hypothesis,
conclusion, exceptional case, or formal artifact. Stage0 repeats those fields and explicitly
leaves exact premises, equivalent formulations, axioms, machine status, and artifact links open.

The word "equilibrium" constrains the intended family toward a continuous-time autonomous vector
field and its flow. It does not by itself choose one exact theorem. The discrete-time version for a
local diffeomorphism at a hyperbolic fixed point remains a separately recognizable Hartman-Grobman
formulation and must not be substituted without a reviewed target decision.

## Inspected source candidates

Hartman's 1960 Theorem (II), page 615, is the closest historical candidate inspected. It starts
with a real autonomous system `x' = T x + F(x)` near zero, with `F = o(|x|)`, `F` of class `C2`,
and all eigenvalues of `T` off the imaginary axis. It produces a continuous one-to-one map from a
neighborhood of zero onto a neighborhood of zero whose coordinate change sends the nonlinear flow
to `u' = T u`, preserving parametrization. This is candidate scope, not the canonical claim.

Teschl's 2012 Theorem 9.9, page 264, is a modern candidate. It states the result for a
differentiable vector field with zero as a hyperbolic fixed point and a homeomorphism locally
conjugating its flow to the flow of the Jacobian. The surrounding proof uses derivative control;
the book also gives a discrete-map version as Theorem 10.4. Its official errata repairs
proof-relevant details on printed pages 265, 266, and 268. The catalogue does not identify this
source or choose between its corrected conventions and Hartman's historical `C2` formulation.

## Proposition-changing decisions

An exact source decision and statement phase must freeze all of the following:

- continuous flow versus discrete local diffeomorphism, and whether a time-one map is merely a
  proof reduction or the theorem's root;
- finite-dimensional `Real^n`, an arbitrary finite-dimensional real normed space, or a Banach
  space, including dimension, universes, norms, and coordinate identifications;
- an equilibrium translated to zero versus an arbitrary point `p`, and the checked translation;
- an autonomous vector field, its domain, the local solution/flow object, existence and uniqueness,
  and the time interval on which conjugacy is asserted;
- `C1`, differentiable, `C2`, or another regularity package, including whether little-o at the
  equilibrium is explicit or derived from differentiability;
- hyperbolicity as all complexified eigenvalues having nonzero real part, a spectral condition,
  or an invariant stable/unstable splitting, with a checked equivalence if alternatives are used;
- a homeomorphism between specified neighborhoods, an unbundled continuous bijection, or a local
  homeomorphism, including whether it fixes the equilibrium;
- the orientation of the conjugacy equation and whether it preserves time parametrization for all
  admissible real times or only maps unparametrized orbits; and
- whether bounded-displacement or uniqueness properties of the conjugating map are part of the
  root, proof infrastructure, or excluded strengthenings.

These choices yield inequivalent propositions or materially different formal interfaces. They are
a resolution checklist, not an inferred statement.

## Boundary and mutation cases

The statement phase must resolve and mutation-test at least:

1. removal or weakening of the differentiability/regularity premise;
2. allowing an eigenvalue on the imaginary axis;
3. replacing finite-dimensional Euclidean space by a general normed or Banach space;
4. changing a flow conjugacy for every local time to a conjugacy only of time-one maps;
5. changing parametrized topological conjugacy to orbit equivalence with a time change;
6. failure to fix the equilibrium or to map neighborhoods onto neighborhoods;
7. the zero-dimensional phase space, zero vector field, purely stable, purely unstable, and mixed
   stable/unstable cases; and
8. trajectories or conjugacy images leaving the selected local neighborhoods.

## Explicit exclusions

- `THM-M-1344` Lyapunov's indirect method: stability inferred from linearization, not topological
  conjugacy of the full local dynamics.
- `THM-M-1346` stable manifold theorem and `THM-M-1347` center manifold theorem.
- `THM-M-1366` structural stability, which is not the same root as conjugacy to one linearization.
- The discrete-map theorem, a time-one-map lemma, or a one-dimensional/scalar example used as the
  continuous-time root without a checked source-approved transport.
- A theorem assuming the desired homeomorphism, conjugacy equation, stable/unstable splitting, or
  linearization conclusion as data.
- `Matrix.IsHyperbolic` for two-by-two matrices, which means positive discriminant in pinned
  mathlib and is not the ODE hyperbolicity predicate required here.
- A phase portrait, numerical simulation, name match, API probe, or the catalogue's `已验证` label
  as source or theorem evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides `IsIntegralCurveOn`, `Flow`,
`Flow.toHomeomorph`, `Function.IsFixedPt`, `HasFDerivAt`, `fderiv`, `IsLocalHomeomorphOn`,
`Homeomorph`, `OpenPartialHomeomorph`, and conjugacy predicates, plus general spectrum and
matrix-exponential infrastructure. `Flow.IsSemiconjugacy` is a global continuous-surjection
interface, not a direct encoding of local neighborhood conjugacy.
A bounded repository and pinned-mathlib search found no Hartman-Grobman declaration or exact
hyperbolic-equilibrium conjugacy theorem. The API probe is feasibility evidence only; it is not an
anchor audit, statement elaboration, or machine-proof result.
