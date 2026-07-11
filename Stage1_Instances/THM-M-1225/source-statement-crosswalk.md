# Source-statement crosswalk

## Repository evidence and source candidate

The repository supplies only: "Tao NLW theorem", year 2006, and `能量临界NLW`. The Stage0 record
leaves the definitions, hypotheses, proof route, and formal system unset. Thus its `已验证` label is
not a primary-source or machine-check receipt.

A concrete candidate is Terence Tao, *Global regularity for a logarithmically supercritical
defocusing nonlinear wave equation for spherically symmetric data*, arXiv:math/0601164 (2006).
Repo-local legacy research also cites this identifier when discussing the established 3D
energy-critical quintic NLW. However, the candidate's title describes a logarithmically
supercritical radial theorem, not literally the metadata phrase. Exact theorem text, version,
pages, assumptions, and errata have not been inspected here; it is a search lead, not `H0`.

## Crosswalk

| Repository phrase | Source question to resolve | Required Lean surface | Intake status |
|---|---|---|---|
| "Tao NLW theorem" | exact 2006 publication/preprint and theorem number | declaration tied to a cited proposition | open |
| `能量临界NLW` | equation, dimension, critical scaling, sign, and exponent | concrete spacetime function, derivatives, Laplacian, nonlinearity | family only |
| theorem conclusion | global existence, regularity, well-posedness, scattering, or quantitative bound | explicit quantified conclusion and solution predicate | unspecified |
| initial data | Sobolev/energy/smooth class and any radial or decay assumptions | concrete function-space predicates and initial traces | unspecified |
| 2006 | publication chronology versus preprint version | immutable source edition in evidence | candidate identified |

## Acceptance boundary

The statement phase must quote and independently cross-check the selected primary theorem and its
surrounding definitions. If the source is the logarithmically supercritical radial result, that
mismatch must be reconciled explicitly rather than broadening or substituting the target. H0 also
requires theorem/page/edition, assumption and conclusion rows, errata search, and independent
review. No existing Lean terminal theorem has been identified or credited by this intake.
