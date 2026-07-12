# THM-M-0162 frozen obligation architecture

Item: `S56-M-0162-OBLIGATION_TREE`.

The registry freezes 17 semantic obligations before proof execution. It follows the classical
moving-frame proof but keeps source, trust, provenance, documentation, and workflow edges separate
from mathematical proof requirements.

## Typed proof route

```text
M0162-ROOT exact canonical proposition
`-- M0162-T-ASSEMBLE checked conditional conjunction/quantifier composition
    |-- M0162-E-TANGENT T' = kappa N
    |   `-- M0162-S-PREMISES exact hypotheses and conventions
    |-- M0162-E-NORMAL N' = -kappa T + tau B
    |   |-- M0162-F-ORTHONORMAL oriented orthonormal frame
    |   |-- M0162-D-INNER differentiated inner products
    |   |-- M0162-A-DECOMPOSE basis coefficient reconstruction
    |   |-- M0162-C-NORMAL-T tangent coefficient -kappa
    |   |   `-- M0162-E-TANGENT
    |   |-- M0162-C-NORMAL-N normal coefficient zero
    |   |   `-- M0162-D-INNER
    |   `-- M0162-C-NORMAL-B binormal coefficient tau
    |       `-- M0162-D-CROSS
    `-- M0162-E-BINORMAL B' = -tau N
        |-- M0162-F-ORTHONORMAL
        |-- M0162-A-DECOMPOSE
        |-- M0162-D-CROSS derivative of B = T cross N
        `-- M0162-C-BINORMAL coefficients (0, -tau, 0)
            |-- M0162-D-INNER
            `-- M0162-D-CROSS
```

`M0162-S-FOUNDATION`, `M0162-X-SOURCE`, and `M0162-X-PROVENANCE` are root-relevant
trust/source/provenance overlays, not hidden proof premises.

## Semantic leaf ledgers

Every node has a typed premise/inference/output/use ledger in `typed-graphs.json` and a step budget
of 60, below the 100-step split ceiling. The major differentiated-inner-product, cross-product,
orthonormal-frame, decomposition, and coefficient arguments are explicit nodes rather than being
compressed into calls to an unnamed "standard" theorem.

Only `M0162-S-PREMISES` and `M0162-T-ASSEMBLE` have checked local interfaces (`M0-L`). The latter
is deliberately conditional: it consumes the tangent, normal, and binormal packages and therefore
does not close any of them.

## Freeze boundary

The minimal open root cut is `M0162-E-TANGENT`, `M0162-E-NORMAL`, and
`M0162-E-BINORMAL`. The root remains `[H1, M3, R4]`; the deeper mathematical leaves are `M4`.
No proof body, source acceptance, audit completion, or theorem completion is claimed. Registry
corrections, splits, merges, or eligibility changes require a new version and append-only delta.
