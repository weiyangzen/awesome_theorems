# THM-M-1237 anchor audit

Audit date: 2026-07-12. Item: `S56-M-1237-ANCHOR_AUDIT`. The canonical target is
`Stage1Rev56.THMM1237.Statement` in `Statement.lean`: the supercritical first-order
Morrey-Sobolev embedding on a bounded extension domain, with `p > n`, exponent
`alpha = 1 - n/p`, an almost-everywhere representative on the domain, Holder continuity on
its closure, and quantitative Holder and value bounds.

## Pinned mathlib

The existing Lake manifest pins mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with Lean 4.29.0. A source scan found one
substantive Sobolev family in `Mathlib.Analysis.FunctionalSpaces.SobolevInequality`:

| Declaration | What it proves | Exact-root fit |
|---|---|---|
| `MeasureTheory.lintegral_pow_le_pow_lintegral_fderiv` | Gagliardo-Nirenberg-Sobolev integral inequality for compactly supported `ContDiff` functions | No weak `W1pData`, representative, closure, or Holder conclusion |
| `MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one` | `L^(n/(n-1))` bound from an `L1` Frechet derivative | No; endpoint smooth compact-support inequality |
| `MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq` | `Lp'` estimate for `1 <= p < n` | No; its regime is explicitly subcritical, opposite to the root's `p > n` |
| `MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_le` and `...fderiv` | Bounded-support subcritical estimates | No continuous or Holder representative |
| `HolderOnWith.continuousOn` | Holder continuity implies continuity for positive exponent | Supporting API only; it consumes the conclusion the root must construct |

`AnchorAudit.lean` imports the exact modules and elaborates every declaration. The pinned source
contains no Morrey embedding declaration and no theorem connecting a weak derivative or Sobolev
object to `HolderOnWith`. Thus this revision supplies analytic and topology APIs, but no exact or
wrapper-ready root closure.

## External Lean 4 candidates

The external scan used immutable commit archives and did not clone, fetch, or alter `.lake`.

| Project and immutable revision | Candidate surface | Toolchain/license | Provenance and fit |
|---|---|---|---|
| `grunweg/SobolevSlobodeckij@88d0535ecf0d2c31dd7f53674919da0aa7c40c7b` | `SobolevSlobodeckij/Basic.lean`, including `MemSobolev`; README says deriving embedding is planned | Lean/mathlib v4.30.0; no license declared | Not closure. The archive has 27 placeholder/axiom token matches in Lean sources, including foundational work, and embedding is future work. |
| `Brsanch/sqg-lean-proofs-fourier@becfcdef6c3110f73bedccb68b76b6bc436a5d87` | `FourierAnalysis/KatoPonce/SobolevEmbedding.lean`; `norm_apply_le_tsum_mFourierCoeff`, `norm_le_tsum_mFourierCoeff` | Lean/mathlib v4.29.0; MIT | No placeholder tokens found. Proves a Fourier sup-norm bound for already-continuous complex functions on the two-torus, not a Holder representative for weak `W^{1,p}` Euclidean-domain data. |
| `abenenson/rellich-kondrachov@70f85d4c1bf99c6e7d61e8be4daa6f3664d08d23` | Euclidean/manifold `H1`, `L2` compactness, and `isCompactOperator_h1ToL2_riemannianVolume` | Lean/mathlib v4.29.1; Apache-2.0 | No placeholder tokens found. This is compact `H1 -> L2` embedding on compact Riemannian manifolds, without the supercritical exponent or Holder representative. |

The GitHub repository searches `sobolev language:Lean` and `morrey language:Lean` returned three
repositories and zero repositories respectively on the audit date; the third Sobolev result was
the Fourier project above. Repository-name search cannot exclude private, unindexed, or differently
named projects, so the negative conclusion is limited to the recorded search surface and revisions.

## Classification and handoff

- Root machine state remains `M3`: the exact statement elaborates, but no exact proof declaration or
  dependency closure was found. There is no discovered external exact closure and therefore no
  current `repo_local_integration_debt` to discharge.
- Machine debt is `formalization_debt`, not mathematical debt. The mathlib subcritical family may
  support later analytic leaves. The supercritical Morrey estimate, weak-derivative-to-representative
  bridge, and domain/closure restriction remain open proof obligations.
- Human/source status remains `H1`; this phase is not a primary edition/theorem/page/errata audit.
- Readability remains `R3`; no proof reconstruction is claimed.
- No candidate receives proof credit, no external archive is installed, and no theorem-completion
  claim is made.

## Validation record

Base revision: `a1b16ca3ed65db2ec65e3d478d1680d9c1f5489d`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1237/AnchorAudit.lean` (from `Formalizations/Lean`) | 0 | All six pinned declaration probes elaborated with their actual types |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned revision matched the manifest |
| `rg -n -i 'sobolev|morrey|holder.*continuous|weak.*deriv|distributional.*deriv' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Found the stated candidate surfaces and no exact Morrey-Sobolev declaration |
| `git ls-remote <project-url> HEAD` for the three external projects | 0 | Resolved the immutable revisions tabulated above |
| `curl .../archive/<revision>.tar.gz \| tar ...` scans | 0 | Inspected trees, toolchains, candidate source, and placeholder-token counts without installing dependencies |

This is self-tested anchor-audit evidence only, pending master acceptance of this node.
