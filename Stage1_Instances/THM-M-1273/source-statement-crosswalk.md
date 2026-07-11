# Source-statement crosswalk

## Available source record

The rev-5.6 manifest supplies the Chinese label "Morse理论在PDE中的应用", the category
"微分方程 / 偏微分方程", and an explicitly untrusted `已验证` source status. The underlying
repository research inventory adds only "many mathematicians", "20th century", and "topological
methods for variational problems". No author, work, theorem number, page, equation, or hypotheses
are attached. The remaining repository occurrences are generated Stage0/Stage1 inventory and
execution entries.

The label is not a proposition with a truth value. It therefore cannot truthfully be broadened into
"Morse theory applies to PDE" or narrowed to an arbitrarily selected application. Primary-source
discovery and theorem disambiguation are mandatory before statement freeze. No primary candidate is
listed merely from memory, because doing so would not identify the intended repository theorem.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Morse theory" | index, critical groups, or Morse inequalities | concrete definitions for a specified functional | ambiguous; not selected |
| "PDE" | equation plus domain and boundary data | function spaces, operator, weak/classical solution predicate | entirely open |
| "application" | existence, multiplicity, topology, or index conclusion | exact proposition and variational-to-PDE bridge | entirely open |
| "topological methods for variational problems" | broad inventory gloss | no unique formal proposition | confirms method-level ambiguity |
| `已验证` | legacy metadata label | no proof credit | explicitly untrusted |

## Source and machine boundary

No theorem-specific legacy Lean module or accepted external declaration was located by the intake
search. This is not a complete mathlib or external anchor audit. After an exact source theorem is
selected, independent review must verify its edition, theorem/page, definitions, hypotheses,
errata, and proof boundary. Each source component must then map row by row to an elaborated Lean
target before H0 or statement credit is possible.
