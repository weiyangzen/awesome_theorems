# THM-M-1274 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the metadata label
"Ljusternik-Schnirelmann theory". The repository source supplies only the gloss "topological
index and critical points"; it does not identify one theorem, a category convention, or analytic
hypotheses. Accordingly this intake freezes the available scope without inventing an exact claim.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Source label | Ljusternik-Schnirelmann theory, attributed to Lazar Ljusternik and Lev Schnirelmann (1930) | The metadata label is not itself a proposition |
| Candidate root family | Lower bounds on critical points/critical values in terms of an LS category or related index | Selection of a particular theorem is open |
| Topological inputs | A space or manifold and a precisely chosen normalized or unnormalized category invariant | Category convention and regularity assumptions are open |
| Analytic inputs | A function or functional, compactness condition, and critical-point notion | Finite-dimensional smooth and infinite-dimensional variational versions are not interchangeable |
| Candidate conclusion | A lower bound on distinct critical points or critical values | Bound (`cat`, `cat + 1`, or cup-length-derived) depends on conventions and hypotheses |
| Formal system | Lean 4 plus pinned mathlib | No canonical Lean declaration or expression is credited at intake |

The later statement phase must obtain a source pinpoint that uniquely fixes the space class,
category normalization, function/functional regularity, compactness assumptions, critical-point
notion, and exact inequality. Until then it must not silently substitute the commonly quoted closed
manifold theorem for the broader source label.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R4]`. The first failed gate is exact
source-statement identification. The manifest's untrusted `已验证` label supplies no proof credit,
and no theorem completion is claimed.

## Validation

The commands and results in `validation.md` establish manifest membership, rev-5.6 structural
consistency, JSON syntax, and dossier hygiene only. There is no Lean target to elaborate in this
intake phase.
