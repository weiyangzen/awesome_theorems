# THM-M-0140 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Kazhdan-Lusztig basis theorem. Historical
Stage1 files are discovery inputs only and provide no accepted statement or proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | existence and uniqueness of the Kazhdan-Lusztig canonical basis of the Hecke algebra of a Coxeter system | Coefficient and normalization conventions must be frozen in the statement phase |
| Coxeter layer | Coxeter system, length, Bruhat order, and intervals | Pinned mathlib has partial Coxeter infrastructure; exact imports remain unaudited |
| Hecke layer | generic one-parameter Hecke algebra, standard basis, multiplication, and bar involution | No concrete repo-local Hecke model is credited |
| Basis characterization | bar invariance plus triangularity/normalization relative to the standard basis | Existence, uniqueness, and equivalence of common `C_w`/`C'_w` conventions remain open |
| Consequences | Kazhdan-Lusztig polynomials and transition coefficients | Consequences are downstream, not substitutes for the root theorem |
| Foundations | Lean 4 kernel with versioned classical/choice/quotient and computation policies | Exact TCB and environment fingerprint remain open |

The canonical human claim, provisional target boundary, domains, and exclusions are structured in
`intake.json`. Source genealogy and the source-to-statement gaps are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact statement gate: there is no accepted concrete Hecke algebra encoding, normalized Lean
expression hash, environment fingerprint, checked convention transport, or mutation suite. This
intake is self-tested as an intake artifact only. It does not establish theorem completion.

## Validation

The commands in `validation.md` establish target membership, standard consistency, JSON syntax,
dossier reference integrity, and absence of forbidden proof devices in the owned artifacts. No Lean
declaration is introduced by this phase and no kernel closure is claimed.
