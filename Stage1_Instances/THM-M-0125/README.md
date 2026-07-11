# THM-M-0125 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Gross-Zagier formula. Historical Stage1
code is discovery input only and contributes no proof or statement credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | The Gross-Zagier height formula relating a central derivative of a Rankin/Hasse-Weil L-series to the Neron-Tate height of a Heegner point | The original paper has several normalizations and levels; the exact variant must be selected in the statement phase |
| Arithmetic objects | modular elliptic curve/modular parametrization, imaginary quadratic field, Heegner hypothesis, Heegner point | Domains, conductors, embeddings, and rationality fields must be explicit |
| Analytic side | completed or imprimitive L-series, central point, first derivative, periods and local factors | No generic complex function may substitute for the arithmetic L-series |
| Height side | Neron-Tate height or height pairing of the corresponding Heegner divisor/point | The actual canonical height construction is required, not an uninterpreted scalar |
| Normalization | degree/index, periods, discriminant, unit, conductor, and local factors selected by the source variant | A named convention and checked conversion are mandatory |
| Consequences | analytic-rank-one non-torsion/rank consequences | Out of the root unless separately derived from the exact formula |
| Foundations | Lean 4 kernel and pinned mathlib with an explicit classical/choice/quotient profile | Exact toolchain, imports, and dependency closure remain open |

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_044.lean` is not the canonical
target: its `GrossZagierStatementData.expectedFormula` is an abstract implication whose arithmetic
inputs are stored fields. It explicitly says that no proof of Gross-Zagier is claimed.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The human theorem family and a
primary source are identified, but the exact source variant and normalization are not yet frozen.
Consequently no canonical Lean declaration or expression is claimed at intake. The first failed
gate is the exact-source-statement gate, and the theorem is not complete.

## Open task DAG

`STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`, with the dependency
edges fixed by the rev-5.6 execution DAG. Intake does not close any dependent node.

