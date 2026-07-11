# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives only the Chinese title "boundary element method",
attribution to multiple mathematicians, twentieth century, the description "a numerical method
based on boundary integrals", importance "high", and the untrusted status `已验证`.
`Docs/Stage0_Blueprint.md` repeats those fields while leaving definitions, hypotheses, proof,
axioms, machine artifacts, and dependencies open. No bibliography, edition, theorem number, page,
or errata record is attached.

No primary-source theorem can truthfully be selected from this record alone. Boundary element
methods comprise inequivalent formulations and results, so inventing a convergence theorem would
broaden the source. The metadata status supplies no `H0` or machine-proof credit.

## Crosswalk

| Source element | Information fixed | Information required for a theorem/Lean target | Intake result |
|---|---|---|---|
| "boundary element method" | broad method family | one named proposition with ordered binders | unresolved |
| "boundary integrals" | some boundary integral formulation | operator, kernel, spaces, mapping properties | unresolved |
| "numerical method" | approximation is intended | discrete spaces, scheme, mesh, computed quantity | unresolved |
| no stated conclusion | none | existence, stability, convergence, or error conclusion | unresolved |
| twentieth century / multiple authors | broad history | primary edition, theorem/page, assumptions, errata | unresolved |
| `已验证` | repository metadata only | inspectable proof and accepted kernel receipts | no credit |

The first downstream gate is primary-source identification and selection of an exact theorem without
substitution. Independent review must then verify its edition, theorem/page, definitions, complete
assumptions, conclusion, and errata before a row-by-row canonical Lean mapping can receive `H0`.
