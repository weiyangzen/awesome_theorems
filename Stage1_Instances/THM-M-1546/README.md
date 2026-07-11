# THM-M-1546 rev-5.6 intake

This is a `planned` dossier for the Hitchin system. The repository's source phrase, “algebraic
integrable system,” is not itself a theorem: it omits the group, curve, moduli space, stability
locus, Hitchin base, and meaning of generic fiber. This intake conservatively selects the classical
complex `GL(n)` spectral-curve formulation as the statement family. The statement phase must fix
the exact variant from the primary source before any Lean expression receives proof credit.

## Scope map

| Surface | Included at intake | Boundary / open work |
|---|---|---|
| Ground data | Smooth projective complex curve and rank `n` | Genus, degree, stability, and coprimality assumptions require source pinpointing |
| Phase space | Stable Higgs bundles, or the appropriate open cotangent-moduli locus | Stack/coarse-moduli conventions and exceptional loci remain open |
| Map | Characteristic coefficients of the Higgs field into the Hitchin base | Indexing and trace-free versus `GL(n)` conventions must not be mixed |
| Fibers | Smooth spectral-curve locus; generic fiber described by line bundles/Jacobian data | Compactified Jacobians and singular spectral curves excluded initially |
| Integrability | Commuting Hamiltonians plus the half-dimension/generic abelian-fiber package | Exact algebraic-symplectic definition must be frozen in Lean |
| Formal system | Lean 4 and pinned mathlib | Object model, imports, toolchain, and environment fingerprint remain open |

The existing legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_205.lean` is discovery
input only. Its `HitchinSystemData` stores major conclusions as proposition fields, so projection
wrappers are not a proof of Hitchin's theorem and receive no machine-proof credit.

## Open task DAG

`STMT-VARIANT` selects one primary-source theorem and fixes `GL(n)` conventions. `STMT-GEOMETRY`
freezes curve, Higgs-moduli, stability, and spectral-curve data. `STMT-MAP` defines the Hitchin map
and regular base. `STMT-INTEGRABILITY` fixes the exact commuting, dimension, and fiber conclusion.
`STMT-EXACT` elaborates and mutation-tests the target. Source pinpointing and immutable Lean-anchor
audit follow that accepted statement. This intake DAG is workflow planning, not a proof-obligation
registry.

The provisional root vector is `[H2, M4, R4]`. The first failed theorem gate is exact statement:
no accepted source theorem/page crosswalk, canonical Lean declaration, expression hash, checked
transport, or environment fingerprint exists. Neither audit nor theorem completion is claimed.
