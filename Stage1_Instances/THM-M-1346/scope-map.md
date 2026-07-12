# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1346`, the label `稳定流形定理` (stable manifold theorem),
the gloss `双曲平衡点的稳定与不稳定流形`, the attribution "many mathematicians," and the
twentieth century. Importance "high" and status `已验证` are catalog metadata, not theorem or proof
evidence.

This identifies a theorem family about stable and unstable manifolds near a hyperbolic equilibrium.
It does not select a phase space, dynamics, theorem variant, definitions, hypotheses, conclusion,
or source.

## Proposition-changing decisions

An approved statement run must freeze all of the following from an immutable source:

- continuous-time autonomous ODE/vector-field flow versus a discrete diffeomorphism or time-one
  map, including the precise relationship between "equilibrium" and "fixed point";
- finite-dimensional `R^n`, a finite-dimensional smooth manifold, a Banach space/manifold, or
  another phase space, with its scalar field, dimensions, charts, and completeness assumptions;
- regularity of the vector field or map and whether the asserted leaves are `C^k`, smoother,
  analytic, topological, immersed, or embedded;
- the definition of hyperbolicity: the Jacobian/derivative at the equilibrium, exclusion of
  spectrum on the imaginary axis or unit circle, and the exact stable/unstable spectral splitting;
- local stable/unstable sets, exponential-rate sets, or global stable/unstable sets, with their
  orbit-existence, neighborhood, convergence, and rate predicates;
- whether the conclusion is graph existence over the spectral subspaces, manifold existence,
  tangency, dimension, local/global invariance, exponential estimates, uniqueness, equality with
  stable/unstable sets, or the complete conjunction of these clauses;
- time direction and whether a complete backward flow or local inverse is required for the
  unstable branch; and
- all quantifier ordering, universe, boundary, trivial-subspace, and zero-dimensional cases.

These decisions produce inequivalent theorems. They are a resolution ledger, not a statement.

## Candidate branches not credited

The inspected preliminary edition of Gerald Teschl's *Ordinary Differential Equations and
Dynamical Systems*, Section 9.2, makes the ambiguity concrete:

- Theorem 9.3 gives an exponential-rate local graph over `E^{+,alpha}` when a shifted
  linearization is hyperbolic, together with tangency and nesting properties.
- Theorem 9.4 gives local stable and unstable `C^k` graphs, tangency, and exponential estimates for
  a `C^k` vector field with a fixed point; its wording does not itself assume the fixed point is
  hyperbolic.
- Theorem 9.5 adds hyperbolicity and identifies the stable/unstable manifolds with points whose
  forward/backward orbits remain in a sufficiently small neighborhood, and with the global
  stable/unstable sets.

The catalog does not cite this source or choose one result or conjunction. None is canonical or
credited at intake.

## Explicit exclusions

- `THM-M-1345` Hartman-Grobman local topological conjugacy, `THM-M-1347` center manifolds, or a
  Lyapunov stability criterion substituted for this target.
- `THM-M-1411` generic hyperbolic systems, `THM-M-1414` Anosov flows, or `THM-M-1420` Pesin theory
  substituted for a hyperbolic-equilibrium theorem.
- The separate physics catalog target `THM-P-0744` silently used as a source or replacement.
- Only linear spectral-subspace invariance, local ODE existence, convergence of one trajectory,
  or an invariant-set definition presented as the nonlinear manifold theorem.
- A structure or hypothesis that assumes the desired stable/unstable manifold, graph,
  invariance, tangency, exponential estimate, or set equality.
- Numerical phase portraits, sampled trajectories, or the catalog label `已验证` credited as
  source or kernel evidence.

## Degenerate and boundary cases

The selected source must decide an equilibrium with a purely stable or purely unstable
linearization, zero-dimensional stable or unstable subspaces, the zero-dimensional phase space,
empty local chart domains, a zero vector field (which is not hyperbolic in positive dimension),
semiflows without backward time, noncomplete vector fields, local versus global orbit existence,
the equilibrium's membership in both leaves, and whether global leaves are embedded, immersed, or
only injectively immersed.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides `IsIntegralCurve`,
`IsMIntegralCurve`, `Flow`, `IsInvariant`, `Function.IsFixedPt`, and
`Manifold.IsSmoothEmbedding`. The bounded intake search found no declaration named or documented
as a stable, unstable, or invariant manifold theorem in pinned mathlib or the repository-local
Lean modules. The probe and search are feasibility evidence only, not an exhaustive anchor audit,
exact target elaboration, or proof evidence.
