# THM-M-0441 frozen obligation architecture

Item: `S56-M-0441-OBLIGATION_TREE`

The registry freezes 21 root-relevant obligations for the exact declaration
`Stage1Instances.THM_M_0441.PilaWilkie`. Its denominator comes from the elaborated
statement and immutable anchor audit before proof metrics were observed. Any
later split, merge, exclusion, or statement correction requires an append-only
registry revision.

## Typed proof route

The route separates the exact statement (`M0441-S`), definable normalization
(`M0441-N`), uniform constructions (`M0441-C`), determinant/counting engine
(`M0441-L`), dimension branches (`M0441-B`), and terminal composition (`M0441-T`).
The zero-dimensional branch counts isolated contributions. Positive-dimensional
connected semialgebraic blocks are removed by `algebraicPart`. The residual
pieces require dimension induction with an unchanged exponent budget.

`ObligationTree.engine_compose` checks binder-preserving assembly from four
explicit abstract engine premises to the exact canonical proposition. The
structure is an interface: no instance or premise inhabitant is declared, so
this certificate does not prove Pila-Wilkie.

## Node ledger

| ID | Role | Budget | Current boundary |
|---|---|---:|---|
| `M0441-ROOT` | Exact canonical theorem | split required | `M3`, open |
| `M0441-S` | Statement and foundation | split required | exact target elaborated |
| `M0441-S-OMIN` | O-minimal/definability semantics | 35 | interface only |
| `M0441-S-HEIGHT` | Affine height and bounded slice | 30 | definition elaborated |
| `M0441-S-ALG` | Algebraic-part dimension bridge | 60 | definition elaborated; bridge open |
| `M0441-N` | Definable normalization | split required | open |
| `M0441-N-CELLS` | Controlled cells/charts | 90 | open |
| `M0441-N-BOUNDARY` | Boundary dimension control | 80 | open |
| `M0441-C` | Construction package | split required | open |
| `M0441-C-PARAM` | Uniform parameterization | 100 | open |
| `M0441-C-BLOCKS` | Semialgebraic blocks | 100 | open |
| `M0441-L` | Core counting engine | split required | open |
| `M0441-L-DET` | Determinant/hypersurface estimate | 100 | open |
| `M0441-L-COUNT` | Uniform subpolynomial count | 100 | open |
| `M0441-B` | Exhaustive dimension split | split required | open |
| `M0441-B-ZERO` | Zero-dimensional branch | 80 | open |
| `M0441-B-POS` | Positive-dimensional branch | 70 | open |
| `M0441-B-INDUCT` | Dimension induction and epsilon budget | 100 | open |
| `M0441-T` | Conditional root assembly | 24 | composition term checked; inputs open |
| `M0441-SOURCE` | Proof-source/errata crosswalk | 80 | `H1`, machine not applicable |
| `M0441-TRUST` | Provenance, TCB, replay, review | 60 | open |

Numeric leaf budgets are at most 100 semantic steps. Aggregate nodes remain
`split required`; the threshold is not a closure or readability claim.

## Separate graph families

`typed-graphs.json` stores proof, refinement, provenance, evidence, trust,
documentation, and workflow edges separately. Source and trust nodes never
become proof premises. The statement definitions and conditional composition
term receive no credit as terminal bodies for the missing mathematical engines.

## Freeze boundary

No proof obligation is machine-closed by this architecture phase. The root cut
set includes uniform parameterization, determinant estimation, block
construction, dimension induction, primary proof-source reconstruction, and
trust/replay review. `audit_complete=false` and `theorem_complete=false`.
