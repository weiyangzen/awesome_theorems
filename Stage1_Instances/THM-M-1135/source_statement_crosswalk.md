# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Target identity | `Docs/researches/math_theorems.md`, entry `Laplace方程` | none | Names Laplace, 1785, and "fundamental equation of harmonic functions"; this is repository metadata, not a primary source |
| Stage0 projection | `Docs/Stage0_Blueprint.md`, `THM-M-1135` | none | Repeats the topic wording and explicitly leaves definitions, premises, equivalences, axioms, and artifacts open |
| Classical equation | Conventional reading: `Delta u = 0` | future expression only | Plausible interpretation, but insufficient to determine a proposition or Lean type |
| Harmonic-function relationship | Harmonic functions are conventionally defined/characterized through vanishing Laplacian | future predicate only | Could be a definition or an equivalence theorem; substituting either would broaden the source record |
| Neighboring PDE theorems | Mean-value, maximum-principle, and boundary-value results | deliberately none | Separate mathematical claims and nearby Stage0 entries; excluded at intake |

## Exact-statement blocker

The available record lacks ordered binders, domain, regularity, boundary conditions, solution
notion, and a conclusion distinct from the equation itself. Therefore there is no truthful exact
human claim to translate yet. `Delta u = 0` is a predicate on suitable functions, not by itself a
closed theorem. The later statement phase requires a primary source with an edition and page or
theorem pinpoint that fixes one claim, followed by an assumptions/notation crosswalk and errata
check. Until then the source state is `H4` and the Lean state is `M4`.

No external machine theorem is claimed, and no source-status label (`已验证`) is treated as proof
evidence. This intake does not classify a machine-proof debt beyond the statement blocker because
doing so would require knowing which proposition is actually owed.
