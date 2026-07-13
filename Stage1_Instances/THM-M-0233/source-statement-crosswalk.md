# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1682-1687` supplies exactly the title `辐角原理`, Augustin
Cauchy, 1831, the gloss `全纯函数零点与极点个数公式`, high importance, and status `已验证`.
All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, edition,
theorem or page, formula, contour, function domain, definition, binder, hypothesis, conclusion,
proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:6464-6489` repeats the gloss and explicitly leaves precise definitions
and premises, equivalent statements, logical assumptions, machine status, and artifact links open.
The rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and resets this target to
`L0 / rework_required`.

## Inspected modern source lead

NIST Digital Library of Mathematical Functions, version 1.2.7 (released June 15, 2026), section
1.10(iv), paragraph "Phase (or Argument) Principle," equation 1.10.9, was inspected on 2026-07-13.
The observed section HTML had SHA-256
`605d1f8cddb8c4bf4ff9d2dd3da566f27f103586c06fdc544818a7fae3f9896a`; the equation's TeX
response had SHA-256 `ac880fe15cdce1bffdf22aa43d3a4234df29b24fde2f18889b5580bb67940e23`.
The DLMF errata page was also inspected; its SHA-256 was
`a99035dc32e51b17da018d37f7fb971e9ce74075bd627f4d5012a74bfbff555a`.
The linked version-1.2.0 change for section 1.10 concerns a new generating-functions subsection,
not equation 1.10.9, but a complete independent correction review is still open.

DLMF says that the contour is traversed positively; if the singularities inside `C` are poles and
`f` is analytic and nonvanishing on `C`, then

```text
N - P = (1 / (2*pi*i)) * integral_C (f'(z) / f(z)) dz
      = (1 / (2*pi)) * Delta_C phase(f(z)).
```

It defines `N` and `P` as the numbers of zeros and poles inside `C`, counted with multiplicity, and
describes the last term as the change in a continuous branch of the phase as `z` passes once around
`C` positively. DLMF is a strong authoritative source lead but not the catalog's cited source. Its
inherited simple-closed-contour, interior, analyticity/singularity, and integration definitions
must be transcribed exactly, an immutable lawful snapshot must be accepted, and an independent
reviewer must approve the mapping before H0.

## Component crosswalk

| Repository/source component | Mathematical content | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `全纯函数` / holomorphic function | conflicts literally with poles; may mean meromorphic or analytic except at poles | `MeromorphicOn f U`, `AnalyticOnNhd` off a finite pole set, or a checked equivalent | exact source definition and transport open |
| closed contour `C` | DLMF inherits a positively traversed simple closed contour and its interior | a future path/cycle interface; `circleIntegral` only handles circles | representation, regularity, interior, and orientation open |
| zeros `N` | enclosed zeros counted with multiplicity | positive meromorphic orders or positive part of `MeromorphicOn.divisor` | exact finite count and region restriction open |
| poles `P` | enclosed poles counted with multiplicity | negative meromorphic orders or negative divisor part | exact finite count and boundary exclusion open |
| logarithmic derivative | `f'(z) / f(z)` on the contour | `logDeriv f`; `MeromorphicOn.logDeriv` | pinned adjacent API authenticated; no terminal bridge |
| normalized integral | `(2*pi*i)^(-1) * integral_C (f'/f)` | future general contour integral, or `circleIntegral` in a circle specialization | general contour and signed-count identity absent |
| phase change | normalized continuous change of `phase(f(z))` | future winding/phase-lift interface | no exact pinned interface located |
| `已验证` | untrusted inventory label | no proposition or proof object | no H or M credit |

## Formal crosswalk boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
checks meromorphic orders/divisors, logarithmic derivatives, circle integrals, and Jensen's formula.
A bounded search over pinned mathlib and repo-local Lean found no named argument-principle theorem,
principle-of-the-argument theorem, or winding-number declaration. This does not establish absence
from external Lean projects and does not replace the downstream immutable anchor audit.

Before statement work can close, reviewers must select and preserve an exact source, incorporate
every contour and analytic definition, map every ordered binder and assumption, decide which of
the two DLMF equalities belongs to the root, settle all boundary cases and corrections, and approve
the source-to-canonical mapping. Only then may the Lean statement gate freeze minimal imports, an
elaborated expression and environment fingerprint, checked alternate transports, and the required
removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
