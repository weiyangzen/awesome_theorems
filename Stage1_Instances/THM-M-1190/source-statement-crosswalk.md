# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` supplies only the title "heat-equation L^p estimate", the
statement phrase "L^p theory for parabolic equations", twentieth-century dating, attribution to
multiple mathematicians, and the untrusted label `已验证`. `Docs/Stage0_Blueprint.md` repeats these
fields and leaves definitions, hypotheses, proof, machine status, and bibliography open. No primary
source, edition, theorem number, page, assumptions, or errata are identified.

No primary-source candidate is asserted at intake. The phrase names a broad family of inequivalent
results, so selecting one now would invent missing mathematics. The metadata status earns no `H0`
or machine-proof credit.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "heat equation" (title) | suggests a particular parabolic model | exact operator and solution predicate | unresolved |
| "parabolic equations" (statement) | broadens beyond the standard heat equation | coefficient/operator structure | unresolved scope mismatch |
| `L^p` | an integrability exponent is involved | measure spaces, exponent domain and endpoints | unresolved |
| "estimate/theory" | some quantitative or regularity result | exact inequality/conclusion and constant | unresolved |
| twentieth century / multiple authors | broad historical family | none | insufficient to identify a theorem |
| `已验证` | untrusted repository label | inspectable source proof or kernel receipt | no credit |

## Downstream source gate

The statement phase must first identify a primary theorem that resolves the title/statement scope
mismatch. Before `H0`, an independent reviewer must verify edition, theorem/page, definitions,
every hypothesis, conclusion, and errata, then approve a row-by-row source-to-canonical-Lean map.
Repository search found no target-specific Lean artifact, so there is no legacy declaration to
credit or audit at intake.

