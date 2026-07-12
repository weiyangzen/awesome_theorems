# Source-statement crosswalk

## Available record and source candidates

The repository source record gives only the Chinese title, attribution to Walther Mayer and
Leopold Vietoris, the year 1930, and the phrase "the homology sequence of a union of spaces". Its
`verified` label is explicitly untrusted under rev-5.6 and does not specify a theorem.

Allen Hatcher, *Algebraic Topology* (Cambridge University Press, 2002), the homology chapter's
Mayer-Vietoris section, is a strong modern statement candidate. Edwin H. Spanier, *Algebraic
Topology* (McGraw-Hill, 1966), is a second stable source candidate. Neither edition was inspected
line by line in this intake, so theorem number/page, exact wording, assumptions, definitions, and
errata remain open. These candidates are discovery locators, not `H0` evidence or proof credit.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "space union" | `X = A union B` plus a source-specific excision condition | subspaces, inclusions, cover/interior evidence | included; exact hypothesis open |
| "homology" | singular homology with fixed coefficients | singular chain complex and homology functor | included; coefficient convention open |
| intersection term | homology of `A intersection B` | intersection subspace and induced maps | required |
| sum term | `H_n(A) direct-sum H_n(B)` | biproduct/direct sum and signed inclusion map | required; sign open |
| union term | `H_n(X)` | inclusion-induced map from the sum | required |
| connecting morphism | degree-lowering boundary map | concrete connecting homomorphism | required; API open |
| "sequence" | exactness in all degrees | long sequence or degreewise exactness | required; indexing open |
| 1930 / Mayer / Vietoris | historical locator | no Lean component and no proof credit | provenance requires primary inspection |

## Source and machine boundary

Repository and pinned-source searches found no theorem-specific local instance. Pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` does contain
`Mathlib.CategoryTheory.Sites.SheafCohomology.MayerVietoris`, including
`GrothendieckTopology.MayerVietorisSquare.sequence_exact`. Its objects are sheaf cohomology groups
on a Grothendieck site, not singular homology groups of a union of topological subspaces. It is
therefore an excluded adjacent candidate, not a transport or closure of this target. This limited
local observation is not the downstream immutable anchor audit.

Before `H0`, an independent reviewer must inspect the selected source edition and verify its
theorem/page, definitions, every assumption, coefficients, signs, endpoint cases, and errata.
Before statement credit, every approved row must map to an elaborated Lean expression without
strengthening hypotheses merely to fit a nearby library theorem.
