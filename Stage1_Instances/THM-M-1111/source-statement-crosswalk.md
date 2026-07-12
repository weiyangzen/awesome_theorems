# Source-statement crosswalk

## Primary-source family

- Terence Tao and Van Vu, "Random matrices: Universality of local eigenvalue statistics",
  *Acta Mathematica* 206 (2011), 127-204, DOI `10.1007/s11511-011-0061-3`.
- Terence Tao and Van Vu, arXiv `0906.0510`, "Random matrices: Universality of local eigenvalue
  statistics", including its version history.

These stable identifiers establish the relevant primary-source family, not yet `H0` evidence. The
journal text and arXiv versions must be compared because theorem numbering and hypotheses can vary.
An exact theorem number, pages, immutable source hash, assumption audit, and errata check remain
open. Secondary expositions and later strengthening papers may aid discovery but cannot silently
define this target.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "Tao-Vu four moment theorem" | comparison theorem for local eigenvalue statistics | one canonical quantified proposition | included; exact source variant open |
| "random matrix universality" | asymptotic agreement between two Wigner ensembles | probability spaces, random Hermitian matrices, expectation, asymptotics | included; encodings open |
| "four moment condition" | off-diagonal atoms agree through fourth order | explicit real/complex mixed-moment equalities | included; source convention open |
| diagonal exception | diagonal atoms agree only through second order | separate diagonal moment predicate | included |
| local eigenvalues | fixed ordered eigenvalue indices with source normalization | measurable ordered eigenvalue maps and scaling | included; range open |
| test observable | smooth function of a fixed eigenvalue tuple | differentiability and derivative-growth bounds plus integrability | included; constants open |
| conclusion | expectation difference has the prescribed small bound | exact finite-`n` inequality or asymptotic formulation | included; quantifiers open |
| tail hypothesis | source Condition C0 or selected replacement | uniform tail/regularity predicate | included; exact formula open |

## Repository-source boundary

The Stage0 record supplies only the Chinese label, the phrase "four-moment condition for random
matrix universality", the year 2010, and the authors. It does not specify a mathematical
proposition and its metadata label `verified` is untrusted intake metadata. No repo-local Lean
artifact for `THM-M-1111` was located during this intake. Consequently the current `M4` is a
fail-closed discovery status, not an exhaustive anchor-audit result.

Before `H0`, a source reviewer must approve the chosen immutable edition and a row-by-row mapping of
all matrix assumptions, moment equations, normalizations, constants, dependencies, quantifiers,
conclusion, and published corrections. Before any `M0-*`, the exact Lean expression must elaborate
and its proof body and trust closure must pass the later gates.
