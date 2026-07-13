# THM-M-0120 proof-phase recheck

Item: `S56-M-0120-PROOF`  
Recheck date: 2026-07-14 (Asia/Shanghai)  
Base revision: `c45f3c7090cb4adf616d45e5414985f956e807b2`  
Base tree: `da6f991c07f11e8608ddc090af9356558d64d360`

## Verdict

`blocked`. This recheck found no legal positive proof body. The exact frozen
proposition is refutable, and the existing placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

kernel-checks again at trust level zero. Its model makes every explicit
geometric proposition hypothesis true for a proper identity morphism but uses
the numerical data `N1 = Real`, `moriCone = {-1}`, `canonicalPairing = id`, and
`RationalCurve = Empty`. The required decomposition of `-1` then forces both
`z0 = -1` and `0 <= z0`.

This is a counterexample to the frozen formal encoding, not to the mathematical
Mori cone theorem. A proof of a repaired or narrowed proposition cannot be
substituted during this proof item. The item remains `[ ]`; no receipt is
accepted, no proof state is proposed, and neither audit nor theorem completion
is claimed. The predecessor graph remains unreconciled at `M3`/`M4`; this proof
attempt exposes an `M5` statement mismatch without editing predecessor state.

## Failed Gate And Retry

The first failed gate is exact-target consistency. `S56-M-0120-STATEMENT` must
be reopened and replace the unconstrained stand-ins with intrinsic definitions
or noncircular laws connecting the projective klt pair to its actual numerical
curve space, effective cone, canonical pairing, rational curves, and
contractions. Assuming `Conclusion` or one of its output packages would be
circular. A repaired statement needs a new accepted expression fingerprint and
obligation-registry version, followed by a fresh anchor audit and proof run.

## Validation

All checks used the existing pinned Lake closure. No update, build, fetch,
clone, or dependency mutation was performed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39, planned lifecycle, theorem incomplete |
| isolated `lake env lean -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C .lake/packages/mathlib rev-parse HEAD` from `Formalizations/Lean` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' ../../Stage1_Instances/THM-M-0120/Proof.lean` from `Formalizations/Lean` | 1 | no matches; exit 1 is ripgrep's no-match result |
| `python3 -m json.tool Stage1_Instances/THM-M-0120/proof-blocker-2026-07-14.json` | 0 | existing structured blocker is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0120` | 0 | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
tmp=$(mktemp -d ./.m0120-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-0120/Statement.lean \
  ../../Stage1_Instances/THM-M-0120/Proof.lean "$tmp/"
lake env lean -t0 -o "$tmp/Statement.olean" "$tmp/Statement.lean" &&
  LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
    lake env lean -t0 "$tmp/Proof.lean"
```

Input SHA-256 values were unchanged: statement
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`,
proof witness
`e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`,
registry `cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`,
typed graphs
`9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`,
and anchor audit
`71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

No `.stage1-worker-selftest.json` is written because the assigned positive
proof deliverable is blocked rather than genuinely self-tested as complete.
