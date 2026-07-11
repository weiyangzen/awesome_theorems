# Source-statement crosswalk

## Primary source

Gerd Faltings, *Endlichkeitssatze fur abelsche Varietaten uber Zahlkorpern*,
Inventiones Mathematicae 73 (1983), 349-366, DOI
`10.1007/BF01388432`. This is the primary published proof source customarily
identified with the Mordell conjecture theorem.

The bibliographic identification is frozen, but a scan-level theorem/page and
errata inspection has not yet been independently reviewed. Consequently this
intake does **not** assign H0 or claim a complete primary-source audit.

| Canonical component | Source mapping | Intake status |
|---|---|---|
| number field `K` | `Zahlkorper` base in the cited paper | identified; pinpoint review open |
| curve over `K` | Mordell-conjecture curve case/consequence | identified; precise theorem label open |
| smooth, proper, geometrically connected | modern curve formulation; terminology must be reconciled with the paper | assumption crosswalk open |
| genus at least two | Mordell hyperbolicity condition | identified; pinpoint review open |
| finitely many `K`-points | finiteness conclusion | identified; pinpoint review open |

No secondary exposition is being used as proof evidence. The anchor-audit phase
must record immutable formal candidates separately; the historical local Lean
file is not a human source and not kernel closure of the theorem.
