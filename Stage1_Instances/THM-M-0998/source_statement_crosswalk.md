# Source-statement crosswalk

| Repository source component | Exact available wording | Formal consequence at intake | Assessment |
|---|---|---|---|
| Name | `Poincare不等式` | Selects the Poincare-inequality family | Insufficient to distinguish probability, PDE, geometric, or discrete variants |
| Category | `概率论与随机过程 / 概率论基础` | Favors a probability/variance formulation | Narrows the family but supplies no domain or assumptions |
| Content gloss | `方差的上界` (upper bound on variance) | Fixes variance as the intended left side | Right-side energy, constant, measure, and function class are absent |
| Attribution/date | Henri Poincare; 1890 | Historical discovery metadata | No title, edition, page, theorem number, or original statement is supplied |
| Source status | `已验证` | Discovery metadata only | Explicitly untrusted under rev-5.6; supplies no H0 or machine credit |
| Legacy Stage1 note | Probability-space/random-variable/measurability/integrability seed | Candidate architecture | The same note mentions convergence, martingale, and Markov branches and therefore cannot serve as an exact Poincare statement |

The repository sources inspected were `Docs/Stage0_Blueprint.md`,
`Docs/Stage1_Blueprint.md`, `Docs/Stage1_Blueprint_Applicable_Theorems.md`, and
`Docs/Stage1_Targets_rev-5.6.json`. None contains a theorem-level citation or missing assumptions.
Consequently the human debt is `H4`: the claim family is recognizable, but exact source fidelity
cannot yet be audited. This is a fail-closed crosswalk, not evidence that any familiar modern
variant is the intended theorem.

Retry condition: provide or locate an authoritative theorem-level source whose statement fixes the
measure/state space, admissible functions, variance convention, energy, constant, and boundary or
centering conditions. Edition/file hash, pinpoint statement, assumptions, and errata must then be
recorded before the statement phase selects a Lean target.
