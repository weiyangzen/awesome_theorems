# Source-statement crosswalk

## Repository provenance

`Docs/researches/math_theorems.md:9775-9780` is the only repository source record. It gives the
title, attribution to many mathematicians, 20th-century date, Chinese gloss `解对参数的导数`, high
importance, and status `已验证`. The six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` and contain no citation.

`Docs/Stage0_Blueprint.md:36453-36478` projects the record as `THM-M-1340` while marking precise
definitions, premises, proof history, equivalent statements, axioms, and machine artifacts open.
Neither file is a primary mathematical source, and the verified label supplies no `H0` or machine-
proof credit.

## Inspected modern source candidate

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society (2012), DOI `10.1090/gsm/140`, Theorem 2.11 on
page 47, gives an exact modern member of the family. In the author-hosted preliminary edition,
`f in C^k(U x Lambda, Real^n)`, `k >= 1`, for an open state-time domain `U` and parameter set
`Lambda subset Real^p`. Around each `(t0, x0, lambda0)`, the local solution map
`phi(t, s, x, lambda)` is `C^k` on a suitable product neighborhood. The proof adjoins `lambda` as
a dependent variable with derivative zero. The next section derives a first-order sensitivity
equation for regular perturbations.

The inspected PDF has SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`. This is a credible modern
source candidate, but the repository does not select it, the theorem incorporates definitions and
existence results from earlier sections, and no errata audit or independent review has approved its
identity as the canonical target. It therefore supports `H1`, not `H0`.

## Component crosswalk

| Catalogue/source component | Mathematical choice still required | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| solution | local solution of `x' = f(t,x,lambda)` through source-selected data | `IsIntegralCurveOn` or a source-faithful solution-map predicate | ODE family fixed; construction and domain open |
| parameter | external `lambda`, its space, domain, and quantifier scope | a normed parameter type and functions curried in `lambda` | must be distinguished from time and initial data |
| differentiability | partial derivative, Frechet derivative, or joint `C^k` regularity | `HasFDerivAt`, `HasFDerivWithinAt`, `DifferentiableAt`, or `ContDiff` | exact strength and boundary convention open |
| derivative | existence alone or identification by a sensitivity equation | continuous-linear derivative plus a checked ODE relation | conclusion boundary with `THM-M-1341` open |
| modern Theorem 2.11 | local joint `C^k` solution map in finite dimensions | product-space solution map and `ContDiff` | strong candidate, not repository-selected canonical claim |
| `已验证` | claimed formal status | no proposition or kernel evidence | explicitly untrusted under rev-5.6 |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.ODE.Basic` exposes `IsIntegralCurveOn` and `IsIntegralCurveAt`, while
`Mathlib.Analysis.ODE.PicardLindelof` supplies local existence interfaces. The calculus library
exposes Frechet differentiability predicates such as `HasFDerivAt` and `DifferentiableAt`.
`IntakeProbe.lean` authenticates only these names in the pinned environment.

A bounded repository and pinned-mathlib search found no ODE result expressing differentiability of
the solution map in an external parameter or deriving its sensitivity equation. This negative
search is not the later immutable external anchor audit. The adjacent interfaces do not justify
`M3`, because no theorem-specific statement, reduction bridge, or root declaration is present;
machine status remains `M4`.

## Required follow-up

Before statement or `H0` acceptance, a source reviewer must select an immutable primary or
authoritative theorem, include all referenced definitions and existence hypotheses, transcribe its
ordered binders and conclusion, audit corrections, resolve the boundaries with `THM-M-1339` and
`THM-M-1341`, and obtain independent review. The statement phase must then elaborate and fingerprint
one exact Lean target, check every credited alternate encoding, and run all mandated mutations.
