# THM-M-0990 proof-phase validation

Item: `S56-M-0990-PROOF`  
Date: `2026-07-14` (`Asia/Shanghai`)  
Base revision: `64ac616628d97140f9ca64eff0298e51d7f4e9ff`

## Implemented proof

The exact frozen theorem now has a placeholder-free repo-local body:

```text
Stage1Instances.THM_M_0990.lyapunovCentralLimit_exact :
  Stage1Instances.THM_M_0990.StatementShape
```

`Normalization.lean` centers each `Fin n` row, transports moments and
independence, proves unit normalized variance on the eventual positive tail,
and identifies its sum with `normalizedRowSum`. `Proof.lean` proves the
`2 + delta` truncation bound and derives the exact Lindeberg condition from
the frozen Lyapunov ratio. `GeneralizedLindeberg.lean` then proves an
eventually normalized `Fin n` Lindeberg-Feller theorem by characteristic
functions, using `ProductLimit.lean` for product-to-exponential convergence,
and transports the Gaussian limit to the target variable `Y` through `hY`.

The analytic architecture is a repo-local eventual-normalization adaptation
of the checked `THM-M-0989` proof and ultimately of
`patrickrd/CLT-lindeberg` commit
`82249ccfc05c0d97b86f33fce2582f0bf4ff9c06`. Immutable source hashes and
Apache-2.0 lineage are recorded in `proof-receipt.json`. The dependency files
from `THM-M-0989` are copied into the isolated replay and re-elaborated; their
provisional state or receipt is not inherited as proof credit.

## Validation

The proof replay used the existing pinned artifacts read-only. It ran no
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0990` | 0 | rank 270; planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0990/check_obligation_tree.py` | 0 | 18 obligations and 43 typed edges; frozen denominator `fa799ae8...921f6` passed |
| `bash Stage1_Instances/THM-M-0990/check_proof.sh` | 0 | nine modules isolated and elaborated with Lean 4.29.0 `--trust=0`; all 24 public target theorems reported exactly `[propext, Classical.choice, Quot.sound]` |
| strict forbidden-device scan over target and imported dependency Lean sources | 1 | expected no-match result: no placeholder, custom axiom, opaque/unsafe/extern declaration, or native proof device |
| JSON parse and `git diff --check` over the owned path and worker packet | 0 | structured evidence parsed and no whitespace diagnostics were emitted |

The frozen obligation registry remains an intentionally unchanged pre-proof
snapshot, so its M3/open report is not an accepted-state update. This worker
proposes repo-local M0-L after master acceptance, while the authoritative
accepted vector remains H2/M3/R4.

## Boundary

This is a self-tested proof-phase proposal `[_]`, not an accepted receipt or
theorem-completion verdict. Full transitive provenance and TCB closure, H0,
R0, hermetic cold/offline replay, independent verification, validation,
release, `AUDIT-Z`, `THEOREM-Z`, and dependency-ordered master acceptance
remain open.
