# THM-M-0120 proof-phase recheck at base 2aab6833

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `2aab68338c370228923a5f7aba2a10b328902eab`

Base tree: `cb6f7e43b6cb5a6b852dea13a3a42cc992176213`

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen proposition. The existing
repo-local, placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

kernel-checks with `--trust=0`. Its model gives a proper identity morphism all six explicit
geometric proposition hypotheses, while the frozen structure permits unrelated numerical data:
`N1 = Real`, `moriCone = {-1}`, `canonicalPairing = LinearMap.id`, and
`RationalCurve = Empty`. Applying the required decomposition to `-1` produces a nonnegative-part
element `z0` with both `z0 = -1` and `0 <= z0`, a contradiction.

This refutes the frozen formal encoding, not the mathematical Mori cone theorem. Proving a
repaired, narrower, or circularly strengthened proposition would substitute a different theorem
and is forbidden in this proof phase. The item remains `[ ]`; no positive proof body, provisional
receipt, audit completion, theorem completion, release, or master acceptance is claimed. The
authoritative predecessor vector remains `H2 / M3 / R4`; this proof attempt records an `M5`
exact-target mismatch without editing predecessor state.

## Failed Gate And Retry

The first failed gate is exact-target consistency. `S56-M-0120-STATEMENT` must be reopened and its
stand-ins replaced by intrinsic definitions or noncircular laws connecting a projective klt pair
to its numerical curve space, effective cone, canonical pairing, rational curves, and
contractions. Assuming `Conclusion` or any required output branch would be circular. Positive
proof work may resume only after a repaired expression fingerprint and obligation-registry version
are accepted and the anchor audit is rerun.

The remaining root cut set is therefore statement repair, klt and numerical-intersection
foundations, ray decomposition with rational generators, local finiteness, and contraction
existence and universality.

## Validation

All checks ran in this worker clone against the existing pinned Lake closure. No `lake update`,
`lake build`, dependency fetch/clone, or `.lake` mutation was performed. The automation-provided
untracked `Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| isolated `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C .lake/packages/mathlib rev-parse HEAD` from `Formalizations/Lean` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| placeholder scan below, from `Formalizations/Lean` | 1 | no matches; exit 1 is ripgrep's no-match result |
| `python3 -m json.tool Stage1_Instances/THM-M-0120/proof-blocker-2026-07-14.json` | 0 | existing structured blocker is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0120` | 0 | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
scratch=$(mktemp -d /tmp/thm-m0120-head-2aab6833.XXXXXX)
trap 'rm -rf "$scratch"' EXIT HUP INT TERM
cp ../../Stage1_Instances/THM-M-0120/Statement.lean "$scratch/Statement.lean"
cp ../../Stage1_Instances/THM-M-0120/Proof.lean "$scratch/Proof.lean"
base_path=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -R "$scratch" -t0 \
  -o "$scratch/Statement.olean" "$scratch/Statement.lean"
LEAN_PATH="$scratch:$base_path" LEAN_NUM_THREADS=1 timeout 300 \
  lake env lean --trust=0 -R "$scratch" -t0 "$scratch/Proof.lean"
```

Exact placeholder scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' \
  ../../Stage1_Instances/THM-M-0120/Proof.lean
```

Input SHA-256 values at this base are: statement
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, proof witness
`e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`, registry
`cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`, typed graphs
`9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`, and anchor audit
`71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

No `.stage1-worker-selftest.json` is written because the assigned positive proof deliverable is
blocked rather than genuinely self-tested as complete.
