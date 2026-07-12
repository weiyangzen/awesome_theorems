# THM-M-0510 frozen obligation architecture

Item `S56-M-0510-OBLIGATION_TREE` freezes registry version 1 against the exact
`Statement.lean` and `anchor-audit.json` hashes in `obligation-registry.json`.
The 17-ID inventory is the denominator for later coverage. Any correction,
split, merge, exclusion, or eligibility change requires a versioned,
append-only delta; later proof discovery cannot silently shrink it.

## Proof architecture

The selected architecture is the analytic circle method. It first connects
the ordinary partition generating function to the reciprocal Euler product
and to coefficient extraction on an admissible contour. The contour is split
exhaustively into major and minor arcs. The major arc consumes the modular
transformation, a uniform local approximation, a model-integral reduction,
and the exact saddle-point asymptotic. The minor arcs require a uniform
little-o estimate. Recomposition must consume both branches and preserve the
constant `1 / (4 * sqrt 3)` before transporting relative-error convergence to
the canonical `IsEquivalent atTop` statement.

```text
M0510-ROOT
`-- T-ASYMPTOTIC
    |-- S-ENCODING
    |-- S-BOUNDARY
    `-- T-RECOMBINE
        |-- N-EULER-PRODUCT
        |-- N-COEFFICIENT
        |-- C-CONTOUR
        `-- B-ARC-SPLIT
            |-- L-MAJOR-LOCAL
            |   |-- L-MODULAR
            |   `-- L-MAJOR-INTEGRAL
            |       `-- L-MAJOR-ASYMPTOTIC
            `-- L-MINOR-BOUND
```

The separate proof, refinement, provenance, evidence, trust, documentation,
and workflow graphs prevent citations and receipts from becoming proof
premises. Proof edges have reciprocal `proof_requires`/`composes` records.
Every node owns a complete schema, substantive ledger, and budget no greater
than 100. The critical analytic nodes remain separate bridge obligations even
if a future Lean body invokes a single deep theorem.

## Closure boundary

Only the already elaborated statement interfaces and the exact final transport
in `ObligationTree.lean` have scoped kernel evidence. `FinalAsymptoticPackage`
is definitionally the exact root, so `root_of_finalAsymptotic` checks the output
boundary but deliberately supplies no analytic proof or composition credit.
All Euler-product, contour, modular-transformation, major-arc, and minor-arc
bodies are open. The primary source map and transitive foundation audit are
also open. Consequently the root stays `M3`, H2 and R4 remain unchanged, the
theorem is incomplete, and no accepted receipt is claimed.

The first open cut is the ordinary Euler-product identity, coefficient
extraction, admissible contour, modular transformation, minor-arc estimate,
source map, and foundation audit. Proof work must refine any central node that
cannot truthfully fit its frozen 100-step budget before closure is considered.
