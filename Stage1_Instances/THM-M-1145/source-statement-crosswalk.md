# Source-statement crosswalk

| Source field | Available wording | Exact-target consequence |
|---|---|---|
| Name | Cauchy estimates | Names a family, not a unique proposition. |
| Content | Derivative estimates for holomorphic functions | Requires holomorphy and a derivative bound, but fixes neither encoding. |
| Proposer/time | Augustin Cauchy, 1831 | Historical metadata only; not theorem-level evidence. |
| Domain | Not stated | Disk, closed disk neighborhood, and general-domain readings remain open. |
| Function/codomain | Not stated beyond holomorphic | Complex scalar and Banach-valued variants cannot be conflated. |
| Quantifiers | Not stated | Center, radius, derivative order, and bound constant remain open. |
| Hypotheses | Not stated | Boundary continuity, neighborhood holomorphy, and supremum assumptions remain open. |
| Conclusion | "derivative estimates" | Exact norm, factorial, radius power, and inequality direction are not sourced. |
| Degenerate cases | Not stated | `R = 0`, `n = 0`, and empty-domain behavior must be explicitly settled. |

Repository evidence is `Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md`; both carry
the same short secondary description. Neither supplies a primary citation or exact formula. Thus an
exact Lean declaration is deliberately deferred to `S56-M-1145-STATEMENT` and remains M4 here.
