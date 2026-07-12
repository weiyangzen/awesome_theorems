# THM-M-0353 frozen obligation architecture

Item: `S56-M-0353-OBLIGATION_TREE`.

The registry freezes 16 obligations before proof execution. It selects the Gaussian-polynomial
orthogonality, polynomial density, measure-changing isometry, complexification, and Hilbert-basis
packaging route. This architecture assigns work; it supplies no proof or source credit.

## Typed proof route

```text
M0353-ROOT
`-- M0353-T-ASSEMBLE (kernel-checked conditional conjunction)
    |-- M0353-P-MEMLP
    |   `-- M0353-C-LP-VECTORS
    `-- M0353-P-BASIS
        `-- M0353-C-HILBERT-BASIS
            |-- M0353-C-LP-VECTORS
            |-- M0353-L-ORTHONORMAL
            |   `-- M0353-L-GAUSSIAN-ORTH
            |       |-- M0353-X-HERMITE-POLY
            |       `-- M0353-S-NORMALIZATION
            `-- M0353-L-DENSE
                |-- M0353-L-POLY-DENSE
                |   `-- M0353-X-HERMITE-POLY
                `-- M0353-T-MEASURE
                    `-- M0353-S-NORMALIZATION
```

`M0353-S-NORMALIZATION` preserves the exact probabilists' polynomial scaling, factorial and pi
constants, natural-number indexing including zero, complex scalars, and Lebesgue measure.
`M0353-X-SOURCE`, `M0353-X-TRUST`, and `M0353-X-PROVENANCE` are separate documentation, trust,
and provenance boundaries; none is a proof premise. Every semantic node has a step budget at most
100. In particular, Gaussian orthogonality, density, and the weighted-to-unweighted transport stay
visible rather than being hidden behind a short invocation.

The minimal open root cut is `M0353-P-MEMLP` plus `M0353-P-BASIS`. The conditional assembly in
`ObligationTree.lean` elaborates without placeholders but proves neither package. Root debt remains
`[H1, M3, R4]`; audit completion and theorem completion remain false. Any registry change requires
a new version and an append-only delta.

## Node anchors

The stable anchors are `m0353-root`, `m0353-t-assemble`, `m0353-p-memlp`, `m0353-p-basis`,
`m0353-c-lp-vectors`, `m0353-l-orthonormal`, `m0353-l-dense`, `m0353-c-hilbert-basis`,
`m0353-l-gaussian-orth`, `m0353-l-poly-dense`, `m0353-t-measure`,
`m0353-s-normalization`, `m0353-x-hermite-poly`, `m0353-x-source`, `m0353-x-trust`, and
`m0353-x-provenance`; their full typed records live in `typed-graphs.json`.
