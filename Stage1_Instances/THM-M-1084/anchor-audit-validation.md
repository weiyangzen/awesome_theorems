# Anchor-audit validation

Item: `S56-M-1084-ANCHOR_AUDIT`  
Audit date: `2026-07-12`  
Base revision: `dfacb54b5f277adf642e7658a065015f486d4cf2`

## Decision

The repo-local search found only the frozen proposition. Pinned mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` provides checked Gaussian-process,
covering-number, and finite pair-reduction infrastructure, but no Dudley
expected-supremum entropy theorem.

The public search located a substantive external near candidate:
`YuanheZ/lean-stat-learning-theory`, `SLT.Dudley.dudley`, at immutable commit
`be5d5a8a1a1f46f2ec9502980ff10a39e17e3820`. Its terminal body invokes
`dudley_chaining_bound_countable`, and the audited source has no proof-placeholder token. It is not
the frozen target: it assumes a sub-Gaussian MGF process, sample continuity, coordinate
measurability, exponential integrability, and a probability-measure instance; uses closed-ball
`WithTop Nat` covering numbers and `(0,D]`; and concludes a bound with constant
`12 * sqrt 2 * sigma` without the target's supremum-integrability conjunct. Its Lean/mathlib pins
also differ from this repository. It is therefore `M1_external_upstream_anchor_only`, not `M0-P`.

## Commands and results

No `lake update`, dependency build, clone, or fetch was run. All local Lean checks used the existing
pinned artifacts.

| Command | Exit | Result |
|---|---:|---|
| `rg -n -i --glob '*.lean' 'dudley|entropy (bound|integral)|metric entropy|generic chaining|chaining|coveringNumber|covering_number' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | covering-number and pair-reduction substrate found; no pinned Dudley theorem |
| `rg -n -i --glob '*.lean' 'Dudley|entropy bound|generic chaining' --glob '!Formalizations/Lean/.lake/**' .` | 0 | only this target and unrelated entropy text; no repo-local proof |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| Sourcegraph query `context:global archived:yes fork:yes Dudley lang:Lean count:100` | 0 | found `YuanheZ/lean-stat-learning-theory` at `be5d5a8...`; shard match limit recorded, so saturation is not claimed |
| Sourcegraph query scoped to `YuanheZ/lean-stat-learning-theory` for `sorry OR admit OR axiom` | 0 | two incidental English uses outside the Dudley dependency surface; no proof placeholder reported |
| immutable raw-source inspection and SHA-256 of `SLT/Dudley.lean`, `MetricEntropy.lean`, `SubGaussian.lean`, `CoveringNumber.lean`, `lean-toolchain`, and `lake-manifest.json` | 0 | exact theorem/type, terminal invocation, conventions, Lean `v4.27.0-rc1`, mathlib `d68c4dc...`, and hashes recorded in `anchor-audit.json` |
| `python3 Stage1_Instances/THM-M-1084/check_anchor_audit.py` | 0 | bounded inventory, six Lean probes, revisions, and fail-closed flags agree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1084/AnchorAudit.lean` | 0 | six pinned substrate declarations and two negative-completion guards elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1084/Statement.lean` | 0 | exact comparison target re-elaborated and printed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique ordered targets |
| `python3 scripts/stage1_target.py show THM-M-1084` | 0 | rank 526; L0/rework-required; planned; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1084/anchor-audit.json` | 0 | JSON valid |
| `git diff --check -- Stage1_Instances/THM-M-1084 .stage1-worker-selftest.json` | 0 | no whitespace errors |

GitHub REST repository searches completed with zero results before later commit/tree calls hit the
unauthenticated API limit. Commit-qualified raw URLs remained available. The repository root
`LICENSE` path returned HTTP 404 although the inspected source headers declare Apache-2.0; this is
retained as a release-level license-verification gap, not hidden.

## Status boundary

This is self-tested anchor-audit evidence pending master acceptance. It does not modify generated
state, integrate the external project, prove an exact bridge, establish `H0`, claim `AUDIT-Z`, or
claim theorem completion.
