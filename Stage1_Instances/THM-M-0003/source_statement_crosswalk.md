# Source-statement crosswalk

| Claim component | Human-source discovery anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Morphism of short exact sequences | H. Cartan and S. Eilenberg, *Homological Algebra* (Princeton University Press, 1956), the classical exact-sequence material | fields of `ShortComplex.SnakeInput C` | Primary-era book identified, but theorem/page and premise-level mapping are not yet verified |
| Connecting morphism | Same source family; modern naming is the snake lemma | `ShortComplex.SnakeInput.δ` | Candidate object only; construction and sign convention unaudited |
| Exact kernel/cokernel sequence | Classical snake-lemma conclusion | `ShortComplex.SnakeInput.snake_lemma`, proposed result `S.composableArrows.Exact` | Candidate is aligned at synopsis level; exact type inspection is deferred |
| Naturality | Standard functorial refinement of the construction | `ShortComplex.SnakeInput.naturality_δ` | Supporting branch, not part of the minimally frozen root |
| Module specialization | Elementwise module formulation | `Mathlib.Algebra.Module.SnakeLemma` declarations | Alternate encoding only; equivalence with the category root is unproved here |

The repository discovery source, `Docs/researches/math_theorems.md`, supplies only the name, a
1950s date, and the wording "short exact sequences induce a long exact sequence." That wording does
not specify the diagram, connecting morphism, six terms, or ambient category, so it is not adequate
for `H0` and must not be used to broaden the theorem into the derived-functor long exact sequence.

The Cartan-Eilenberg bibliographic anchor is a source lead, not an accepted citation receipt. The
source audit must pin an edition or scan hash, locate exact pages/theorem, map every assumption and
term, check errata and sign conventions, and obtain independent review. Accordingly this dossier
claims `H2`, not source closure.

Lean names above were discovered in the legacy local module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_098.lean`. That file is explicitly unaccepted under
the uniform rev-5.6 L0 baseline. The statement phase must inspect the pinned mathlib source and
serialize the elaborated declaration before any machine credit is possible.
