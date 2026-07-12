# S56-M-1245-ANCHOR_AUDIT receipt

## Audit boundary

The audited root is `Stage1Instances.THM_M_1245.SobolevInequalityTarget` from `Statement.lean`:
the scalar, compactly supported `C1` Euclidean estimate, including `p = 1`, with the constant
outside the function binder. A Sobolev-space embedding, a compact embedding, or a Fourier
inequality on a torus is not substituted for this target.

## Pinned mathlib candidate

The Lake manifest pins mathlib4 at `8a178386ffc0f5fef0b77738bb5449d50efeea95` and Lean at
`v4.29.0`. The terminal candidate is
`MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner` in
`Mathlib.Analysis.FunctionalSpaces.SobolevInequality`. Specializing its domain to
`EuclideanSpace Real (Fin n)`, codomain to `Real`, and measure to `volume` makes its hypotheses
identical to the per-function premises of the frozen target. Its explicit nonnegative constant is
independent of the function and therefore witnesses the frozen existential.

`AnchorAudit.lean` checks the candidate and three nearby declarations, elaborates the complete
specialization, and prints the candidate's axiom profile. Lean reports only `propext`,
`Classical.choice`, and `Quot.sound`. A source scan of the pinned module found no `sorry`, `admit`,
local `axiom`, or `unsafe` marker. The module is Apache-2.0 licensed. These facts identify a real
pinned proof body and a feasible direct wrapper; this audit does not preempt the later proof node by
declaring that named wrapper.

| Candidate | Role | Boundary |
|---|---|---|
| `eLpNorm_le_eLpNorm_fderiv_of_eq_inner` | exact scalar terminal anchor | proof node still owns the root wrapper |
| `eLpNorm_le_eLpNorm_fderiv_one` | upstream `p = 1` foundation | narrower than the full target |
| `eLpNorm_le_eLpNorm_fderiv_of_eq` | finite-dimensional codomain alternative | applicable but less direct for scalar values |
| `eLpNorm_le_eLpNorm_fderiv_of_le` | bounded-support generalization | adds a support-set parameter and weaker exponent relation |

## External Lean 4 candidates

Bounded GitHub discovery used four recorded queries. At immutable revision
`88d0535ecf0d2c31dd7f53674919da0aa7c40c7b`, `grunweg/SobolevSlobodeckij` says the embedding
theorem is planned and delegates the inequality to mathlib; its inspected sources contain
placeholders. At revision `70f85d4c1bf99c6e7d61e8be4daa6f3664d08d23`,
`abenenson/rellich-kondrachov` proves compact `H1 -> L2` embedding on compact Riemannian manifolds,
not this norm inequality. `Brsanch/sqg-lean-proofs-fourier` advertises a homogeneous Fourier
embedding on the two-torus, also a different statement; immutable revision retrieval was not
available after the GitHub API rate limit was exhausted, so it receives no immutable anchor credit.

The search is a bounded inventory, not an assertion that no unindexed or future project exists. No
external repository was installed and `.lake` was not mutated.

## Verdict

The anchor-audit node is self-tested. The root vector is provisionally `[H2, M1, R3]`: a direct
pinned terminal candidate exists, but the named root wrapper, primary-source review, readable
reconstruction, and all release gates remain open. No H0, M0, proof acceptance, audit completion,
or theorem completion is claimed.
