# THM-M-0406 source-statement crosswalk

## Repository sources

| Source | Recorded claim | Intake finding |
|---|---|---|
| `Docs/researches/math_theorems.md` | Corvaja/Evertse, 2004, degeneracy of integral points on curves, status “verified” | Metadata-only, no theorem/page/assumptions; status is untrusted. |
| `Docs/Stage0_Blueprint.md` | Repeats the metadata and leaves exact definitions and hypotheses open | Cannot identify an exact proposition. |
| `Docs/Stage1_Blueprint.md` | Lean 4 candidate in a hard anchor/wrapper lane | Selection only; explicitly not completion. |
| `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_019.lean` | Selects Corvaja--Zannier, *On integral points on surfaces* (2004), as a candidate repair | Legacy discovery evidence only; selection must be independently checked against the primary statement. |

## Candidate primary source

Pietro Corvaja and Umberto Zannier, “On integral points on surfaces,” *Annals of Mathematics* 160 (2004), 705-726, DOI `10.4007/annals.2004.160.705`; legacy artifact also records arXiv `math/0206100`.

This citation is sufficiently specific for the next audit, but the paper's exact theorem number, page-level statement, assumptions, and errata have not been inspected in this intake. Consequently it supports `H1`, not `H0`.

## Claim-field crosswalk

| Required field | Metadata | Candidate-source direction | Status |
|---|---|---|---|
| Authors | Corvaja/Evertse | Corvaja/Zannier | conflict; must resolve |
| Year | 2004 | 2004 publication | compatible |
| Geometric object | curves | surface with boundary divisors in legacy candidate | conflict/possible gloss error |
| Arithmetic base | absent | expected number field and finite places | missing exact source text |
| Hypotheses | absent | divisor/intersection and integrality conditions | missing exact source text |
| Conclusion | “degeneracy” | integral points contained in a proper curve, per legacy candidate | needs primary-source transcription |
| Errata | absent | unknown | open |
| Lean target | absent | legacy abstract `StatementShape` | not exact; no credit |

## Statement-phase resolution

The immutable arXiv source `math/0206100` (SHA-256
`cea7fd97f089fb2d33a771dce9399a30d869e24b06fd319cb62fba26f20139de`)
identifies Theorem 1 on pages 706-707. It has authors Corvaja--Zannier and a
surface domain. Evertse occurs later only in the discussion of quantitative
Subspace-Theorem estimates. The metadata author and curve wording are thus
errors, not authorization for a substituted Evertse theorem.

`Statement.lean` transcribes that theorem. Primary-source/errata review to H0
belongs to a later audit; the present statement record remains provisional.
