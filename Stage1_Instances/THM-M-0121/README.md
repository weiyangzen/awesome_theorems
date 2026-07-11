# THM-M-0121 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the label "Mori rationality theorem". The
manifest's gloss, "rationality of Fano varieties", does not determine a true, unique theorem. This
intake therefore freezes the ambiguity rather than silently broadening or substituting the target.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Source identity | identify which published result the label denotes | no theorem/page was supplied by the source metadata |
| Exact root | retain the original label and gloss | no mathematical root is selected |
| Candidate A | MMP rationality theorem for a nef threshold | candidate only; would require characteristic, projectivity, singularity, divisor, and positivity data |
| Candidate B | rational curves or uniruledness of a Fano variety | candidate only; weaker than rationality of the variety |
| Candidate C | rational connectedness of a smooth projective Fano variety | candidate only; not birational rationality |
| Rejected reading | every Fano variety is a rational variety | not an admissible normalization; the unqualified claim is false |
| Legacy Lean file | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_040.lean` | discovery input only; its predicate-parametric shape is not an exact theorem statement |
| Foundations | Lean 4 kernel and pinned mathlib | profile and environment fingerprint remain open |

## Open task DAG

`SOURCE-ID` (obtain a primary-source theorem/page) -> `READING` (choose the exact claim) ->
`SCOPE` (freeze fields, characteristic, varieties/schemes, divisors and singularities) ->
`LEAN-TARGET` (elaborate a non-parametric expression) -> `TRANSPORTS` (check alternate encodings).

This is an intake task map, not the frozen proof-obligation registry required by the later
obligation-tree phase.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M4, R4]`. The first failed gate is exact
source identification. Consequently the exact-statement gate cannot begin. No source reading, Lean
declaration, proof, or theorem completion is claimed.

## Validation

The commands in `validation.md` establish manifest membership, repository-standard consistency,
JSON syntax, and dossier-local hygiene only.
