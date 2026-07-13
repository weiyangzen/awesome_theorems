# THM-M-1474 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10756-10761` supplies exactly the title
`von Neumann稳定性分析`, attribution to John von Neumann, year 1947, gloss
`有限差分的稳定性分析`, importance `high`, and status `已验证`. All six uncited lines
originate in repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains
no equation, scheme, grid, stability predicate, Fourier convention, amplification condition,
hypothesis, conclusion, theorem/page locator, proof, erratum record, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:40081-40105` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, alternate forms, axioms, machine status, and artifact
links open. Its generic closed-result and leaf-audit wording is planning metadata, not source
evidence. Rev-5.6 retains `已验证` only as untrusted metadata and resets this target to
`L0 / rework_required`.

## Inspected source-family lead

Randall J. LeVeque, *Finite Difference Methods for Ordinary and Partial Differential Equations:
Steady-State and Time-Dependent Problems*, SIAM, 2007, DOI
`10.1137/1.9780898717839`, ISBN `978-0-898716-29-0`, is an authoritative modern locator for
the family. Crossref metadata, the author-hosted companion page, its six-page table of contents,
and the author-hosted errata were observed on 2026-07-13.

The contents distinguish Section 9.6, `von Neumann analysis`, page 197, for diffusion/parabolic
problems from Section 10.5, `Von Neumann analysis`, page 219, for advection/hyperbolic problems.
They separately list scheme-specific stability analyses and Section 10.7, the CFL condition. The
errata also includes a material correction to equation (10.48) on page 222. This confirms that the
catalog gloss spans multiple definitions and results rather than identifying one root proposition.

This source-family lead is not `H0`: the catalog does not cite it; no full theorem passage,
incorporated definition chain, assumptions, proof boundary, or correction impact has been selected
and crosswalked; and no independent reviewer has admitted a root statement.

## Literal statement crosswalk

| Repository component | Required mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| von Neumann stability analysis | a criterion or analysis theorem with its logical direction | exact proposition and ordered quantifiers | method family only; necessity/sufficiency/equivalence open |
| finite differences | PDE, grid, stencil, recurrence, coefficients, and boundary closure | indexed state space and update operator/scheme | all absent |
| Fourier modes | transform domain, normalization, frequencies, and Plancherel bridge | finite/infinite lattice Fourier model and checked norm transport | all open |
| amplification | scalar factor, matrix symbol, or characteristic roots | source-identical symbol declaration | representation and hypotheses open |
| stability | norm, time horizon, mesh-uniform bound, and parameter range | quantified norm/power estimate | predicate and constants absent |
| John von Neumann, 1947 | historical attribution | provenance only | no work, edition, passage, or immutable source supplied |
| verified | inventory screening label | accepted source/kernel receipt | explicitly rejected as evidence |

The literal record cannot populate a canonical domain, ordered binders, hypotheses, conclusion,
alternate encodings, excluded cases, or Lean expression fingerprint.

## Pinned Lean crosswalk

| Candidate | What the pinned declaration supplies | Why it is not the target |
|---|---|---|
| `MeasureTheory.Lp.fourierTransformₗᵢ` | Fourier transform on continuous `L2` as a linear isometry equivalence | no discrete grid, recurrence, or symbol |
| `MeasureTheory.Lp.norm_fourier_eq` | a Plancherel norm equality | no finite-difference update or stability criterion |
| `spectralRadius` | abstract spectral radius in a normed algebra | no amplification matrix or uniform power conclusion |
| `spectrum.spectralRadius_le_nnnorm` | spectral radius bounded by norm | the inequality direction alone cannot turn spectral-radius control into scheme stability |

`IntakeProbe.lean` checks these declarations at the pinned revision. A bounded exact-topic search
located no source-selected terminal theorem. The probe is discovery evidence only, not a canonical
target, proof body, exhaustive anchor audit, or absence proof.

## Source gate

The first downstream gate requires an accountable correction that selects and preserves one exact
source proposition; maps the equation, domain/data, grid, stencil, recurrence, coefficients,
boundary treatment, stability norm and horizon, frequency set, symbol type, amplification/power
condition, logical direction, constants, quantifier order, arithmetic model, and degenerate cases;
audits the incorporated proof and errata; and receives independent numerical-analysis and source
review. Only then may the statement phase freeze the Lean expression, minimal imports, checked
transports, and required mutations.

Until then, `H5` records that the catalog target is not yet a stable truth-valued proposition,
`M4` records the lack of a source-identical usable formal artifact, and `R4` records the lack of
an anchorable proof reconstruction. These classifications do not say that established von Neumann
stability results are false or open.
