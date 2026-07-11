# Source-statement crosswalk

## Candidate primary sources

- Saunders Mac Lane, *Categories for the Working Mathematician*, second edition, Springer, 1998,
  Chapter V (Limits). This is a primary monograph candidate for the universal definitions,
  completeness, and standard existence constructions. Exact section, proposition/theorem, page,
  assumptions, and errata have not yet been inspected.
- Peter Freyd, *Abelian Categories: An Introduction to the Theory of Functors*, Harper & Row, 1964.
  This is a historical source candidate only if the intended claim is the completeness theorem for
  a special class of categories. No theorem identity is inferred from the repository label.

These entries are discovery anchors, not `H0` evidence. The statement phase must select and inspect
one exact result; a textbook definition cannot by itself support an unspecified existence claim.

## Crosswalk

| Repository phrase | Mathematical reading | Required Lean component | Intake status |
|---|---|---|---|
| "limits and colimits theorem" | unspecified categorical result and its dual | exact declaration-shaped proposition | ambiguous; open |
| "existence of limits in categories" | existence for a diagram or shape under hypotheses | `HasLimit F` or a construction yielding it | hypotheses absent; open |
| limit | terminal object in the category of cones | `CategoryTheory.Cone`, `IsLimit` | subject identified; imports open |
| colimit | initial object in the category of cocones | `CategoryTheory.Cocone`, `IsColimit` | subject identified; imports open |
| duality | reversal through the opposite category | checked `op`/`unop` transport | inclusion source-dependent |

## Source boundary

The repository provides only a generic title and the sentence "existence of limits in categories".
There is no existing `S1_M_136.lean` module in the worker clone. Consequently this intake does not
invent a theorem from nearby homological-algebra prose. Before `H0`, independent review must verify
the exact edition, theorem/page, definitions, all hypotheses, size conventions, errata, and every
source-to-Lean row. Before any `M0` claim, the selected expression must elaborate and its terminal
proof body and transitive trust closure must be checked at the pinned revision.
