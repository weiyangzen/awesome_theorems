# Source-statement crosswalk

| Repository claim component | Repository anchor | Lean discovery candidate | Intake assessment |
|---|---|---|---|
| Name | Stage0: `志田周期`; Stage1: `志田周期`; legacy Lean: “Shida periods” | namespace `S1_M_086` | The transliteration and identity are not established by a cited source |
| Attribution | Stage0 names Goro Shimura | none | Attribution conflicts with or at least fails to explain the “Shida” label; no inference to a Shimura theorem is permitted |
| Subject | “period integrals on Shida varieties” | `ShidaPeriodDatum.periodPackage` | A topic phrase, not a theorem statement; variety and period are undefined |
| Geometric assumptions | none in source metadata | `GeometricShidaModel D := IsProper ... ∧ Smooth ...` | Assumptions were introduced by the legacy artifact and have no located source anchor |
| Automorphic/cohomological data | none in source metadata | proposition fields on `ShidaPeriodDatum` | Placeholders for missing semantics, not sourced hypotheses |
| Conclusion | unspecified “period relation” | `D.hasPeriodComparison` | The desired conclusion is stored as an arbitrary input proposition; this cannot be credited as the source theorem |

The repository currently supplies no bibliography, title, edition, theorem number, page, quoted
statement, assumptions, or errata trail for this target. Consequently no responsible crosswalk to
a primary mathematical source can yet be made. A broad web or library search for work of Goro
Shimura on periods would be discovery, not enough to choose one result: the next phase must require
a unique source pinpoint and independently review the name correction before freezing a claim.

The legacy file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_086.lean` is useful only for inventorying likely
API areas (schemes, number fields, integrals). Its `StatementShape` is neither an alternate encoding
nor a weakened theorem accepted here. Exact elaboration, mutation tests, source pins, and checked
transports remain open.

No `H0`, exact-statement, machine-closure, or theorem-completion claim is made.
