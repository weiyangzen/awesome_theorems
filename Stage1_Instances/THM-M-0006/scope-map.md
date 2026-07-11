# Scope map

| Surface | Candidate scope | Intake boundary |
|---|---|---|
| Human root | existence of left and right derived functors | Source does not state categorical hypotheses or meaning of existence |
| Degreewise branch | additive `F : C ⥤ D`, abelian categories, projective/injective resolutions, functors `F.leftDerived n` and `F.rightDerived n` | Legacy checked wrapper is discovery input, not the frozen root |
| Total branch | left/right Kan extensions along a localization | Distinct mathematical construction; cannot be silently substituted for the degreewise claim |
| Acyclic branch | higher derived functors vanish on projective/injective objects | Possible consequence, not present in the one-line source |
| Degree zero | comparison with the original functor under finite (co)limit preservation | Possible consequence; extra hypotheses required |
| Functoriality | natural transformations induce maps and naturality squares | Inclusion in the named theorem is unresolved |
| Exactness | connecting morphisms and long exact sequences | Inclusion and exact hypotheses are unresolved |
| Foundations | Lean 4 kernel and pinned mathlib category theory | Exact toolchain, imports, axioms, and environment fingerprint belong to later phases |

Excluded from intake credit are the mere definability of a chosen functor, any assumption-free
universal existence claim, and aggregation of separate branch wrappers into a terminal theorem.
Degenerate categories and zero functors must be checked after binders and hypotheses are frozen.
