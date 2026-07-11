# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives only the Chinese title "Kirchhoff formula", attribution to
Gustav Kirchhoff, year 1883, and statement "solution of the three-dimensional wave equation".
`Docs/Stage0_Blueprint.md` repeats this wording while leaving equivalent formulations, axioms, and
machine artifacts open. Neither record gives a bibliography, edition, theorem number, page,
definitions, assumptions, or errata. No primary source is therefore asserted at intake.

## Crosswalk

| Source element | Information fixed | Information still required for Lean | Intake result |
|---|---|---|---|
| "Kirchhoff formula" | a historically named formula family | exact formula variant and normalization | unresolved |
| "three-dimensional" | spatial dimension is three | model of `R^3`, norm, spheres, measure | family-level only |
| "wave equation" | a hyperbolic PDE is intended | operator sign, wave speed, forcing, derivatives | unresolved |
| "solution" | formula should represent some solution | initial/boundary data, regularity, solution and uniqueness class | unresolved |
| Gustav Kirchhoff / 1883 | attribution metadata | primary edition, theorem/page, assumptions, errata | unverified |
| `已验证` | untrusted repository label | human proof crosswalk and kernel receipt | no credit |

## Statement boundary

The conventional spherical-mean Cauchy formula makes the family intelligible but is not enough to
freeze an exact proposition: sources differ in sphere-measure normalization, wave speed, forcing,
regularity, and whether existence and uniqueness accompany the identity. Adopting one silently
would broaden the source record. The next phase must first select and independently review a primary
edition/theorem/page, then map every hypothesis and conclusion to an elaborated Lean expression.

No repo-local Lean module specific to `THM-M-1128` was found during intake. Anchor discovery and API
feasibility belong to the later anchor-audit phase and are not inferred from similarly named
Kirchhoff results in unrelated domains.
