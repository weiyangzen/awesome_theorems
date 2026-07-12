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
| "condition for subelliptic operators" | rank hypothesis used for a sum-of-squares operator | generated brackets and pointwise span | frozen as the condition, not its consequence |
| differential equations / PDE | vector fields on an open coordinate domain | open set and coordinate vector fields | frozen |
| 1967 / Lars Hormander | historical Acta Mathematica result | immutable bibliographic anchor | article identified; theorem/page open |

## Statement-phase selection

The adjacent repository row THM-M-1259 separately names "Hormander theorem (subelliptic)" and its
regularity conclusion. THM-M-1258 therefore freezes the condition itself: the Lie algebra generated
by the drift and square fields has full pointwise rank. `Statement.lean` maps this to an inductively
generated bracket family and pointwise `Submodule.span = top`.

This resolves target identity without pretending to resolve source fidelity. The article's exact
page wording, coefficient regularity assumed when the condition is used, operator convention, and
errata still require primary-source audit. None of those may be used later to broaden this target
into THM-M-1259's analytic conclusion.
