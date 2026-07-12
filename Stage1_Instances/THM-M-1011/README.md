# THM-M-1011 rev-5.6 obligation architecture

This directory is the `planned` intake for Prohorov's theorem. It freezes the intended claim as
the equivalence between uniform tightness and relative compactness, in the weak topology, for a
family of Borel probability measures on a Polish space.

The legacy module is discovery input only. Although it contains wrappers around pinned mathlib
declarations, rev-5.6 requires the statement and later gates to re-audit their exact types,
assumptions, imports, provenance, and source fidelity. This intake assigns them no proof credit.
The provisional root vector is `[H2, M4, R4]`; no exact Lean target, audit completion, or theorem
completion is claimed.

The statement and bounded anchor audit now feed a frozen 14-obligation registry
and seven separate typed graph families. `ObligationTree.lean` checks the
reverse implication and the complete conditional composition with an explicit
`T2Space X` child. Because that child is absent from the frozen pseudo-metric
context, the root remains open at M5. The registry, graph boundary, and exact
validation results are recorded in `obligation-tree.md` and
`obligation-tree-validation.md`; no theorem-completion claim is made.
