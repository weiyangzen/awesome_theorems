# Source-statement crosswalk

## Candidate primary sources

- Emilio Gagliardo, "Ulteriori proprieta di alcune classi di funzioni in piu variabili",
  *Ricerche di Matematica* 8 (1959), 24-51.
- Louis Nirenberg, "On elliptic partial differential equations", *Annali della Scuola Normale
  Superiore di Pisa*, series 3, 13(2) (1959), 115-162.

These bibliographic records are discovery anchors, not `H0` evidence. The statement phase must
inspect stable scans, select an exact numbered result and page, preserve the source's notation and
assumptions, and check corrections or later clarifications. No theorem/page anchor is inferred from
the family name.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| Gagliardo-Nirenberg inequality | one selected interpolation estimate, not the whole family | one canonical proposition plus checked transports only | family scoped; variant open |
| intermediate derivative | weak derivative of order `j` | multi-index derivative or Sobolev seminorm | encoding open |
| higher derivative | derivative order `m > j` | concrete weak-derivative membership and norm | encoding open |
| interpolation powers | factors with powers `a` and `1-a` | real extended norms/powers with boundary handling | exact type open |
| exponent relation | scaling constraint involving dimension and derivative orders | explicit equality and admissibility hypotheses | exact source constraints open |
| constant `C` | independent of `u`, dependent only on listed structural data | quantified positive finite constant | dependency list open |

## Fidelity boundary

The Chinese catalog title and its `已验证` metadata do not identify a theorem variant and cannot
support source fidelity. Before `H0`, an independent reviewer must verify the selected scan,
theorem/page, translation of every hypothesis, endpoint exceptions, constant dependencies, and
errata, then approve the source-to-Lean crosswalk. Before machine credit, the later anchor audit
must inspect the pinned mathlib revision and terminal proof provenance; this intake makes no claim
that a suitable Lean declaration exists.
