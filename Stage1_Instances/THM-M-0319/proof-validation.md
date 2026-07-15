# THM-M-0319 proof-phase attempt

Item: `S56-M-0319-PROOF`  
Base revision: `4e04f1277aeb8c718b61049fd1af49b0ab00d882`  
Date: `2026-07-15` (`Asia/Shanghai`)

## Verdict

`blocked`: the exact external Brouwer body can be ported to the pinned Lean environment, but it
cannot truthfully be copied into this repository without a license grant. The immutable archive for
`harfe/fixed-point-theorems-lean4@11a9f041246d28374edae384241757f9a0cbd5e4` contains no
`LICENSE`, `COPYING`, `NOTICE`, source license header, SPDX identifier, or other redistribution and
modification permission. It is also absent from the pinned Lake dependency graph. Repository policy
makes an unresolved license a repo-local integration blocker, so none of the derived port was copied
into the owned path and no dependency was added or fetched.

This is a legal/provenance blocker, not a failed mathematical or Lean proof. Using the immutable
source already present in temporary audit storage from the prerequisite audit, a compatibility experiment ported
the exact five-module Brouwer closure to Lean 4.29/mathlib `8a178386`. All five modules elaborated
from source with `--trust=0`; the exact wrapper inhabited the unchanged
`Stage1Instances.THM_M_0319.BrouwerFixedPointTarget`. `assert_no_sorry` accepted both the terminal
and wrapper declarations, the source scan found no prohibited proof escape, and Lean reported only
`propext`, `Classical.choice`, and `Quot.sound`.

These temporary checks establish technical feasibility only. They do not pin, import, or vendor the
proof body, do not close `M0319-X-INTEGRATION` or `M0319-T-EXTERNAL`, and do not justify `M0-*` or
theorem-completion credit. Because the assigned proof deliverable is incomplete,
`.stage1-worker-selftest.json` is deliberately absent and the root remains `[H1, M3, R4]`.

## Validation evidence

All repository commands ran in this worker clone. Proof replay wrote only to a fresh temporary tree and read the
automation-provided canonical `.lake` symlink. No `lake update`, `lake build`, dependency clone or
fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0319` | 0 | rank 685, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0319/check_obligation_tree.py` | 0 | frozen 12-obligation, 31-edge architecture passed; open root and denominator `9d15b5ea...cee8` unchanged |
| Sequential use of the Lean binary and `LEAN_PATH` returned by `lake env` to replay the frozen `Statement.lean`, `cubical_sperner_prep`, `cubical_sperner`, `apply_cubical_sperner`, `convex_homeos`, `brouwer`, and the exact wrapper at `--trust=0` in temporary tree `m0319-exact-proof-replay.tfkOdP` | 0 for every source | all sources elaborated; the wrapper imported `Statement` and proved its canonical target; `assert_no_sorry` accepted the terminal and wrapper; both declarations reported only the allowed three axioms; log SHA-256 `61b1bd6c...5c99` |
| `rg -n '\b(sorry\|admit\|sorryAx\|axiom\|unsafe\|implemented_by\|native_decide\|extern)\b'` on the five temporary proof modules and wrapper | 1 | expected no-match result: no prohibited proof escape; normalized scan log SHA-256 `fd10ec45...106d4` |
| `sha256sum "$ARCHIVE"` | 0 | immutable audit archive SHA-256 `08749ae7e97b6125a68ae89e1a5ef59e3a2c9793bb850d6ae3b5d96bb2388d70`; 25,969 bytes |
| `tar -tzf "$ARCHIVE"` plus license-name and source-header scans | 0 for listing, 1 for both expected no-match scans | archive has no license artifact and its sources have no license grant |
| `python3 -m json.tool Stage1_Instances/THM-M-0319/proof-blocker.json` | 0 | structured blocker parses |
| `git diff --check -- Stage1_Instances/THM-M-0319` | 0 | no whitespace diagnostics |

The five ported proof sources total 2,986 lines. Their ordered SHA-256 values are recorded in
`proof-blocker.json`; the fresh replay ran from `2026-07-15T08:52:43,735033859+08:00` through
`2026-07-15T08:53:04,892793922+08:00`. Its exact wrapper SHA-256 is
`a4d01c794b76d77c65c8b8259ffa5d4a1a82bb9faae1e5f882898e1d10f466c2`, and its combined replay log
has SHA-256 `61b1bd6ca17c0f62c2189059604c2f00c7be80eb1c196e2427ec4a3b63115c99`.
The replay compiled the copied frozen statement first, then the five sources in import order, then
the wrapper. The core command form was:

```bash
LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
BASE_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_PATH="$TMP:$BASE_PATH" "$LEAN_BIN" --trust=0 --root "$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
for module in cubical_sperner_prep cubical_sperner apply_cubical_sperner convex_homeos brouwer; do
  LEAN_PATH="$TMP:$BASE_PATH" "$LEAN_BIN" --trust=0 --root "$TMP" \
    -o "$TMP/FixedPointTheorems/$module.olean" \
    "$TMP/FixedPointTheorems/$module.lean"
done
LEAN_PATH="$TMP:$BASE_PATH" "$LEAN_BIN" --trust=0 --root "$TMP" \
  "$TMP/ProofWrapper.lean"
```

The final wrapper output contains:

```text
'brouwer_fixed_point' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_0319.Proof.brouwerFixedPoint' depends on axioms: [propext, Classical.choice, Quot.sound]
exit=0
```

## Reopen condition

Obtain a license or explicit permission compatible with pinning and adapting the immutable external
commit, then place its five-module Brouwer closure in the repository validation closure with full
provenance and replay the checked exact wrapper. A genuinely independent local proof or another
licensed immutable exact proof body would also reopen the node. Until then the proof item, downstream
validation and release, master acceptance, audit completion, and theorem completion remain open.
