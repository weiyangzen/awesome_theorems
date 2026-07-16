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

The current statement execution rechecked the repository source row at
`Docs/researches/math_theorems.md`: it contains no citation or mathematical detail beyond the title,
authors, year, and one-line gloss. Nothing in that row selects one candidate below. Network access
is denied in the worker lane, and the repo contains no immutable scan of any candidate source, so
this phase cannot promote a discovery citation into a source-faithful canonical claim.

## Crosswalk

| Metadata component | Candidate source meaning | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "Mazur-Tate theorem" | height/refined BSD result or abbreviated MTT exceptional-zero result | materially different objects and binders | unresolved |
| "p-adic L-function of an elliptic curve" | interpolation theorem or exceptional leading term | must freeze normalization, periods, Euler factors, and reduction type | unresolved |
| no prime/reduction hypotheses | ordinary, good, or split multiplicative cases not distinguished | no exact domain or hypotheses can be frozen | blocking |
| source status `已验证` | untrusted catalog metadata | cannot identify a declaration or terminal proof body | no credit |

## Exact premise and boundary obligations

| Candidate | Premises that must be fixed before encoding | Conclusion that must be fixed | Boundary choices still unresolved |
|---|---|---|---|
| p-adic L-function interpolation | curve domain and model, prime, reduction type, character family, conductors, periods, Euler factors, coefficient fields and embeddings | the complete specialization/interpolation equality with its quantifier range | trivial character, conductor one, bad primes, vanishing Euler factors, sign and period conventions |
| exceptional-zero formula | all interpolation data plus split multiplicative reduction, Tate period and logarithm convention, L-invariant, analytic parameter and derivative order | exact leading-term or derivative equality | simple versus higher-order zero, logarithm normalization, period and Euler-factor normalization |
| Mazur-Tate elements/refined BSD | finite abelian extensions, group rings, augmentation filtration, modular-symbol normalization and specialization maps | exact congruence, divisibility, leading term, or conjectural equality selected by the source | trivial extension, augmentation order, torsion and sign conventions, theorem versus conjecture status |

The three rows are not interchangeable encodings. No checked transport can be authored until one
row and one exact source statement are selected. The current `Statement.lean` therefore probes only
adjacent pinned interfaces and contains no canonical declaration.

Before H0, a reviewer must inspect stable copies, identify the exact proved theorem (not a
conjecture), record edition/pages and definitions, check errata and later proof attribution, and map
every ordered hypothesis and conclusion to the canonical claim. A separate anchor audit must then
search pinned Lean 4 sources; this intake makes no claim that the required elliptic-curve p-adic
L-function objects currently exist in mathlib.
