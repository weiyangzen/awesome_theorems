# THM-M-0120 proof-phase recheck at base `ffea62ba`

Item: `S56-M-0120-PROOF`  
Intent: `prove`  
Recheck date: 2026-07-14 (Asia/Shanghai)  
Base revision: `ffea62ba1a7c0b0f84d70fd07f87d3eef57fe330`  
Base tree: `4662e08d189bd534919775f750c6909591aeafcb`

## Verdict

`blocked`. The exact frozen proposition cannot receive a truthful positive proof body: the existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

kernel-checks in the pinned environment. Its countermodel makes every explicit input proposition
true for a proper identity morphism, while the statement leaves its numerical data independent of
those propositions: `N1 = Real`, `moriCone = {-1}`, `canonicalPairing = LinearMap.id`, and
`RationalCurve = Empty`. Applying the required decomposition to `-1` produces a nonnegative-part
element `z0` satisfying both `z0 = -1` and `0 <= z0`.

This refutes the frozen formal encoding, not the mathematical Mori cone theorem. Proving a repaired,
narrower, or circularly strengthened proposition would substitute a different target and is not a
legal completion of this item. The item therefore remains `[ ]`; no positive proof body, worker
self-test, receipt, audit completion, theorem completion, release, or master acceptance is claimed.
The predecessor registry still reports root `M3` with every substantive geometric package open;
the countermodel establishes an `M5` exact-target blocker without changing predecessor state.

## Failed Gate And Retry

The first failed gate is exact-target consistency. `S56-M-0120-STATEMENT` must be reopened and its
stand-ins replaced by intrinsic definitions or noncircular laws connecting the projective klt pair
to the numerical curve space, effective cone, canonical pairing, rational curves, and contractions.
Assuming `Conclusion` or any required output package would be circular. Positive proof work can
resume only after the repaired expression fingerprint and obligation registry receive master
acceptance, followed by a fresh anchor audit and proof execution.

## Scoped Validation

All commands ran in this worker clone using the existing canonical pinned Lake closure. No update,
build, clone, fetch, or dependency mutation was performed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes the run dirty, nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| isolated `lake env lean -t0` recipe below | 0 | exact statement elaborated; countermodel checked; axiom report `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains `M3`; substantive packages remain open |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C .lake/packages/mathlib rev-parse HEAD` from `Formalizations/Lean` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `test -z "$(git -C .lake/packages/mathlib status --porcelain)"` from `Formalizations/Lean` | 0 | pinned mathlib worktree clean |
| placeholder scan below, from `Formalizations/Lean` | 1 | no matches; exit 1 is ripgrep's no-match result |
| `python3 -m json.tool Stage1_Instances/THM-M-0120/proof-blocker-2026-07-14.json` | 0 | historical structured blocker is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0120` | 0 | no whitespace errors in the owned-path delta |
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

The relevant output was:

```text
'Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
```

Exact placeholder scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' \
  ../../Stage1_Instances/THM-M-0120/Proof.lean
```

Content inputs at this base are unchanged: statement SHA-256
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, proof witness
`e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`, obligation registry
`cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`, typed graphs
`9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`, and anchor audit
`71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

No `.stage1-worker-selftest.json` is written because the assigned positive proof deliverable is
blocked rather than genuinely self-tested as complete.
