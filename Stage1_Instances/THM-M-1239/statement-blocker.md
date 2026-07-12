# Exact-statement gate: blocked

Item: `S56-M-1239-STATEMENT`  
Theorem: `THM-M-1239`  
Base revision: `854537bcbb10ad4c68b5a61f06171fffcec64961`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
complete mathematical wording is only "Poincare inequality" in the PDE/Sobolev category, glossed
as "an L^p estimate for Sobolev functions." The record gives no theorem-level primary source,
edition, page, or exact statement. In particular, it does not fix:

- the ambient dimension and scalar field;
- the domain, its boundedness or connectedness, and its boundary regularity;
- the exponent range or endpoint conventions;
- the Sobolev-space and weak-gradient definitions;
- a zero-trace condition, compact support, or subtraction of the integral mean;
- the two norms and the dependence or normalization of the constant;
- treatment of disconnected, unbounded, zero-measure, constant-function, or endpoint cases.

These choices distinguish non-equivalent theorems. For example, a bound on `u` for a zero-trace
Sobolev function is not the same statement as a bound on `u - average u` on a connected bounded
domain. Nor may mathlib's compact-support Gagliardo-Nirenberg-Sobolev inequality be relabeled as
this target: it relates exponents by dimension and is a distinct theorem family. Selecting any one
of these formulations from mathematical preference would substitute for the source claim, which
rev-5.6 forbids.

Consequently there is no canonical formal expression whose imports can be minimized, no honest
normalized expression hash, no checked alternate encoding, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary mutation suite. The intake's `M4` classification
therefore remains unchanged. No theorem declaration, assumption of the desired inequality,
weakened special case, or proof-status claim was introduced.

## Pinned Lean boundary

`StatementProbe.lean` elaborates the nearest independent analysis substrate using the single
declared import `Mathlib.Analysis.FunctionalSpaces.SobolevInequality`. It checks `eLpNorm`,
`fderiv`, and mathlib's `eLpNorm_le_eLpNorm_fderiv_of_eq` and
`eLpNorm_le_eLpNorm_fderiv_of_le`. This proves only that pinned mathlib exposes norm, derivative,
and Gagliardo-Nirenberg-Sobolev APIs. It neither identifies nor elaborates the missing Poincare
claim and receives no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation record

Commands were run from this worker clone on 2026-07-12. Lean used the existing pinned `.lake`
artifacts; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1239` | 0 | Rank 420, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1239/StatementProbe.lean` | 0 | All four substrate declarations elaborated and printed their types; no canonical target was declared |
| repository and pinned-mathlib `rg` searches for Poincare and Sobolev inequality forms | 0 | Found the separate probability target, abstract legacy predicates, the Gagliardo-Nirenberg-Sobolev module, and no source-frozen PDE Poincare proposition for this target |
| `git diff --check -- Stage1_Instances/THM-M-1239` | 0 | No whitespace errors |

## Retry condition

An accountable source decision must supply an immutable primary-source edition and pinpoint
statement, resolve errata, and freeze every domain, function-space, exponent, normalization,
gradient, norm, constant, and boundary convention listed above. A later statement run can then
encode that exact claim, minimize its pinned imports, serialize the elaborated expression and
environment fingerprints, compile checked transports, and execute all four mutation classes.

First failed gate: rev-5.6 section 5 exact source-statement identity. The assigned phase is not
genuinely self-tested to completion, so no `.stage1-worker-selftest.json` is emitted. This artifact
does not claim statement acceptance, audit completion, or theorem completion.
