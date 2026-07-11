# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names "Sobolev inequality", attributes it to Sergei Sobolev in
1938, and describes it only as "Sobolev embedding in norm form". Its `已验证` label is untrusted
metadata and does not specify hypotheses, endpoints, or a source theorem.

## Candidate primary sources

- S. L. Sobolev, "On a theorem of functional analysis", *Mat. Sbornik* 4 (46) (1938), 471-497
  (Russian). This is the historical primary-paper candidate. The exact proposition/page,
  translation, assumptions, and errata have not yet been inspected.
- E. Gagliardo, "Proprieta di alcune classi di funzioni in piu variabili", *Ricerche di
  Matematica* 7 (1958), 102-137, and L. Nirenberg, "On elliptic partial differential equations",
  *Annali della Scuola Normale Superiore di Pisa* 13 (1959), 115-162, are candidate primary
  anchors for the commonly formalized Gagliardo-Nirenberg-Sobolev form. Their exact theorem rows
  and relation to the repository's intended attribution require inspection.

These citations are discovery anchors, not `H0` evidence.

## Crosswalk

| Repository phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| Sobolev inequality | first-order Euclidean norm estimate | measurable function and derivative/gradient | included; encoding open |
| embedding in norm form | `L^p` derivative control implies `L^q` control | `MemLp`/`eLpNorm` or equivalent normed spaces | included; transport open |
| Sobolev conjugate | `1/q = 1/p - 1/n` | exact exponent relation and side conditions | included; endpoints open |
| compact support | removes lower-order term on all of Euclidean space | compact-support predicate | provisional pending source |
| constant | depends only on permitted parameters | existential or explicit nonnegative constant | normalization open |

## Existing Lean boundary

Repository search finds the pinned mathlib module
`Mathlib.Analysis.FunctionalSpaces.SobolevInequality`, referenced by historical Stage1 modules.
This is only an anchor candidate at intake: its exact declarations, types, transitive proof bodies,
axioms, toolchain revision, and correspondence to the selected source have not been audited. It
therefore supplies no M-state proof credit here.

Before `H0`, an independent reviewer must verify a stable source edition, theorem/page, all
assumptions and definitions, translations and errata, then approve the source-to-Lean crosswalk.
