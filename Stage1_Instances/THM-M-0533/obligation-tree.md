# THM-M-0533 obligation tree

Registry version 1 freezes the classical small-chain proof route before proof
closure is observed. The 19 stable obligation IDs and their complete semantic
ledgers are authoritative in `obligation-registry.json` and
`typed-graphs.json`; this document is the readable projection.

## M0533-ROOT

The exact target is `AwesomeTheorems.THM_M_0533.MayerVietorisSequence`: for
every two-open cover, ordinary integral singular homology has the signed long
exact sequence and explicit degree-zero endpoint frozen in `Statement.lean`.

## Statement and trust nodes

- `M0533-S-DEFINITIONS` freezes coefficients, open subspaces, inclusion maps,
  the `(i_*,-j_*)` sign, and natural indexing.
- `M0533-S-BOUNDARY` preserves arbitrary spaces, empty intersections, degree
  zero, and exactness of the final map to the zero group.
- `M0533-S-FOUNDATION` requires the transitive axiom, import, TCB,
  noncomputability, and no-oracle audit.

## Chain construction

- `M0533-C-SUBDIVISION` constructs barycentric subdivision and a chain
  homotopy making singular chains subordinate to the cover.
- `M0533-L-SMALL-QUASIISO` proves cover-small chains compute the same homology.
- `M0533-C-CHAIN-SES` and `M0533-L-CHAIN-KERNEL` construct and prove exact the
  signed chain-complex sequence for intersection, biproduct, and union.
- `M0533-C-BOUNDARY` derives connecting homomorphisms in homology.
- `M0533-L-NATURALITY` identifies the derived maps with exactly `firstMap` and
  `secondMap`, including the sign convention.

## Exactness and assembly

- `M0533-T-CONSTRUCTION` packages boundary maps and zero-composite laws.
- `M0533-T-EXACT-INTER`, `M0533-T-EXACT-BIPROD`, and
  `M0533-T-EXACT-SPACE` close the three recurring exactness positions.
- `M0533-T-DEGREE-ZERO` closes the separate `H_0(X) -> 0` endpoint.
- `M0533-T-EXACTNESS` combines these into `ExactnessPackage`.
- `M0533-T-ASSEMBLE` is the only checked proof composition. In
  `ObligationTree.lean`, it consumes the two open packages as explicit
  hypotheses and returns the exact root. It supplies no proof of either input.

`M0533-X-SOURCE` owns primary-source coverage. `M0533-X-PROVENANCE` owns
terminal-body, import, trust, placeholder, and replay evidence. Neither is a
substitute for mathematical proof.

Every node has a four-step semantic ledger, below the 100-step split threshold.
The root remains open at `M3`. No H0, M0 root, R0, audit completion, accepted
receipt, or theorem completion is claimed.
