# Source-statement crosswalk

## Candidate primary sources

- B. Mazur and J. Tate, "Canonical height pairings via biextensions", in *Arithmetic and
  Geometry*, Vol. I, Progress in Mathematics 35, Birkhauser, 1983, pp. 195-237. This is a primary
  Mazur-Tate source relevant to p-adic height and refined arithmetic statements, but the repository
  gloss does not establish that one of its results is intended.
- B. Mazur, J. Tate, and J. Teitelbaum, "On p-adic analogues of the conjectures of Birch and
  Swinnerton-Dyer", *Inventiones Mathematicae* 84 (1986), 1-48, DOI
  `10.1007/BF01388731`. This is the primary source for the exceptional-zero conjectural formula;
  exact theorem/conjecture labels and the later proof source must be inspected.
- B. Mazur and J. Tate, "Refined conjectures of the Birch and Swinnerton-Dyer type", *Duke
  Mathematical Journal* 54 (1987), 711-750, DOI `10.1215/S0012-7094-87-05437-8`. This is a primary
  source for Mazur-Tate elements/refined conjectures, not automatically a proved theorem.

These are discovery anchors only. Exact pages, statements, errata, and proof status have not been
verified, so they provide neither H0 nor machine-proof credit.

## Crosswalk

| Metadata component | Candidate source meaning | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "Mazur-Tate theorem" | height/refined BSD result or abbreviated MTT exceptional-zero result | materially different objects and binders | unresolved |
| "p-adic L-function of an elliptic curve" | interpolation theorem or exceptional leading term | must freeze normalization, periods, Euler factors, and reduction type | unresolved |
| no prime/reduction hypotheses | ordinary, good, or split multiplicative cases not distinguished | no exact domain or hypotheses can be frozen | blocking |
| source status `已验证` | untrusted catalog metadata | cannot identify a declaration or terminal proof body | no credit |

Before H0, a reviewer must inspect stable copies, identify the exact proved theorem (not a
conjecture), record edition/pages and definitions, check errata and later proof attribution, and map
every ordered hypothesis and conclusion to the canonical claim. A separate anchor audit must then
search pinned Lean 4 sources; this intake makes no claim that the required elliptic-curve p-adic
L-function objects currently exist in mathlib.
