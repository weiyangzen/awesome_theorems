# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives the title "Green function", George Green, 1828, and the
phrase "integral kernel for boundary-value problems". `Docs/Stage0_Blueprint.md` repeats those data
and explicitly leaves definitions, hypotheses, proof, equivalent formulations, dependencies, and
machine artifact open. No bibliography, edition, theorem/page, quotation, or errata is supplied.

The same research inventory later contains another "Green function" entry phrased "integral
representation for boundary-value problems"; it does not identify itself with THM-M-1163 and is
not used to silently sharpen this target. No primary-source candidate is asserted at intake.

## Crosswalk

| Source element | Information fixed | Information still required | Intake result |
|---|---|---|---|
| "Green function" | a conventional mathematical object | definition, operator, normalization | unresolved |
| "boundary-value problems" | boundary data participates | domain, boundary condition, solution space | unresolved |
| "integral kernel" | an integral operator is intended | measure, integrability, kernel identity | unresolved |
| George Green / 1828 | historical attribution metadata | primary edition, theorem/page, exact scope | unverified |
| `已验证` | metadata-screening label only | inspectable source and kernel receipts | no credit |

The first downstream gate is primary-source identification and selection of a single exact claim.
An independent reviewer must then verify every hypothesis and approve a row-by-row mapping to the
canonical Lean proposition before source or statement closure can be credited.
