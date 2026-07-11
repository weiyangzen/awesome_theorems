# Source-statement crosswalk

## Repository source

`Docs/Stage0_Blueprint.md` names `THM-M-0151` as "Hacon theorem", gives the gloss "pluricanonical
maps of varieties of general type", the year 2007, and Christopher Hacon as source. These metadata
are untrusted discovery input: they contain no theorem number, page, bibliography, hypotheses, or
quantifiers and do not support `H0`.

## Primary-source candidates requiring inspection

- Christopher D. Hacon, "Boundedness of pluricanonical maps of varieties of general type",
  *Inventiones Mathematicae* 166 (2006), 1-25. This title is the closest match to the repository
  gloss, but its exact theorem wording, pages, corrections, and relationship to the recorded year
  must be checked from the publication.
- Christopher D. Hacon and James McKernan, "Boundedness of pluricanonical maps of varieties of
  general type", *Inventiones Mathematicae* 166 (2006), 1-25, is a possible bibliographic
  attribution variant to resolve against the actual publication record rather than guess here.
- Later Hacon-McKernan/Takayama/Tsuji uniform birationality results may be what the 2007 metadata
  intended. They are comparison candidates only and cannot be substituted without provenance.

These are discovery anchors, not verified citations. The statement phase must consult the actual
paper and errata and record immutable edition metadata, theorem number, page, and verbatim logical
shape. The deliberately visible attribution uncertainty is preferable to fabricated source detail.

## Crosswalk

| Repository phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| varieties of general type | smooth projective `n`-fold with big canonical class | concrete variety, canonical sheaf/divisor, bigness | included; definitions open |
| pluricanonical map | rational map from sections of `rK_X` | complete linear system and associated rational map | included; API open |
| boundedness | integer depending only on dimension | ordered existential/universal binders | included; quantifiers open |
| theorem conclusion | birationality onto the image | concrete birational-map predicate | provisional; source check required |
| Hacon / 2007 | attribution and date | provenance only, never a Lean hypothesis | unresolved metadata conflict |

Before `H0`, an independent reviewer must verify the chosen primary theorem, all assumptions,
quantifiers, definitions, errata, and every source-to-Lean row. Before machine credit, a canonical
Lean expression must elaborate without `sorry`, axioms introduced for the result, or abstract
packages containing the conclusion.

