# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` records only the Chinese title "热方程的基本解", attribution to
multiple mathematicians, nineteenth century, and the statement "热核或高斯核". The Stage 0
blueprint repeats those fields while marking exact definitions, hypotheses, proof, and machine
artifacts open. Neither record provides a bibliography, edition, theorem/page, formula, or errata.
The `已验证` field is explicitly untrusted metadata in the rev-5.6 manifest.

No primary-source candidate is asserted at intake. In particular, familiarity with the standard
Euclidean Gaussian does not resolve which of its analytical properties the source intended to claim.

## Crosswalk

| Source element | Information fixed | Information still required for Lean | Intake result |
|---|---|---|---|
| "heat equation" | a parabolic heat operator is relevant | operator convention, coefficient, domains | unresolved |
| "fundamental solution" | kernel should represent point-source evolution | distribution/approximation notion, initial condition, solution class | unresolved |
| "heat kernel" | a heat-evolution kernel is intended | ambient geometry, formula, time range, normalization | unresolved |
| "Gaussian kernel" | Gaussian form is suggested | dimension, norm, constants, exponent and prefactor | unresolved |
| nineteenth century / multiple authors | broad history | edition, theorem/page, assumptions, errata | insufficient |
| `已验证` | repository screening label | inspectable human and kernel evidence | no credit |

## Formalization boundary

No repository-local Lean artifact is identified for this target by the manifest (`legacy_priority_slot`
is null), and no canonical Lean declaration is frozen. The next phase must first select and verify a
primary statement, then map every domain, binder, hypothesis, conclusion, and boundary convention to
an elaborated Lean expression. Until that review, a mathlib Gaussian or PDE result is discovery
material only and cannot receive statement or proof credit.
