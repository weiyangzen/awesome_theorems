# THM-M-1181 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the metadata label "Caffarelli theorem"
(`Caffarelli定理`). Historical Stage1 files are discovery material only and contribute no accepted
statement or proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human label | "Caffarelli theorem: interior regularity of convex solutions" | This label does not uniquely select one published theorem |
| PDE family | Convex generalized solutions of the real Monge-Ampere equation, locally in a convex domain | Solution notion, dimension, normalization, and meaning of the Monge-Ampere measure remain to be fixed |
| Hypothesis family | Interior density bounds of the form `0 < lambda <= f <= Lambda`, with stronger regularity of `f` for stronger conclusions | Exact source assumptions and boundary separation are not yet frozen |
| Conclusion family | Strict convexity / interior `C^{1,alpha}`, `W^{2,p}`, or `C^{2,alpha}` regularity | These are distinct Caffarelli results and must not be conflated |
| Formal target | A future Lean 4 proposition over finite-dimensional real Euclidean space | No exact declaration or elaborated expression is credited at intake |
| Proof architecture | sections and affine normalization; localization/strict convexity; measure estimates; iteration; regularity upgrade | Architecture only; no obligation or proof closure is claimed |
| Foundations | Lean 4 kernel plus pinned mathlib analysis, measure, convexity, and finite-dimensional APIs | Exact toolchain, imports, axioms, and dependency closure remain open |

The terse repository source says only `凸解的内部正则性` (interior regularity of convex
solutions). It is compatible with several non-equivalent theorems. Therefore this intake preserves
the full candidate family and explicitly forbids silently choosing the easiest member. The dependent
statement phase must resolve the source identity from a primary theorem/page before elaboration.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed gate is exact
source-statement identification: the metadata does not determine the hypotheses or the regularity
conclusion. The theorem is not complete. See `source_statement_crosswalk.md` for the candidate
primary sources and the decision required next.

## Validation

The commands and exact outcomes in `validation.md` establish manifest membership, standard
consistency, JSON syntax, and dossier-local integrity only. No Lean declaration was added and no
kernel result is claimed.
