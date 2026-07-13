# THM-M-0120 proof-phase recheck at current base

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `504e508e93fd30c552d715ef48be068d5e131df2`

Base tree: `745f1603c60b7bb726e7789f08a6170c82621b6a`

The tracked owned path was clean at preflight. The only worktree entry was the
automation-provided untracked `Formalizations/Lean/.lake` symlink to the canonical pinned
dependency cache. It was reused read-only, making this nonrelease evidence.

## Verdict

`blocked`. No truthful positive proof body exists for the exact frozen proposition. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

kernel-checks at trust level zero. Any universe-polymorphic positive proof of the frozen target
would specialize to universes `(0, 0, 0, 0)` and contradict this declaration.

The countermodel takes the base field to be `AlgebraicClosure Rat`, uses the proper identity
morphism on its spectrum, and makes every explicit geometric proposition hypothesis true. The
statement nevertheless permits independent numerical data: `N1 = Real`, `moriCone = {-1}`,
`canonicalPairing = LinearMap.id`, and `RationalCurve = Empty`. Applying the required decomposition
equivalence to `-1` produces `z0` in the nonnegative part and in `{-1}`, forcing both `z0 = -1` and
`0 <= z0`, a contradiction. Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for
the refutation.

This refutes the frozen abstract encoding, not the mathematical Mori cone theorem. Adding the
missing geometric semantics during this phase would change the frozen target; assuming
`Conclusion` or one of its output packages would be circular. No positive proof body, proof
receipt, or obligation closure was added. The item remains `[ ]`, lifecycle remains `planned`, and
the authoritative root remains `[H2, M3, R4]`; `[H5, M5, R4]` is only the proposed diagnosis for
the refutable encoding. Audit completion, theorem completion, release, and master acceptance are
not claimed. `.stage1-worker-selftest.json` is deliberately absent because the requested proof
phase is not complete.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY` at `M0120-S-DATA` and
`M0120-S-BOUNDARY`. The frozen proposition admits data satisfying every input hypothesis while
refuting `Conclusion`. The remaining root cut set for this blocker is those two statement nodes.

Retry only after reopening `S56-M-0120-STATEMENT`, replacing the disconnected proposition and
numerical-data stand-ins with intrinsic definitions or noncircular laws tied to the actual
projective klt pair, accepting a new exact expression fingerprint and obligation-registry version,
then rerunning the anchor audit, obligation-tree freeze, and proof phase.

## Validation

All checks ran in this worker clone against the existing pinned Lake artifacts. No `lake update`,
`lake build`, dependency clone/fetch, network access, or `.lake` mutation was performed. Temporary
Lean sources and objects were created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | Rank 39; planned lifecycle; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0120/check_statement.py` | 0 | Three mutations killed; expression SHA-256 `074d45c3...d88cfd`; pinned toolchain/mathlib matched. |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | Immutable local candidates, clean pinned mathlib, eight probes, and M3 boundary agreed. |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; root remains M3. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | Exact statement and countermodel elaborated; axiom report was `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|unsafe' Stage1_Instances/THM-M-0120 -g '*.lean'` | 1 | Expected no-match exit; no prohibited token occurs in owned Lean sources. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact isolated Lean recipe, run from `Formalizations/Lean`:

```bash
set -u
repo_root=$PWD/../..
target=$repo_root/Stage1_Instances/THM-M-0120
tmp=$(mktemp -d /tmp/thm-m-0120-proof-504e508e.XXXXXX)
log=$(mktemp /tmp/thm-m-0120-proof-504e508e-log.XXXXXX)
trap 'rm -rf "$tmp" "$log"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
base=$(lake env printenv LEAN_PATH)
{
  LEAN_NUM_THREADS=1 lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Statement.olean" "$tmp/Statement.lean"
  LEAN_PATH="$tmp:$base" LEAN_NUM_THREADS=1 \
    lake env lean --trust=0 -t0 --root="$tmp" "$tmp/Proof.lean"
} >"$log" 2>&1
status=$?
cat "$log"
printf 'KERNEL_OUTPUT_SHA256='; sha256sum "$log" | cut -d' ' -f1
printf 'STATEMENT_OLEAN_SHA256='; sha256sum "$tmp/Statement.olean" | cut -d' ' -f1
printf 'LEAN_RECHECK_EXIT=%s\n' "$status"
exit "$status"
```

The complete captured Lean output had SHA-256
`19d53d6a657e000a6c2cfd7f6cf0a5e34ffb70112eca7beb74a243e2b472cc59`; the temporary
`Statement.olean` had SHA-256
`f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16` before cleanup.

The source inputs were `Statement.lean` SHA-256
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, `Proof.lean`
SHA-256 `e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`, registry
SHA-256 `cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`, typed graphs
SHA-256 `9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`, and anchor audit
SHA-256 `71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.
