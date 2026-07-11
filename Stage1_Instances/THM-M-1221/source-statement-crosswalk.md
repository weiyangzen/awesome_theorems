# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` records only "Segal theorem", Irving Segal, 1963, and "local
well-posedness of NLW", plus the untrusted label `已验证`. `Docs/Stage0_Blueprint.md` repeats these
fields and explicitly leaves definitions, premises, proof path, formal artifacts, and axioms open.
Neither supplies a title, journal, edition, theorem number, page, equation, bibliography, or errata.
No primary-source candidate is asserted by this intake.

The phrase does not distinguish among inequivalent nonlinear wave equations and functional
settings. Selecting a familiar Segal-style abstract evolution theorem or a modern Sobolev-space
NLW formulation would broaden or substitute the source claim. Primary-source identification is
therefore the first downstream statement gate.

## Crosswalk

| Source element | Information fixed | Information required for Lean | Intake result |
|---|---|---|---|
| "NLW" | some nonlinear wave equation | exact operator, domain, dimension, nonlinearity, parameters | unresolved |
| "local" | a non-global time assertion | interval form, lifespan quantifiers, maximality | unresolved |
| "well-posedness" | an informal result family | exact existence, uniqueness, dependence, and solution-space predicates | unresolved |
| Segal / 1963 | secondary attribution and year | no Lean content | requires primary-source verification |
| `已验证` | untrusted inventory label | inspectable proof and kernel evidence | no credit |

## Formalization boundary

No target-specific Lean declaration or legacy priority slot was found. H0 requires a primary
edition/theorem/page/assumption/errata crosswalk and independent review. Statement acceptance
requires an exact canonical Lean expression under pinned minimal imports, environment fingerprint,
and checked transports for any alternate formulation. Those belong to later phases.
