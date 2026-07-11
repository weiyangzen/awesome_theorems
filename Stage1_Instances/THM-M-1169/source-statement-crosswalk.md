# Source-statement crosswalk

## Available source record

The repository research inventory (`Docs/researches/math_theorems.md`) supplies only: title
"boundary estimates", attribution to multiple mathematicians, twentieth century, statement
"regularity of solutions at the boundary", and the untrusted label `已验证`. `Docs/Stage0_Blueprint.md`
repeats that phrase and explicitly leaves definitions, hypotheses, proof, and machine status open.
No bibliography, edition, theorem number, page, or errata record is attached.

Consequently no primary-source candidate is asserted at intake. Selecting one of the many inequivalent
boundary regularity theorems without further provenance would invent missing mathematics. The source
label is metadata-screening input, not `H0` evidence.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "boundary estimates" | a boundary-related bound or regularity result | concrete proposition and norm inequality | unresolved |
| "solutions" | some equation has solutions | operator, data, solution predicate | unresolved |
| "at the boundary" | domain boundary is relevant | ambient space, domain, boundary/trace API | unresolved |
| "regularity" | improved or controlled regularity | source/target function spaces and exponent/order | unresolved |
| twentieth century / multiple authors | broad historical family | none | insufficient to identify a theorem |
| `已验证` | untrusted repository label | inspectable human proof or kernel receipt | no credit |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_146.lean` is useful discovery evidence. Its
`StatementShape` universally quantifies over an abstract `BoundaryRegularityProblem` whose fields
already supply the intended regularity predicate, trace, and norms. It neither identifies the source
theorem nor proves a concrete boundary estimate. Its wrappers and dated audits receive no rev-5.6
credit at intake.

The first downstream gate is therefore primary-source identification. Before `H0`, an independent
reviewer must verify edition, theorem/page, every assumption, definitions and errata, and approve a
row-by-row source-to-canonical-Lean mapping.
