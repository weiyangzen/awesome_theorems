# THM-M-1158 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the target named "single-layer
potential" (`单层位势`). The upstream metadata supplies only the phrase "boundary
integral representation" (`边界积分表示`), not a quantified theorem. This intake
therefore freezes that ambiguity rather than silently choosing one of several standard
results about single-layer potentials.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Source claim | The exact Stage0 wording: single-layer potential / boundary integral representation | No formula, dimension, kernel normalization, boundary regularity, density space, or asserted property is supplied |
| Mathematical object | A boundary integral formed from a fundamental solution and a boundary density | This is a discovery description, not a frozen theorem statement |
| Candidate assertions | Definition/representation, harmonicity off the boundary, trace continuity, normal-derivative jump relations | Mutually non-equivalent possibilities; none is selected or credited |
| Domains | Euclidean domains and their boundaries are suggested by the title/category | Ambient dimension, scalar field, boundary measure, and regularity remain open |
| Lean surface | Lean 4 with pinned mathlib | No declaration or exact expression is claimed before source disambiguation |
| Foundations | Lean 4 kernel with a later accepted classical/choice/quotient policy | Toolchain, imports, TCB closure, and computation profile remain open |

The next statement phase is blocked until an authoritative source identifies the exact
assertion and assumptions. It must not broaden the metadata into a theorem about all
single-layer potentials or substitute a convenient library theorem.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R3]`. The first failed gate
is exact source-statement identification. No proof, Lean elaboration, historical
"verified" label, or theorem-completion credit is accepted.

## Validation

The commands and results in `validation.md` establish target membership, repository
standard consistency, JSON syntax, and dossier-local integrity only.
