# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` supplies only the Chinese title `双层位势`, attribution to
multiple mathematicians, nineteenth century, the phrase `边界积分表示`, high importance, and the
untrusted status `已验证`. `Docs/Stage0_Blueprint.md` repeats these fields and leaves definitions,
hypotheses, proof, dependencies, and machine artifacts open. There is no bibliography, edition,
theorem number, page, quotation, or errata record.

No primary-source candidate is asserted at intake. Potential theory contains inequivalent
double-layer formulas for different operators and conventions, so selecting one from the title
alone would invent mathematics. The metadata is not `H0` evidence.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| `双层位势` | a double-layer-potential family | an explicit kernel normal derivative and boundary integral | family only; unresolved |
| `边界积分表示` | some object is represented by boundary data | quantified represented function, region, equality, and hypotheses | unresolved |
| nineteenth century | historical period | none | insufficient to identify a theorem |
| multiple mathematicians | no unique attribution | none | insufficient to select a source |
| `已验证` | untrusted inventory label | inspectable proof or kernel receipt | no credit |

## Formalization boundary

There is no matching target module among the repository's historical 300 Lean Stage1 modules and no
accepted Lean declaration attached to this record. The later anchor audit must search the pinned
mathlib revision and credible external Lean 4 projects only after the exact statement is frozen.

The first downstream gate is primary-source identification. Before `H0`, an independent reviewer
must verify the stable edition, exact theorem/page, definitions, every hypothesis, normalization,
orientation convention, and errata, and approve a row-by-row source-to-canonical-Lean mapping.
