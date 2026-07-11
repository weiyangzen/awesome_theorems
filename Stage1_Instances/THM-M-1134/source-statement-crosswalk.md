# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives the title, attribution "many mathematicians", twentieth
century, the phrase "lower-bound estimate for positive solutions", and `已验证`. The corresponding
`Docs/Stage0_Blueprint.md` entry repeats this wording while leaving definitions, hypotheses, proof,
formal system, axioms, and machine status open. Neither record supplies a bibliography, edition,
theorem number, page, or errata trail. The label is therefore screening metadata, not `H0` evidence.

## Crosswalk

| Source element | Fixed mathematical content | Required canonical/Lean detail | Intake result |
|---|---|---|---|
| "heat equation" | parabolic PDE family | operator normalization, dimension, domain, time interval | unresolved |
| "positive solutions" | positivity plus a solution predicate | codomain, positivity strength, regularity, equation semantics | unresolved |
| "Harnack inequality" | comparison across parabolic regions/times | quantified regions, time order, inequality, constant | unresolved |
| "lower-bound estimate" | a later/earlier value controls another | exact infimum/supremum or pointwise formulation | unresolved |
| twentieth century / many authors | broad historical family | primary edition, theorem/page, assumptions, errata | insufficient |
| `已验证` | untrusted repository label | inspectable source and kernel receipts | no credit |

## Statement boundary

Multiple inequivalent standard formulations fit the phrase, including pointwise heat-kernel
comparisons and cylinder `sup`/`inf` parabolic Harnack inequalities. Choosing among them at intake
would invent missing mathematics. A primary source must first be selected and independently
cross-checked row by row. Only then may the statement phase freeze ordered binders and hypotheses,
elaborate an exact Lean expression, and mutation-test domain, time-order, positivity, and boundary
conditions. No existing Lean declaration is credited by this intake.
