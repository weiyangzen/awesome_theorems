# THM-M-0120 proof-phase recheck at current base

Item: `S56-M-0120-PROOF`  
Recheck date: 2026-07-14 (Asia/Shanghai)  
Base revision: `67b1bf1758649d2be86775230c7d4bfe117ade2b`  
Base tree: `5f872831428a9d9805e61aad3868be443c29cef2`

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen proposition. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

kernel-checks at trust level zero. Its model makes every explicit geometric proposition hypothesis
true for a proper identity morphism, but the numerical fields remain unconstrained: `N1 = Real`,
`moriCone = {-1}`, `canonicalPairing = LinearMap.id`, and `RationalCurve = Empty`. Applying the
required decomposition to `-1` forces a nonnegative-part element `z0` with both `z0 = -1` and
`0 <= z0`.

This is a counterexample to the frozen formal encoding, not to the mathematical Mori cone theorem.
A repaired, narrowed, or circularly strengthened proposition cannot replace the assigned target.
The item remains `[ ]`; no proof body, receipt, audit-completion, theorem-completion, release, or
master-acceptance claim is made. The frozen predecessor graph remains unreconciled at `M3`/`M4`,
while this proof attempt establishes an `M5` exact-target mismatch.

## Failed Gate And Retry

The first failed gate is exact-target consistency. `S56-M-0120-STATEMENT` must be reopened and its
stand-ins replaced by intrinsic definitions or noncircular laws connecting the projective klt pair
to its numerical curve space, effective cone, canonical pairing, rational curves, and contractions.
Assuming `Conclusion` or any required output package is circular. A repaired target requires a new
accepted expression fingerprint and obligation-registry version, then a fresh anchor audit and proof
run.

## Validation

All checks ran in this worker clone using the existing pinned Lake closure. No update, build, fetch,
clone, or dependency mutation was performed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned lifecycle; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| isolated `lake env lean -t0` recipe below | 0 | exact statement elaborated; countermodel checked; axiom report `[propext, Classical.choice, Quot.sound]` |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C .lake/packages/mathlib rev-parse HEAD` from `Formalizations/Lean` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| placeholder scan shown below, from `Formalizations/Lean` | 1 | no matches; exit 1 is ripgrep's no-match result |
| `python3 -m json.tool Stage1_Instances/THM-M-0120/proof-blocker-2026-07-14.json` | 0 | structured blocker is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0120` | 0 | no whitespace errors after this artifact was added |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
tmp=$(mktemp -d ./.m0120-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-0120/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-0120/Proof.lean "$tmp/Proof.lean"
lake env lean -t0 -o "$tmp/Statement.olean" "$tmp/Statement.lean" &&
  LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
    lake env lean -t0 "$tmp/Proof.lean"
```

Exact placeholder scan, also run from `Formalizations/Lean`:

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
