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

The statement node selects Nirenberg's Lecture II theorem on page 125, formulae (2.2)--(2.3), in
the stable NUMDAM scan. Its SHA-256 is
`cd76d6de19f77a7f27d44909c2c00cafbb5fb165a6587b4ff8d86dd13ff7eb3e`. The scan explicitly gives
the exponent equation, `j/m <= a <= 1`, dependence of the constant, and two exceptional cases.
This pinpoint selection does not itself close the later source-fidelity or errata review gate.

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| Gagliardo-Nirenberg inequality | Nirenberg 1959, Lecture II theorem, p. 125, (2.2)--(2.3) | `GagliardoNirenbergTarget` | selected and elaborated |
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
