# THM-M-0005 rev-5.6 statement

This directory is the rev-5.6 `planned` instance for the Kunneth formula. The exact PID target is
`AwesomeTheorems.Stage1.THM_M_0005.KunnethFormula` in `KunnethStatement.lean`. It elaborates with
the pinned toolchain and a narrow set of direct imports. The historical label `已验证` remains
untrusted metadata and grants no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | PID-coefficient Kunneth natural short exact sequence for singular homology of a product | Elaborated as a nonempty structure of short exact sequences and naturality/component equations |
| Algebraic layer | tensor product of chain complexes, graded tensor sum, `Tor₁`, exactness, splitting | No mathlib declaration or terminal body has been audited |
| Topological bridge | singular chains of `X × Y` compared with the tensor product of singular chains | Eilenberg-Zilber data is a distinct root-critical obligation, not an implicit rewrite |
| Naturality | maps induced by maps of both spaces and the naturality square for the sequence | Diagram orientation and categorical encoding remain open |
| Specialization | field coefficients, where the Tor term vanishes | A simpler field theorem cannot replace the PID root |
| Foundations | Lean 4 kernel and pinned mathlib | Lean v4.29.0 and mathlib `8a178386`; broader trust audit remains downstream |

The scope deliberately retains the Tor term and the topological product. It does not broaden the
claim to arbitrary rings or silently weaken it to field coefficients. No connectedness, nonempty,
or finite-type hypothesis is introduced, and no noncanonical splitting is asserted.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
`STATEMENT` is addressed provisionally here. No downstream node or receipt is accepted.

The version-1 proof architecture is frozen in `obligation-registry.json`, `typed-graphs.json`, and
`obligation-tree.md`. It records 18 canonical obligations and assigns no proof-closure credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The exact expression and
environment are frozen, but no term inhabiting `NaturalKunnethSequence` is supplied. The first
failed theorem gate is therefore proof closure. Source audit, obligation-tree, trust, provenance,
hermetic replay, readability, and independent acceptance gates also remain open. The theorem is
not complete.

## Validation

The exact commands and outcomes establishing manifest membership, repository-standard consistency,
JSON syntax, dossier reference integrity, and clean patch formatting are recorded in `validation.md`.
