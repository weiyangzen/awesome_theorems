# Anchor audit validation record

Item: `S56-M-1016-ANCHOR_AUDIT`  
Base revision: `350ffc25f193b3d2ac0fcc9f4d760879cfae0f58`  
Audit date: 2026-07-12

## Decision

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` has the continuous mapping
theorem, a Slutsky-style convergence-in-measure perturbation theorem, and the Frechet derivative
interfaces needed to begin a proof. Source and declaration searches found no terminal delta-method
theorem. `AnchorAudit.lean` checks those nearby interfaces against the pinned environment without
asserting the canonical target.

The repository-local legacy file `S1_M_295.lean` contains a kernel-checked one-dimensional bridge,
but only after a negligible remainder is supplied explicitly. Its own `TaylorRemainderPackage`
retains the missing product-to-zero result as a field, and its public scope is real-valued rather
than the frozen finite-dimensional Frechet target. It is classified `M2` partial proof evidence,
not an exact wrapper or terminal proof. The root therefore remains `M3`.

Anonymous GitHub repository metadata queries returned no candidate repositories. GitHub code search
returned HTTP 403 after the anonymous rate limit was exceeded, so the external result is explicitly
non-exhaustive. No external dependency was cloned, fetched, installed, or credited.

## Commands and results

All commands ran in this worker clone using the existing pinned Lake artifacts. No update, build,
dependency fetch, clone, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1016/AnchorAudit.lean` | 0 | six pinned convergence and Frechet-derivative interfaces elaborated and printed |
| `rg -ni "delta method|delta_method|deltamethod|TendstoInDistribution.*HasFDeriv|HasFDerivAt.*TendstoInDistribution" .lake/packages --glob '*.lean'` | 1 | no terminal delta-method candidate in any materialized pinned package source |
| analogous repository-local `rg` excluding `.lake` | 0 | only legacy `S1_M_295.lean`; inspected bridge and open Taylor-remainder boundary |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a1783...a95`, tree `bdc39a...2b` |
| `sha256sum` on three mathlib sources, mathlib license, legacy source, and frozen statement | 0 | hashes recorded in `anchor-audit.json` |
| four anonymous GitHub repository API queries | 0 | each returned count 0 with `incomplete_results=false` |
| anonymous GitHub code-search API query | 0 (HTTP 403 response recorded) | rate-limit access failure; not treated as negative evidence |
| `python3 Stage1_Instances/THM-M-1016/check_anchor_audit.py` | 0 | structured audit, immutable source hashes, classifications, and boundary passed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard projection passed |
| `python3 scripts/stage1_target.py check` | 0 | all 1546 targets and uniform L0 baseline passed |
| `python3 scripts/stage1_target.py show THM-M-1016` | 0 | rank 295, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1016/anchor-audit.json` | 0 | structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1016 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This node is self-tested pending master acceptance. It freezes and classifies the discovered machine
candidate inventory, but supplies no root proof, H0 decision, readable reconstruction, audit
completion, or theorem completion. Remaining work begins with concentration of `X_n` at `theta`,
the scaled Frechet remainder, a finite-dimensional bounded-in-probability product lemma, and
measurability/composition evidence.
