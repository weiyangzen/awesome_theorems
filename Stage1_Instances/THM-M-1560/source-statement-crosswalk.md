# Source-statement crosswalk

## Repository record

The repository discovery record in `Docs/researches/math_theorems.md` names the “Deift-Zhou
method,” attributes it to Percy Deift and Xin Zhou, dates it to 1993, and gives only “steepest
descent method” as its statement. `Docs/Stage0_Blueprint.md` repeats those fields while leaving exact
definitions, assumptions, proof path, equivalent forms, axioms, and machine artifacts open. The
rev-5.6 manifest assigns `THM-M-1560` rank 571 and uniformly resets it to `L0 / rework_required`.
Its historical `已验证` field is explicitly untrusted.

## Primary-source candidate inspected at intake

The official Annals of Mathematics article record was inspected on 2026-07-12:

- Percy Deift and Xin Zhou, *A steepest descent method for oscillatory Riemann-Hilbert problems.
  Asymptotics for the MKdV equation*, Annals of Mathematics 137 (1993), issue 2, pages 295-368,
  DOI `10.2307/2946540`.
- Official record: `https://annals.math.princeton.edu/1993/137-2/p03`.

The journal record confirms the title, authors, year, volume, issue, and pages. This is genuine
discovery provenance, but the full paper's theorem text, numbered results, definitions, hypotheses,
proof boundaries, and errata were not independently audited here. It is therefore a candidate, not
an `E4`/`H0` source packet and not yet the selected exact statement.

## Crosswalk

| Repository or source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| “Deift-Zhou method” | nonlinear steepest descent through Riemann-Hilbert deformations | typed chain of equivalent/transformed jump problems and checked transports | method family identified; exact chain open |
| “steepest descent” | isolate stationary phase and reduce to model plus small-norm error problems | phase, stationary points, contour deformation, parametrices, norm estimates | not classical scalar steepest descent; conventions open |
| “oscillatory Riemann-Hilbert problems” | normalized matrix boundary-value problem with oscillatory jump | contours, boundary values, jump matrix, normalization, solvability | title-level scope only |
| “Asymptotics for the MKdV equation” | reconstruct a modified-KdV solution and prove long-time asymptotics | PDE/scattering data, reconstruction map, asymptotic expansion and error | leading root candidate; theorem/page open |
| Percy Deift / Xin Zhou / 1993 | bibliographic identity | no proof credit | confirmed by official journal record |
| repository `已验证` | historical metadata | no source or machine evidence | rejected as assurance evidence |

## Statement and machine boundary

The article contains a method and multiple mathematical stages; its title does not select one
numbered theorem or determine all binders and boundary cases. An independent source reviewer must
choose the immutable edition and root theorem, map every premise and conclusion to pinpoint pages
and definitions, inspect corrections/errata, and distinguish imported inverse-scattering results
from results proved in the paper. Only then can the statement phase produce a canonical Lean target
and checked alternate encodings.

The repository-wide intake search found no theorem-specific Deift-Zhou or nonlinear-steepest-
descent Lean artifact. A narrow search of pinned mathlib found no matching Riemann-Hilbert,
modified-KdV, or oscillatory-jump theorem. These are scoped negative discovery results, not the
later immutable anchor audit. No formal candidate or machine status receives proof credit here.
