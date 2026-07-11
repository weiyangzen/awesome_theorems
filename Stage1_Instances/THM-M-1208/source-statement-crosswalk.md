# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` contains two duplicate inventory records. They give the title
"Strichartz estimates", Robert Strichartz, 1977, and respectively "spacetime estimates for solutions
of dispersive equations" and "spacetime estimates for dispersive equations". Neither record gives a
bibliography, journal, theorem number, page, equation, hypotheses, exponent range, or errata. The
generated Stage0 entry adds no missing mathematical detail. The `已验证` field is explicitly
untrusted metadata under rev-5.6.

No primary-source theorem is asserted at intake. The attribution is a search lead, not `H0` evidence.
Selecting one of the inequivalent results commonly called a Strichartz estimate would broaden or
substitute the source record.

## Crosswalk

| Source element | Information fixed | Information required for canonical Lean target | Intake result |
|---|---|---|---|
| "Strichartz estimates" | conventional theorem-family name | exact named theorem and edition/page | unresolved |
| "dispersive equations" | broad PDE class | equation or propagator and its assumptions | unresolved |
| "solutions" | estimate applies to a solution | solution construction, data, and equality notion | unresolved |
| "spacetime estimates" | mixed time/space control | norms, exponent order/range, interval, constant | unresolved |
| Robert Strichartz / 1977 | source-search coordinates | primary publication and theorem locator | unverified |
| `已验证` | repository screening label | inspectable proof and kernel receipt | no credit |

## Lean discovery boundary

Repo-local search found incidental references to Strichartz machinery in historical Stage1 modules,
but no artifact tied to THM-M-1208 and no exact terminal declaration was established. This is not an
anchor audit and gives no machine credit. After primary-source identification, the statement phase
must produce an elaborated exact target and test altered equation, exponent, endpoint, scope, and
norm-order mutations. Independent review must then verify the source edition, theorem/page,
assumptions, definitions, errata, and the row-by-row source-to-Lean map before `H0` is possible.
