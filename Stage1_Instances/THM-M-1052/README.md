# THM-M-1052 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Krylov-Bogolyubov
invariant-measure theorem. Historical Stage0 text and the existing
`S1_M_219.lean` module are discovery inputs only; this intake grants them no
proof or acceptance credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Existence of an invariant Borel probability measure for continuous/Feller dynamics under a compactness or tightness hypothesis | The precise classical variant must be selected and elaborated in the dependent statement phase |
| Deterministic form | Continuous self-map of a nonempty compact Hausdorff/Borel state space | Candidate specialization; no equivalence or proof credit |
| Markov form | Feller Markov kernel with tight empirical averages (compact state space as a sufficient specialization) | Candidate canonical generalization; exact hypotheses remain open |
| Construction | Cesaro averages of iterated pushforwards from an initial probability/point mass | Architecture only |
| Compactness branch | compactness of probability measures, or Prokhorov compactness from tightness | Open machine and source frontier |
| Limit branch | select a weak cluster point and pass the Feller action through weak convergence | Open machine and source frontier |
| Conclusion | the cluster point is a probability measure invariant under the dynamics/kernel | Open machine frontier |
| Foundations | Lean 4 kernel and pinned mathlib, with classical choice used only if exposed by the final dependency audit | Exact toolchain, imports, axioms, and TCB fingerprint are deferred |

The human source wording currently available in the repository says only
"existence of invariant measures". It is too underspecified to choose silently
between the deterministic compact-space theorem and the Feller-kernel/tightness
form. `intake.json` therefore freezes the intended theorem family and the
ambiguity rather than inventing a stronger claim.

## Open task DAG

`statement` -> `anchor_audit` -> `obligation_tree` -> `proof` -> `validation`
-> `release`. The statement phase must resolve the source variant before any
downstream proof evidence can be credited.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M3, R3]`. The first
failed theorem gate is exact-statement identification/elaboration. The intake
node itself is self-tested, but master acceptance is still required. The
theorem is not complete.

