# Source-statement crosswalk

## Primary-source candidate

Lars Hormander, "Hypoelliptic second order differential equations," *Acta Mathematica* 119
(1967), 147-171, DOI `10.1007/BF02392081`. This is the historical article indicated by the
repository's 1967 attribution. The exact theorem number, page span, hypotheses, and any errata have
not yet been checked against a stable scan, so this is an `H2` discovery anchor rather than `H0`.

## Crosswalk

| Repository metadata | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "Hormander condition" | Lie brackets generate tangent directions | vector fields, Lie bracket, pointwise span | bounded; exact quantifiers open |
| "condition for subelliptic operators" | sum-of-squares operator and regularity gain | differential operator and local Sobolev estimate | ambiguous with hypoellipticity |
| differential equations / PDE | distributional solution regularity | distributions, smoothness, operator action | included; APIs open |
| 1967 / Lars Hormander | historical Acta Mathematica result | immutable bibliographic anchor | article identified; theorem/page open |

## Fidelity boundary

The article title supports a hypoellipticity reading, while the repository wording explicitly says
"subelliptic." Those claims are related but not interchangeable. The statement phase must inspect
the article, identify the exact result intended, and record a row-by-row mapping of every operator,
bracket, locality, regularity, and norm hypothesis. No secondary summary may silently choose a
stronger or weaker formulation. No repo-local Lean declaration has been credited at intake.

