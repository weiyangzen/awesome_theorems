# THM-M-0120 proof-phase recheck at base `5a080720`

Item: `S56-M-0120-PROOF`  
Intent: `prove`  
Recheck date: 2026-07-14 (Asia/Shanghai)  
Base revision: `5a080720059200b542aa35ee17a748b3251fe8d0`  
Base tree: `d7029aa7599db39fbcc55e968a4fe70376143f27`

## Verdict

`blocked`. No truthful positive proof body exists for the exact frozen proposition. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

kernel-checks at trust level zero. Its countermodel makes every explicit geometric proposition
hypothesis true for a proper identity morphism, while the statement leaves the numerical data
independent of those hypotheses: `N1 = Real`, `moriCone = {-1}`, `canonicalPairing = LinearMap.id`,
and `RationalCurve = Empty`. Applying the required decomposition equivalence to `-1` produces an
element `z0` of the nonnegative part with both `z0 = -1` and `0 <= z0`, a contradiction.

This refutes the current formal encoding, not the mathematical Mori cone theorem. A repaired,
narrower, or circularly strengthened proposition cannot be substituted for the assigned target.
The item remains `[ ]`; no positive proof body, provisional receipt, audit completion, theorem
completion, release, or master acceptance is claimed. The frozen predecessor registry still
records the root at `M3` and substantive geometric packages as open; this checked countermodel
supports a proposed `H5 / M5 / R4` exact-target-mismatch classification without rewriting the
authoritative `H2 / M3 / R4` predecessor state.

## Failed Gate And Retry

The first failed gate is exact-target consistency at `M0120-S-DATA` and `M0120-S-BOUNDARY`.
`S56-M-0120-STATEMENT` must be reopened and its stand-ins replaced by intrinsic definitions or
noncircular laws connecting the projective klt pair to its numerical curve space, effective cone,
canonical pairing, rational curves, and contractions. Assuming `Conclusion`, its decomposition
branch, or another required output package would be circular. Positive proof work may resume only
after a repaired target receives a new accepted expression fingerprint and obligation-registry
version, followed by a fresh anchor audit and proof execution.

## Scoped Validation

All successful checks ran in this worker clone using the existing pinned Lean artifacts. No update,
build, clone, fetch, or dependency mutation was performed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this dirty, nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned lifecycle; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_statement.py` | 0 | three structural mutations killed; expression SHA-256 `074d45c3...d88cfd`; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable local candidates, clean pinned mathlib, eight Lean probes, and the `M3` boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains `M3`; substantive packages remain open |
| isolated `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C .lake/packages/mathlib rev-parse HEAD` from `Formalizations/Lean` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `test -z "$(git -C .lake/packages/mathlib status --porcelain)"` from `Formalizations/Lean` | 0 | pinned mathlib worktree clean |
| placeholder scan below | 1 | no matches; exit 1 is ripgrep's no-match result |
| `python3 -m json.tool Stage1_Instances/THM-M-0120/proof-recheck-2026-07-14-head-5a080720.json` | 0 | current-base structured blocker is valid JSON |
| structured blocker invariant check | 0 | identity, base/tree, paths, hashes, blocked state, no receipts, failed gate, retry condition, and no completion claims agreed |
| `git diff --check -- Stage1_Instances/THM-M-0120` | 0 | no whitespace errors in the owned-path delta |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
tmp=$(mktemp -d ./.m0120-proof.XXXXXX)
log=$(mktemp /tmp/thm-m-0120-proof-log.XXXXXX)
trap 'rm -rf "$tmp" "$log"' EXIT HUP INT TERM
cp ../../Stage1_Instances/THM-M-0120/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-0120/Proof.lean "$tmp/Proof.lean"
base=$(lake env printenv LEAN_PATH)
{
  LEAN_NUM_THREADS=1 lake env lean --trust=0 -t0 \
    -o "$tmp/Statement.olean" "$tmp/Statement.lean"
  LEAN_PATH="$tmp:$base" LEAN_NUM_THREADS=1 \
    lake env lean --trust=0 -t0 "$tmp/Proof.lean"
} >"$log" 2>&1
status=$?
cat "$log"
printf 'LEAN_RECHECK_EXIT=%s\n' "$status"
exit "$status"
```

The relevant output was:

```text
'Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
LEAN_RECHECK_EXIT=0
```

The complete captured Lean output has SHA-256
`19d53d6a657e000a6c2cfd7f6cf0a5e34ffb70112eca7beb74a243e2b472cc59`; the emitted temporary
`Statement.olean` had SHA-256
`6366e8afb5ee0c61cb39d40931419fc3347591fc37066df80fd1a9d8d835cc4e` before cleanup.

Exact placeholder scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' \
  Stage1_Instances/THM-M-0120 -g '*.lean'
```

The content inputs at this base are unchanged: statement SHA-256
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, proof-witness
SHA-256 `e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`, registry
SHA-256 `cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`, typed graphs
SHA-256 `9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`, and anchor audit
SHA-256 `71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

No `.stage1-worker-selftest.json` is written because the assigned positive proof deliverable is
blocked rather than genuinely self-tested as complete.
