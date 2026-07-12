# THM-M-0593 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 22 semantic obligations against the exact `Statement.lean` and bounded
`AA-0593-v1` anchor inventory. Eligibility follows the classical dimension split and Morse-Sard
rank/Taylor architecture, not the availability of Lean proofs. The three `X` nodes are explicit
formal-anchor, source, and provenance overlays and receive no mathematical machine-coverage credit.

## Typed proof route

```text
M0593-ROOT exact SardTarget [open M4]
`-- M0593-B-MERGE checked conditional dimension split
    |-- M0593-B-ZERO n = 0
    |-- M0593-B-LOWDIM m < n
    |   `-- M0593-L-DIMENSION-IMAGE [root cut]
    `-- M0593-B-HARD 0 < n and n <= m
        `-- M0593-T-LOCAL-GLOBAL
            |-- M0593-N-LOCAL countable local cover
            `-- M0593-T-HARD-LOCAL
                |-- M0593-C-RANK-STRATA
                |   `-- M0593-L-HIGHER-STRATA
                |-- M0593-L-RANK-REDUCTION [root cut]
                `-- M0593-L-NULL-LIMIT
                    `-- M0593-L-CUBE-COVER
                        `-- M0593-L-TAYLOR [root cut]
```

The proof graph stores reciprocal `proof_requires` and `composes` edges. Statement refinement,
provenance, evidence, trust, documentation, and workflow are separate graphs. Thus the narrower
equal-dimensional determinant theorem and Sard's paper cannot accidentally become exact proof
premises. Every leaf ledger is capped at 100 substantive steps; discovering a hidden theorem
package or longer proof requires a versioned split rather than silently enlarging a leaf.

## Node anchors

### M0593-ROOT
Exact `SardTarget`; consumes the exhaustive branch merger.

### M0593-S-DEFINITIONS
Freezes the derivative, nonsurjectivity, image, and volume predicates.

### M0593-S-DOMAINS
Freezes dimensions, total maps, open regions, and region-local smoothness.

### M0593-S-BOUNDARY
Accounts for empty and zero-dimensional cases.

### M0593-S-FOUNDATION
Owns the classical, quotient, measure-completion, and TCB audit.

### M0593-N-LOCAL
Reduces the open region to a countable bounded local cover.

### M0593-B-ZERO
Closes the `n = 0` branch when proved.

### M0593-B-LOWDIM
Owns the `m < n` whole-image nullity branch.

### M0593-B-HARD
Owns the `0 < n` and `n <= m` Morse-Sard branch.

### M0593-B-MERGE
Kernel-checked conditional merger of all dimension cases.

### M0593-L-DIMENSION-IMAGE
The missing higher-codimension image-nullity bridge.

### M0593-C-RANK-STRATA
Constructs an exhaustive rank and derivative-vanishing stratification.

### M0593-L-RANK-REDUCTION
The missing coordinate-straightening, slicing, and induction engine.

### M0593-L-HIGHER-STRATA
Separates successive derivative-vanishing strata.

### M0593-L-TAYLOR
The missing Taylor remainder image-diameter estimate.

### M0593-L-CUBE-COVER
Converts local Taylor bounds into outer-volume bounds.

### M0593-L-NULL-LIMIT
Passes arbitrary bounds and countable unions to measure zero.

### M0593-T-HARD-LOCAL
Composes the hard argument on one bounded local cube.

### M0593-T-LOCAL-GLOBAL
Reassembles local nullity on the arbitrary open region.

### M0593-X-EQUAL-DIM
Records the narrower pinned determinant-zero theorem without root credit.

### M0593-X-SOURCE
Maps mathematical engines to Sard 1942 Theorems 4.1 and 7.2.

### M0593-X-PROVENANCE
Owns terminal-body, revision, import, wrapper, and axiom provenance.

## Composition and status

`ObligationTree.lean` kernel-checks only the exhaustive merger: exact zero-codomain,
dimension-increasing, and hard-dimension branch hypotheses yield `SardTarget`. It does not assert
any branch hypothesis. The remaining root cut is the low-dimensional image-nullity bridge plus
the rank-reduction and Taylor engines in the hard branch. These have no exact audited proof bodies.
Consequently the root remains `[H1, M4, R4]`; audit completion, proof completion, `M0`, and theorem
completion are not claimed.
