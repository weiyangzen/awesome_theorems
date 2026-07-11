# THM-M-0004 rev-5.6 intake

This is the `planned` dossier for the universal coefficient theorem. The repository source says
only "the relation between homology groups and tensor products/Hom groups." That wording does not
select one of the distinct homological tensor/Tor and cohomological Hom/Ext universal coefficient
theorems. This intake therefore freezes the shared theorem family and records the ambiguity; the
dependent statement phase must select an exact root from a pinned primary source before elaboration.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Ambient algebra | Chain complexes and coefficients over a ring, with hypotheses sufficient for the selected UCT | Ring handedness, projectivity/freeness, grading, and universes remain open |
| Homological branch | A natural short exact sequence with tensor and `Tor` terms | Exact indices, comparison maps, and splitting claim are not frozen |
| Cohomological branch | A natural short exact sequence with `Hom` and `Ext` terms | This may be the intended root or a related sibling; source audit must decide |
| Formal candidate | Category-level package using homology, short exact complexes, tensor/`Tor`, and `Hom`/`Ext` | Legacy `StatementShape` is discovery input only and is intentionally more abstract than a terminal theorem |
| Naturality | Naturality of the comparison sequence | Required if present in the selected source statement; no witness is credited here |
| Excluded readings | Kunneth formula, arbitrary long exact sequences, and a bare existence package with unconstrained output terms | None may substitute for an exact UCT statement |

The structured claim boundary is in `intake.json`; the source and formal-candidate mapping is in
`source_statement_crosswalk.md`.

## Open phase DAG

`STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
All nodes remain open. Intake creates no proof credit and does not inherit assurance from the
historical `S1_M_099.lean` file or the untrusted source label `已验证`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M3, R3]`. The first failed gate is source
and exact-statement selection: no primary-source theorem/page, unique branch, normalized Lean type,
expression hash, or environment fingerprint is accepted. The theorem is not complete.

