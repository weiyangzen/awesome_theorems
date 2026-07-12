# THM-M-0311 obligation architecture

The frozen registry contains 17 semantic obligations. It separates the exact target, the real and
complex scalar branches, their checked recomposition, the shared pinned mathlib completeness route,
and source/provenance/trust/computation/workflow boundaries. Eligibility was assigned without
crediting the anchor-audit candidate as accepted proof state.

## Typed proof route

```text
M0311-ROOT [H1, M3, R4]
|-- M0311-S-ENCODING       exact MeasureTheory.Lp quotient and binders
|-- M0311-B-REAL           real scalar branch [open]
|   `-- M0311-L-LP-COMPLETE
|       |-- M0311-L-CRITERION
|       `-- M0311-L-CAUCHY
|           |-- M0311-L-AE-LIMIT
|           |-- M0311-L-AE-CAUCHY
|           |-- M0311-L-NORM-LIMIT
|           `-- M0311-L-MEMLP
|-- M0311-B-COMPLEX        complex scalar branch [open; shared body]
|   `-- M0311-L-LP-COMPLETE
`-- M0311-T-ASSEMBLE       checked conditional child-to-root composition
```

The registry records the same shared upstream obligation for both scalar branches, so wrapper
aliases cannot double-count the terminal body. The proof graph stores reciprocal `proof_requires`
and `composes` edges. Refinement, provenance, evidence, trust, documentation, and workflow edges
are distinct and cannot discharge a proof premise.

## Leaf policy and boundaries

Every leaf-shaped ledger has at most 100 semantic steps; every node with proof children is marked
`split-required`. These are architecture budgets, not proof completion. The pinned source shows
that `instCompleteSpace` invokes `completeSpace_lp_of_cauchy_complete_eLpNorm`, whose witness is
`cauchy_complete_eLpNorm`; that theorem explicitly constructs an almost-everywhere limit, proves
norm convergence, and establishes `MemLp` membership. Those substantive dependencies are retained
rather than hiding the analysis behind the instance name.

`ObligationTree.lean` kernel-checks only the exact real/complex decomposition and recomposition.
The scalar premises remain parameters. Admitting and validating pinned mathlib's terminal bodies,
full transitive provenance and trust closure, and node-scoped receipts belongs to later phases. The
root therefore remains `M3`; no H0, M0, R0, audit-complete, or theorem-complete claim is made.
