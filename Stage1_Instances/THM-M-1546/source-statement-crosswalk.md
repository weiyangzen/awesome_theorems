# Source-statement crosswalk

| Claim component | Source discovery anchor | Proposed formal component | Intake assessment |
|---|---|---|---|
| Higgs-bundle phase space and characteristic coefficients | N. J. Hitchin, “Stable bundles and integrable systems,” *Duke Mathematical Journal* 54(1) (1987), 91-114 | curve, rank, Higgs object, moduli/stable locus, and coefficient map | Primary source family located; exact theorem/page and all hypotheses are not yet accepted |
| Hitchin base and map | Same paper, characteristic polynomial/spectral-curve construction | `hitchinMap : HiggsModuli -> HitchinBase` with explicit coefficient spaces | `GL(n)` versus trace-free conventions and indexing require page-level crosswalk |
| Generic fiber via spectral curves | Same paper, spectral-curve/Jacobian analysis | regular-base predicate and an isomorphism/torsor statement for line-bundle data | Smoothness, degree shifts, open subsets, and Jacobian/Prym distinction must be pinned |
| Complete integrability | Same paper, integrable-system result | Poisson commutation, independence/half dimension, and generic abelian fiber | Exact definition and logical conjunction must be recovered, not inferred from the title |

Discovery identifier (not an immutable evidence receipt):

- DOI: <https://doi.org/10.1215/S0012-7094-87-05408-1>

The repository research row supplies only “Hitchin system,” year 1987, and “algebraic integrable
system.” It does not specify a theorem or hypotheses and its “verified” label is untrusted metadata.
`SRC-PINPOINT` must inspect the primary paper, record theorem/proposition and page numbers, reconcile
notation and group conventions, check errata, and obtain independent review. The exact-statement
phase must then mutation-test rank, genus, degree/stability, regular-locus, group, and generic-fiber
conditions. No row above establishes `H0` or Lean closure.
