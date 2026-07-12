# Source-statement crosswalk

## Available record and source boundary

The repository research inventory supplies only the title `格林定理`, attribution to George Green,
the year 1828, the gloss "the relationship between a line integral and a double integral on a
planar region", and an `已验证` label. The manifest deliberately marks that label untrusted. This is
enough to identify the theorem family, but not enough to select an exact proposition.

The historical source candidate is George Green, *An Essay on the Application of Mathematical
Analysis to the Theories of Electricity and Magnetism*, Nottingham (1828). It is relevant
historical provenance, but its exact relation to the modern circulation formula, its original
notation and hypotheses, and a page/formula locator have not been inspected here. A stable modern
analysis text stating and proving the precise selected variant will also be needed as the
statement-and-proof source. Exact edition, theorem number, pages, invoked definitions, and errata
remain statement/source-audit work. These locators therefore give no `H0` credit.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "planar region" | compact oriented `D` in `R^2` | set/chain plus compactness, regularity, and orientation data | family included; region class open |
| "line integral" | circulation of `P dx + Q dy` on `boundary D` | oriented path/chain integral with boundary multiplicity | integral API and boundary representation open |
| "double integral" | area integral over `D` | measure/restricted integral on `R x R` | convention and integrability hypotheses open |
| Green's theorem | `integral_boundary P dx + Q dy = integral_D (partial_x Q - partial_y P) dA` | derivatives, scalar curl, and an equality of concrete integrals | provisional human root only |
| positive orientation | outer boundary counterclockwise, holes oppositely oriented | oriented boundary operator or equivalent winding convention | exact encoding open |
| regularity | differentiability sufficient for the chosen theorem | neighborhood plus `C1`/derivative hypotheses | exact strength open |

## Variant and proof boundary

The flux formula follows formally by rotating a vector field, and the differential-form formula is
a two-dimensional Stokes instance. Neither is definitionally the same statement. A later phase may
credit one only after compiling an exact checked transport that preserves region, boundary,
orientation, regularity, and integration conventions.

No theorem-specific accepted Lean declaration is identified in this intake. The
`hard_statement_first_partial_verification` lane is scheduling metadata, not evidence that pinned
mathlib contains this theorem. Anchor audit must separately inspect repo-local and pinned upstream
candidates, their exact types and terminal bodies, axioms, imports, licenses, and revisions.

Before `H0`, an independent reviewer must inspect the chosen editions and pinpoint every assumption,
conclusion, proof boundary, and known erratum. Before statement credit, those rows must map to an
elaborated Lean expression and all alternate forms must have checked transports.
