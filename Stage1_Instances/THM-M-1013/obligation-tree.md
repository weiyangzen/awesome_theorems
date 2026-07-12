# THM-M-1013 frozen obligation architecture

Item: `S56-M-1013-OBLIGATION_TREE`.

The registry freezes fourteen root-relevant obligations around the characteristic-function route
found by the immutable anchor audit. This architecture records what must be proved and checked; it
does not take proof-phase credit merely because viable terminal candidates are already known.

## Typed proof route

```text
M1013-ROOT exact Cramer-Wold biconditional
`-- M1013-T-COMPOSE checked composition of both implications
    |-- M1013-F forward implication
    |   |-- M1013-F-MAP continuous mapping theorem
    |   `-- M1013-C-PROJECTION continuous scalar projection
    `-- M1013-R reverse implication
        |-- M1013-R-VECTOR-CHAR vector characteristic-function criterion
        |-- M1013-R-SCALAR-CHAR scalar criterion at frequency one
        `-- M1013-R-PROJ-ID projected/vector characteristic-function identity
            `-- M1013-C-PROJECTION
```

`M1013-S` binds the elaborated statement, while `M1013-S-BOUNDARY` records that `d = 0` is retained
and checked rather than silently excluded. `M1013-X-SOURCE`, `M1013-X-PROVENANCE`, and
`M1013-X-TRUST` are separate non-proof graphs and cannot be counted as mathematical premises.

## Semantic ledgers

| ID | Premises and inference | Output and parent use | Budget / boundary |
|---|---|---|---|
| `M1013-ROOT` | Every `d`, sequence `mu`, and limit `mu0` | Exact frozen biconditional | 20; open M3 |
| `M1013-S` | Frozen imports, binders, projection, topology | Statement fingerprint and representation | 35; locally elaborated |
| `M1013-S-BOUNDARY` | Root instantiated at `d = 0` | Zero-dimensional target remains included | 20; checked consequence only |
| `M1013-T-COMPOSE` | Exact forward and reverse implications | Exact root via `Iff.intro` | 20; checked conditional composition |
| `M1013-F` | Vector weak convergence | Every scalar pushforward converges | 30; proof-phase credit open |
| `M1013-F-MAP` | Weak convergence and continuous projection | Weak convergence after `ProbabilityMeasure.map` | 35; pinned mathlib bridge candidate |
| `M1013-R` | Every scalar pushforward converges | Vector weak convergence | 45; proof-phase credit open |
| `M1013-R-VECTOR-CHAR` | Pointwise vector characteristic-function convergence | Vector weak convergence | 40; pinned mathlib bridge candidate |
| `M1013-R-SCALAR-CHAR` | Weak convergence of the `t` projection | Characteristic convergence at frequency `1` | 35; pinned mathlib bridge candidate |
| `M1013-R-PROJ-ID` | Map-integral identity and inner-product simplification | `charFun (map (projection t) mu) 1 = charFun mu t` | 40; local candidate inventoried |
| `M1013-C-PROJECTION` | Inner product with fixed `t` | Continuous and measurable projection | 25; local checked construction |
| `M1013-X-SOURCE` | Primary edition, theorem locator, assumptions, errata | Reviewed node-to-source crosswalk | 100; open H1 |
| `M1013-X-PROVENANCE` | Terminal bodies, imports, revisions, licenses | Transitive body-origin inventory | 70; open |
| `M1013-X-TRUST` | Axiom policy, replay, freshness, second verifier | Accepted trust closure | 70; open |

## Freeze boundary

The immediate mathematical root cut is `M1013-F` plus `M1013-R`. The Lean harness consumes both
children and yields the exact root; it also proves that the zero-dimensional specialization is in
scope. Normalization and case-split layers add no separate mathematical premise: the selected
Euclidean representation is already canonical, and the generic characteristic-function argument
has no dimension or coefficient case split. Construction work is represented explicitly by
`M1013-C-PROJECTION`.

Any later split, merge, eligibility change, or target change requires a new registry version and an
append-only delta. Human-source reconstruction, proof execution, terminal provenance, release trust,
readable independent review, and master acceptance remain open. Theorem completion is false.
