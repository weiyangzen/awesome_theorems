# THM-M-1414 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog target "spectral
decomposition theorem" in dynamical systems. The repository supplies only Stephen Smale, 1967,
and the gloss "decomposition of Axiom A systems." Its `已验证` label is explicitly untrusted and
provides no human-source or machine-proof credit.

A primary-source candidate has been inspected: Stephen Smale, *Differentiable dynamical systems*,
**Bulletin of the American Mathematical Society** 73(6) (1967), 747-817, DOI
`10.1090/S0002-9904-1967-11798-1`. Theorem (6.2), printed page 777, is the spectral decomposition
of an Axiom A diffeomorphism on a compact manifold. It uniquely writes the nonwandering set as a
finite union of pairwise disjoint closed invariant indecomposable pieces, with the restriction to
each piece topologically transitive. The same paper also states a materially different flow
version as Part II, theorem (5.2), printed page 803. The catalog gloss does not select between them.

This intake therefore records theorem (6.2) as the leading candidate while leaving the canonical
mathematical and Lean statements null until source selection and independent review resolve the
diffeomorphism/flow boundary and all definitions. The provisional vector is `[H1, M4, R3]`: a
published source and proof-sketch locator are known, no usable exact formal artifact has been
located, and no complete readable reconstruction exists.

The lifecycle remains `planned`; all six downstream tasks and master acceptance remain open. The
Lean file is an API-only probe and neither states nor proves the target. No H0, M0, R0, audit
completion, theorem completion, or accepted execution state is claimed.
