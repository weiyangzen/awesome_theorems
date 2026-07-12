# THM-M-0729 frozen obligation architecture

Item `S56-M-0729-OBLIGATION_TREE` freezes registry version 1 against the exact
`Statement.lean` and `anchor-audit.json` hashes in `obligation-registry.json`.
The 19 semantic IDs are the denominator for later coverage. Any split, merge,
exclusion, or eligibility change requires a versioned append-only delta.

## Proof route

The root is split into the two directions of the frozen class equality. The
NP-to-PCP direction owns the verifier-to-constraint normalization, robust gap
theorem, PCP composition, logarithmic-randomness and constant-query accounting,
perfect-completeness construction, and exact soundness-one-half transport. The
PCP-to-NP direction separately owns finite proof-bit certificates, exhaustive
random-string verification with its polynomial cost proof, and the finite
below-threshold input branch. Boundary and encoding obligations are shared but
receive no duplicate proof credit.

The proof graph has reciprocal `proof_requires` and `composes` edges. Separate
refinement, provenance, evidence, trust, documentation, and workflow graphs
prevent citations, receipts, or workflow state from becoming proof premises.
Every node has a substantive ledger and a step budget no greater than 100.

## Checked boundary

`ObligationTree.lean` defines a directional package and kernel-checks its
assembly through `ExpandedTarget` to the exact `PCPTheorem`. The two inclusions
are assumptions to that composition theorem, not proved children. This gives
the assembly obligation local evidence only and no root proof credit.

The first open cut is both directional packages, the primary-source node map,
and the foundation audit. The root remains `M3`; H remains `H3`, readability
remains `R4`, and theorem completion is false.
