# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Catalogue claim: "low regularity for dispersive equations" | `Docs/researches/math_theorems.md`, THM-M-1216 record | none | Too broad to identify a unique mathematical proposition |
| Selected real-line KdV reading | C. E. Kenig, G. Ponce, L. Vega, *A bilinear estimate with applications to the KdV equation*, Journal of the American Mathematical Society 9 (1996), 573-603 | future concrete KdV target | Named primary-source candidate; theorem number, page, assumptions, and corrections are not yet audited, so this is `H1`, not `H0` |
| Candidate regularity range `s > -3/4` | Reported by the legacy discovery artifact as the selected reading of the 1996 paper | `selectedRegularityThreshold` and `SelectedRegularity` in legacy `S1_M_154` | Discovery input only; endpoint and exact source wording must be checked before freezing |
| Local well-posedness package | Same candidate paper | legacy `LocalWellPosedData` and `FrozenVariantStatement` | Abstract proposition-valued estimate fields do not encode the PDE, Sobolev space, or Bourgain space; no equivalence is established |
| Analytic proof boundary | Airy linear theory, Bourgain restriction-space estimates, KdV bilinear estimate, fixed point, Sobolev trace | no accepted terminal declaration | Scope map only; later obligation-tree and proof phases own decomposition and closure |

The selected paper is a plausible disambiguation of the catalogue entry, not yet a frozen exact
source theorem. The statement phase must inspect a stable copy of the paper and record edition or
file hash, theorem/page, equation normalization, strict versus endpoint threshold, lifespan,
solution space, uniqueness class, persistence and dependence clauses, and any errata. It must then
build and elaborate a concrete Lean proposition rather than promote the abstract legacy wrapper.

No immutable source receipt is supplied at intake. No human-source closure, machine closure, or
checked source-to-Lean transport is claimed.
