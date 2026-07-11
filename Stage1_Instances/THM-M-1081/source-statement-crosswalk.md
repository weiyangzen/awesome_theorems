# Source-statement crosswalk

## Repository evidence

The originating entry in `Docs/researches/math_theorems.md` gives only the name, Michel Talagrand,
the year 1995, and `配置函数的集中`. `Docs/Stage0_Blueprint.md` repeats those fields and explicitly
leaves the exact definitions, assumptions, proof path, axioms, and machine artifact open.

## Primary-source candidate

Michel Talagrand, "Concentration of measure and isoperimetric inequalities in product spaces,"
*Publications Mathématiques de l'IHÉS* 81 (1995), 73-205, is the leading primary-source candidate
because its title, author, date, and product-configuration subject fit the metadata. The paper's
exact theorem number/page, displayed formula, conventions, and errata have not been inspected for
this intake. This citation is a discovery anchor, not `H0` evidence.

## Crosswalk

| Source field | Repository evidence | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|---|
| theorem identity | `Talagrand不等式` | one of several Talagrand inequalities | one canonical proposition/declaration | ambiguous |
| subject | concentration of configuration functions | product-space/configuration concentration | coordinate measurable spaces and product probability measure | family included; encoding open |
| geometric form | not supplied | convex distance from a point to a measurable set | finite-support weights, coordinate disagreement, supremum/infimum, measurability | candidate only |
| functional form | not supplied | tail bound for a Lipschitz/certifiable function | regularity, certificate predicate, median/expectation and tail event | candidate only |
| constants | not supplied | Gaussian-type exponential tail | exact real/extended-real expression and side conditions | open |
| source proof | no theorem/page or proof cited | primary proof and assumptions | node-by-node premise/source map | open (`H4`) |
| formal anchor | none supplied | possible probability/product-measure APIs | exact module, declaration, revision, type, axioms and body provenance | open (`M4`) |

## Disambiguation boundary

The same name is used for unrelated transportation and functional inequalities. The 1996 Gaussian
transportation-cost result cannot be selected merely because it is also called Talagrand's
inequality. Conversely, the separate repository target `THM-M-0974` describes concentration of
convex Lipschitz functions, so choosing that statement here requires an explicit source-identity
crosswalk rather than name similarity.

Before `H0`, an independent reviewer must verify an immutable edition, exact theorem/page,
definitions, all assumptions, normalization, and errata, and approve a row-by-row source-to-Lean
map. Before any machine credit, the anchor audit must inspect the pinned mathlib revision and
credible Lean 4 projects and record exact types, toolchains, placeholders, axioms, imports, and
terminal proof-body provenance.
