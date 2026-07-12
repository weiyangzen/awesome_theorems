# Source-statement crosswalk

## Repository source surfaces

| Surface | Wording | Statement contribution | Intake assessment |
|---|---|---|---|
| `Docs/Stage1_Targets_rev-5.6.json` | `孤立子理论`; untrusted `已验证` | target identity and scheduling metadata only | no proposition or proof credit |
| `Docs/Stage0_Blueprint.md` | `孤立子的数学理论`; many mathematicians; twentieth century | broad topic description | no equation, hypotheses, or conclusion |
| `Docs/researches/math_theorems.md` | same short topic record | provenance of the generated metadata | not a mathematical source |
| neighboring legacy `S1_M_212.lean` | abstract Hirota certificate and partial KdV definitions for `THM-M-1553` | possible infrastructure discovery | different theorem ID; no statement or proof credit |

## Foundational primary-paper anchors

Norman J. Zabusky and Martin D. Kruskal, "Interaction of 'Solitons' in a Collisionless Plasma and
the Recurrence of Initial States," *Physical Review Letters* **15** (1965), 240-243,
DOI `10.1103/PhysRevLett.15.240`, is a primary historical anchor for the term *soliton* and for
numerically observed KdV recurrence/collision behavior. It is not, merely by citation, a single
analytic theorem matching the repository phrase.

Clifford S. Gardner, John M. Greene, Martin D. Kruskal, and Robert M. Miura, "Method for Solving
the Korteweg-de Vries Equation," *Physical Review Letters* **19** (1967), 1095-1097,
DOI `10.1103/PhysRevLett.19.1095`, is a primary anchor for the inverse-scattering method for the KdV
initial-value problem. Selecting a precise theorem from this line requires a stable copy and an
assumption-complete transcription, potentially using its detailed follow-up literature; that work
has not occurred in this intake.

## Claim-component crosswalk

| Needed canonical component | Repository metadata | 1965 Zabusky-Kruskal | 1967 Gardner-Greene-Kruskal-Miura | Status |
|---|---|---|---|---|
| equation and normalization | absent | KdV setting is relevant | KdV setting is central | exact convention not transcribed |
| mathematical domains | absent | physical/numerical setup | initial-value/scattering setup | not frozen |
| ordered quantifiers | absent | no repository mapping | no repository mapping | missing |
| analytic hypotheses | absent | numerical initial state | decay/regularity assumptions require pinpoint audit | missing |
| conclusion | "theory" only | recurrence and interaction observations | solution by inverse-scattering method | multiple non-equivalent candidates |
| proof/evidence kind | untrusted `已验证` | numerical computation and interpretation | analytic method announcement | source role differs |
| theorem/page/errata map | absent | paper pages identified only | paper pages identified only | not `H0` |

## Fidelity decision

The available repository wording does not determine which primary claim is intended. Freezing the
1965 numerical observation as a theorem would violate the computation boundary; freezing an
arbitrary explicit KdV solution would narrow the target without source authority; freezing the full
inverse-scattering theory would require assumptions not present in the metadata. The statement gate
is therefore blocked until an integration-lane source decision selects one proposition and records
pinpoint text, assumptions, corrections/errata, and independent review.
