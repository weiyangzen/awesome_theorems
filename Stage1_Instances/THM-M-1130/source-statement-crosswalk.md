# Source-statement crosswalk

| Claim component | Source lead | Lean target surface | Intake assessment |
|---|---|---|---|
| Historical heat model | J. Fourier, *Theorie analytique de la chaleur* (Paris: Firmin Didot, 1822) | Future space-time field and differential operators | Primary historical work identified, but exact chapter/page, edition hash, notation, translation, and errata have not been audited; not H0 evidence |
| Repository claim | `Docs/Stage0_Blueprint.md`, `THM-M-1130`: "热传导的数学模型" | No exact `Prop` follows from this phrase | It identifies a model family, not ordered binders, hypotheses, and conclusion |
| Differential equation | A pinpoint primary source must fix `partial_t u`, Laplacian/divergence convention, coefficients, and source term | Future PDE predicate or equality | The homogeneous constant-coefficient display is only a candidate, not a frozen statement |
| Domain and data | Must be supplied by the selected claim or its explicit mathematical setup | Future time interval, spatial domain, initial data, and boundary trace | Whole-space, bounded-domain, Cauchy, Dirichlet, Neumann, and mixed problems cannot be conflated |
| Solution notion | Must be selected with its regularity assumptions | Future classical/weak/mild solution structure | These notions are not interchangeable without checked bridge theorems |
| Theorem conclusion | Must be a sourced assertion about the PDE, rather than the PDE name itself | Future exact Lean proposition | Derivation, existence, uniqueness, representation, and qualitative properties are distinct targets |
| Adjacent records | `THM-M-1132` fundamental solution; `THM-M-1133` maximum principle | Explicit exclusions from this target | Reusing either neighboring theorem would substitute rather than clarify `THM-M-1130` |

The source-to-statement blocker is categorical: an equation is mathematical data, while Lean's
theorem gate requires an exact proposition. The statement phase must first determine which sourced
claim the catalog intends, then freeze domains, ordered binders, coefficients, data, regularity,
solution notion, conclusion, and boundary cases. It must mutation-test each material assumption and
keep neighboring theorem IDs distinct. Source audit must obtain an immutable edition with pinpoint
anchors for every premise and conclusion, investigate translation/errata, and receive independent
review. Human status therefore remains `H1`.
