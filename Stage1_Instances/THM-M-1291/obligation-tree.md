# THM-M-1291 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 17 obligations before proof execution. The exact
denominator is recorded in `obligation-registry.json`. Eligibility follows the
canonical arbitrary-measure-space, complex-valued statement for every real
`p > 0`; it was not inferred from available proof bodies. The source boundary
and provenance/trust overlays cannot receive mathematical proof credit.

## Typed proof route

```text
M1291-ROOT [open M3]
`-- M1291-T-ASSEMBLE exact root assembly
    `-- M1291-T-ALGEBRA integral-expression transport
        `-- M1291-T-INTEGRAL [remaining root cut]
            |-- M1291-L-POINTWISE AE corrected-remainder convergence
            |   `-- M1291-B-MERGE
            |       |-- M1291-B-SUBUNIT  (0 < p <= 1)
            |       `-- M1291-B-SUPERUNIT (1 < p)
            |-- M1291-L-TRUNCATION nonnegative error construction
            `-- M1291-L-TAIL uniform tail control
```

The proof graph gives each dependency a reciprocal `composes` edge. Separate
refinement, provenance, evidence, trust, documentation, and workflow graphs
prevent source or governance records from masquerading as proof premises. All
semantic ledgers have budgets at most 100 steps. A node exceeding that budget
must be split through a versioned, append-only registry delta.

## Status boundary

No obligation is closed in this phase. In particular, the uniform bound in the
canonical hypothesis is not silently strengthened to domination, and the
subunit exponent range is not discarded. The root remains `[H2, M3, R4]` with
`M1291-T-INTEGRAL` as the first substantive cut. Proof, provenance, readable
reconstruction, independent verification, and all release gates remain open.
