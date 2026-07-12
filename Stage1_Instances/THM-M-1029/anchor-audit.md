# Anchor audit record

Item: `S56-M-1029-ANCHOR_AUDIT`  
Base revision: `81c766970d38b9ae3179b58cc75a46425a624c6e`  
Audit date: 2026-07-12

## Decision

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides the exact
`Martingale`, `Indep`, `HasLaw`, and `gaussianReal` interfaces used by the frozen statement. A
case-insensitive source scan found no Brownian/Wiener object, stochastic quadratic-variation API,
or Levy martingale-characterization theorem in its probability tree. The Levy hits that do exist
are the unrelated generalized Borel-Cantelli and upward theorems. `AnchorAudit.lean` checks the
required interfaces against the pinned environment without asserting a terminal result.

The strongest credible external candidate is `RemyDegenne/brownian-motion` at immutable commit
`bdf5ea0c34f9e6d75bce5f0609a968d6e9e99e8e`. Its Brownian module supplies
`IsFilteredPreBrownian`, `IsBrownianReal`, and the forward theorem
`IsPreBrownianReal.isMartingale`; its stochastic-integral branch defines `quadraticVariation`.
Neither inspected relevant module states the converse Levy characterization. The project is not
in this repository's manifest and is on Lean 4.31 with mathlib `fabf563...`, rather than the local
Lean 4.29/mathlib `8a1783...` closure. It is therefore a valuable future API source, not an exact
external proof or an integration obligation.

The repository-local `S1_M_222.lean` is also non-terminal: its conclusion contains abstract
proposition fields and its own documentation disclaims a Levy proof. The audit consequently keeps
the root at `M3 / formalization_debt`. It does not claim that no proof exists anywhere: anonymous
GitHub code search returned HTTP 401, and repository metadata plus relevant-module inspection is
not exhaustive search.

## Commands and results

Commands ran in this worker clone on 2026-07-12. Lean ran from `Formalizations/Lean` against the
existing canonical `.lake` artifacts; no dependency update, clone, fetch, or installation ran.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1029/AnchorAudit.lean` | 0 | pinned martingale, independence, law, and Gaussian interfaces elaborated and printed |
| `rg -ni "brownian|wiener|levy|lévy|quadratic.?variation|quadraticVariation" .lake/packages/mathlib/Mathlib/Probability --glob '*.lean'` | 0 | 11 hits, all unrelated Levy Borel-Cantelli/upward references; no Brownian or quadratic-variation declaration |
| `git -C .lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a1783...a95`, tree `bdc39a...2b` |
| `sha256sum` on three mathlib sources, license, frozen statement, and legacy source | 0 | hashes recorded in `anchor-audit.json` |
| GitHub repository API queries for Brownian/Levy/stochastic-calculus Lean projects | 0 | counts `2, 2, 0, 0, 1`; `incomplete_results=false` |
| GitHub commit/tree/content API for `RemyDegenne/brownian-motion` | 0 | immutable commit/tree, toolchain, manifest, license, relevant declarations, and source hashes recorded |
| GitHub code-search API query | 22 | HTTP 401 without authentication; recorded as an access limitation |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard projection passed |
| `python3 scripts/stage1_target.py check` | 0 | all 1546 targets and uniform L0 baseline passed |
| `python3 scripts/stage1_target.py show THM-M-1029` | 0 | rank 222, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1029/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1029 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This anchor-audit node is self-tested pending master acceptance. It establishes a versioned
negative/partial candidate inventory, not kernel closure: `H2, M3, R4` remain unchanged. The next
proof architecture must account for the characteristic-function or exponential-martingale bridge,
Gaussian increment laws, and independence from the past. No H0, proof, full audit completion, or
theorem completion is claimed.
