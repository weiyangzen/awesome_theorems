# THM-M-0005 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Kunneth formula. The historical label
`已验证` is untrusted intake metadata and grants no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | PID-coefficient Kunneth natural short exact sequence for singular homology of a product | The blueprint only says "homology groups of product spaces"; the precise Lean object model is not yet elaborated |
| Algebraic layer | tensor product of chain complexes, graded tensor sum, `Tor₁`, exactness, splitting | No mathlib declaration or terminal body has been audited |
| Topological bridge | singular chains of `X × Y` compared with the tensor product of singular chains | Eilenberg-Zilber data is a distinct root-critical obligation, not an implicit rewrite |
| Naturality | maps induced by maps of both spaces and the naturality square for the sequence | Diagram orientation and categorical encoding remain open |
| Specialization | field coefficients, where the Tor term vanishes | A simpler field theorem cannot replace the PID root |
| Foundations | Lean 4 kernel and a versioned classical/choice/quotient policy | Toolchain, imports, axioms, and dependency fingerprint remain open |

The scope deliberately retains the Tor term and the topological comparison. It does not broaden the
claim to arbitrary rings or silently weaken it to field coefficients. The provisional wording in
`intake.json` must be replaced by an exact elaborated expression in the dependent statement phase.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Only `INTAKE` is addressed here. No downstream node or receipt is accepted.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact-statement gate: coefficients, hypotheses, grading conventions, Lean declarations,
normalized expression hash, checked transports, and environment fingerprint are not yet frozen.
The theorem is not complete.

## Validation

The exact commands and outcomes establishing manifest membership, repository-standard consistency,
JSON syntax, dossier reference integrity, and clean patch formatting are recorded in `validation.md`.
