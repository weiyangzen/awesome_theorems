# Proof outline

The claim is the solved variant of Erdős problem 1004. Let `IsDistinctTotientRun n K` mean that Euler's totient is injective on the integer interval from `n + 1` through `n + K`. The conclusion asserts the existence of a positive real constant `c` such that, for all sufficiently large natural `n`, every natural `K` satisfying this distinctness hypothesis obeys

`K ≤ n / exp(c (log n)^(1/3))`

after coercion to the reals.

The frozen provider theorem states exactly this proposition behind `answer(True) ↔`; in the source utility, `answer(True)` elaborates to `True`. The canonical Lean project does not currently expose FormalConjectures as an importable package. Each theorem-only replay surface consequently expands `IsDistinctTotientRun` to its frozen body under Mathlib, while carrying the exact module spelling and qualified provider declaration for the frozen semantic validator. The forward and reverse identity transports establish the expanded crosswalk, and the audit wrapper independently re-elaborates the same expression.

The mathematical boundary is important: this package does not manufacture a new elementary proof of the deep Erdős–Pomerance–Sárközy result. Its Lean declarations are conditional identity transports, while the pinned source theorem remains the semantic/provenance authority. The source's `sorryAx` is retained in provenance and never disguised as a local proof. Canonical Master must review the provider/import boundary and independently recompute the elaborated expression, dependencies, and axiom environment before acceptance.
