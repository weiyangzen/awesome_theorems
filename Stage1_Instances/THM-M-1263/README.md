# THM-M-1263 rev-5.6 intake

This directory is the `planned` intake for **Propagation of singularities** (`奇性传播`). The
metadata supplies only “wavefront sets and propagation of singularities”; it does not identify a
unique theorem. Accordingly, the standard real-principal-type propagation theorem is a provisional
scope, not a silently invented exact target.

## Scope map

| Surface | Provisional in-scope content | Intake boundary |
|---|---|---|
| Root phenomenon | propagation of `WF(u)` along Hamilton bicharacteristics of a real principal symbol, away from `WF(Pu)` | exact source theorem and local/global formulation are open |
| Analytic objects | smooth manifold, distribution, classical pseudodifferential operator, principal symbol | scalar/bundle setting, orders, support assumptions, and wavefront convention are open |
| Geometric layer | cotangent bundle without zero section, characteristic set, Hamilton vector field and maximal integral curves | no Lean representation has been selected |
| Regularity layer | ordinary wavefront set; Sobolev wavefront propagation is an alternate candidate | equivalence/corollary transports are unchecked |
| Boundary cases | elliptic points, stationary Hamilton field, forcing singularities, radial/boundary variants | exclusions must be matched to the selected source |
| Formal layer | Lean 4 plus pinned mathlib | no declaration, imports, elaboration, or environment fingerprint exists |

The statement phase must first disambiguate a pinpointed primary-source theorem. It must not encode
the informal slogan as the weaker assertion that an arbitrary set is invariant under an arbitrary
flow, nor replace pseudodifferential propagation by elliptic regularity.

## Open task DAG

1. `S56-M-1263-STATEMENT`: select and transcribe an exact primary-source formulation; freeze all
   binders, symbol/order conventions, wavefront definitions, and boundary cases; then elaborate it.
2. `S56-M-1263-ANCHOR_AUDIT`: inventory pinned mathlib and external Lean candidates without treating
   definitions or nearby microlocal lemmas as proof closure.
3. `S56-M-1263-OBLIGATION_TREE`: freeze typed analytic, geometric, propagation, provenance, trust,
   documentation, and workflow obligations.
4. `S56-M-1263-PROOF`: implement or pin/import exact proof bodies only after the preceding gates.
5. `S56-M-1263-VALIDATION`: run exact-type, kernel, axiom, provenance, hermetic, and independent checks.
6. `S56-M-1263-RELEASE`: reconcile accepted evidence and decide theorem completion separately from audit completion.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. `H2` records that credible
source families are identified but not yet pinned and premise-mapped. `M4` records that the source
label is too broad to yield a unique canonical Lean proposition. The first failed theorem gate is
exact-statement identification. No historical “verified” label or source discovery receives proof
credit, and the theorem is not complete.

## Validation

The exact commands and results for this intake are in `validation.md`. They establish target
membership, repository structural consistency, JSON syntax, and dossier-local integrity only.
