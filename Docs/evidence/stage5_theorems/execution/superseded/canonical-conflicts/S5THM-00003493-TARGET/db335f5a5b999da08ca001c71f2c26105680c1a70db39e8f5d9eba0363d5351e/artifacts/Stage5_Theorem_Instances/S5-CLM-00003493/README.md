# S5-CLM-00003493 — maximalLength asymptotic bound

This complete Stage5 target package discharges the sorry-backed frozen theorem
`Arxiv.«1609.08688».maximalLength_le_isBigO` without using its proof body.

The central observation is that the statement permits any real-valued witness
`Ω`. Taking the negative iterated logarithm makes the Big-O condition immediate
because Big-O compares norms, while its exponential is at most one. An
independent pigeonhole proof establishes the quadratic bound on
`maximalLength`, so division by that exponential preserves the bound.

The package contains exact statement transport, source and machine anchors, a
typed proof/provenance/trust/readability DAG, independent trust-zero Lean proof
and audit files, a total injective readable reconstruction, mutation evidence,
and a provisional release receipt. The canonical Master must recompute semantic
identity against the pinned source and is the only authority that can accept
the target or advance the program cursor.
