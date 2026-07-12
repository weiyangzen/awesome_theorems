# Scope map

## Preserved catalog scope

The intake preserves only the ordinary-differential-equations target `THM-M-1378`, the name
`Euler-Lagrange方程`, the attribution to Leonhard Euler and Joseph Lagrange, the year 1755, and the
gloss `泛函极值的微分方程`. The wording points to the Euler-Lagrange necessary-condition family.
It is not itself a quantified theorem and does not authorize one conventional variant as the root.

## Proposition-changing decisions

An approved source correction must freeze all of the following before statement elaboration:

- whether the root is a necessary condition for a local extremum, stationarity implies the
  differential equation, a weak-to-classical implication, a converse, or only an operator formula;
- the independent-variable domain and dimension, the codomain and scalar field, the interval or
  open-set model, universes, topology, normed structures, and coordinate conventions;
- the integrand or Lagrangian, its explicit time dependence, derivative convention, regularity,
  integrability, and any convexity, Legendre, or nondegeneracy assumptions;
- the admissible functions and variations, path regularity, fixed/free endpoint policy, compact
  support or boundary conditions, and the exact definition of first variation or extremum;
- every ordered binder and dependency, the local or global hypothesis, and whether all variations
  are quantified before or after the candidate extremal;
- the classical, almost-everywhere, distributional, or weak conclusion and its sign convention,
  such as `d/dt (partial L / partial v) = partial L / partial q`;
- the source edition, theorem/formula/page, incorporated definitions, assumptions, proof boundary,
  corrections and errata, translation, and independent review.

## Boundary and degenerate cases

The selected proposition must explicitly decide a zero-length interval, an empty interior,
constant paths, zero-dimensional configuration spaces, a zero or path-independent Lagrangian,
nonsmooth extrema, nonintegrable derivatives, free endpoints and transversality terms, constrained
variations, singular Lagrangians, corners, and whether endpoint equalities are data or hypotheses.
No case is excluded or credited before the exact proposition is selected.

## Neighbor and substitution exclusions

- `THM-M-1377` is the broader calculus-of-variations target; its scope and evidence are not shared.
- `THM-M-1382` and `THM-M-1518` are least-action targets. A stationary-action principle may be an
  upstream hypothesis, but neither target selects this target's statement or transfers status.
- `THM-M-1517` is Lagrangian mechanics. Its abstract system fields cannot replace a concrete
  calculus-of-variations theorem.
- `THM-P-0749` is a separate physics-corpus record. Its `delta integral L dt = 0` wording is
  contextual discovery input, not source authority for `THM-M-1378`.
- `Stage1_Instances/THM-M-1518/Statement.lean` is a later statement chosen for another target and
  cannot be copied without a checked, source-approved relationship.
- `S1_M_186.lean` assumes the crucial first-variation-to-Euler-Lagrange bridge as structure data;
  `S1_M_187.lean` states the converse Euler-Lagrange-to-stationarity direction; neither closes this
  target.
- `S1_M_184.lean` proves only that every real-line path satisfies the zero-Lagrangian equation; it
  does not prove any extremum or stationarity premise implies that equation.
- A finite-dimensional specialization, autonomous Lagrangian, local-minimum premise, weak equation,
  numerical extremizer, generic calculus API, or external URL cannot silently replace the root.
- A predicate, structure field, hypothesis, axiom, or unchecked certificate that assumes the desired
  differential equation supplies no proof credit.
- The catalog's `已验证` label and this intake API probe supply no human-source or machine-proof
  evidence.

The canonical statement, Lean expression and environment fingerprints, transports, mutations,
discovery protocol, obligation registry, and proof state remain unfrozen.
