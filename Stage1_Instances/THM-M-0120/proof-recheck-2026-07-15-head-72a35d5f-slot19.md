# THM-M-0120 proof-phase recheck at base `72a35d5f`

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `72a35d5f64e32233c0bc77a57e47bd078475ad74`

Base tree: `a80eb91ed5629dee62d031e78bc87b509cf8e6eb`

## Verdict

`blocked`. No positive proof body can truthfully inhabit the exact frozen proposition. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

was recompiled from fresh copies of `Statement.lean` and `Proof.lean` with Lean trust level zero.
It supplies a concrete countermodel to the universal target. The proper morphism is the identity on
`Spec (AlgebraicClosure Rat)`, and every explicit proposition hypothesis is true, but the numerical
data are independent: `N1 = Real`, `moriCone = {-1}`, `canonicalPairing = LinearMap.id`, and
`RationalCurve = Empty`. The required decomposition of `-1` then produces a nonnegative component
that is both `-1` and nonnegative, a contradiction.

This refutes the current abstract Lean encoding, not the mathematical Mori cone theorem. Replacing
the target, narrowing its binders, or adding `Conclusion` or one of its output packages as an
assumption would be a substitution or a circular repair and is outside this proof item's ownership.
The item therefore remains `[ ]`; no proof receipt, provisional state, audit completion, theorem
completion, release decision, or master acceptance is claimed.

## Failed Gate And Retry

The first failed gate is exact-target consistency at `M0120-S-DATA` and
`M0120-S-BOUNDARY`. `S56-M-0120-STATEMENT` must be reopened so that the numerical curve space,
effective cone, canonical pairing, rational curves, and contractions are defined intrinsically or
connected to the projective klt pair by noncircular semantic laws. Positive proof execution may
resume only after the repaired target has a new accepted expression fingerprint, anchor audit, and
obligation-registry version.

## Scoped Validation

All checks used this worker clone and the existing pinned Lean artifacts. No `lake update`, build,
clone, fetch, dependency mutation, or network operation was performed. The automation-provided
untracked `Formalizations/Lean/.lake` symlink points at the canonical pinned artifacts, so this is
dirty, nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; lifecycle planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| unchanged predecessor statement evidence (not rerun) | n/a | source SHA-256 still `69eabc83...7444fd6b`; predecessor evidence records canonical expression SHA-256 `074d45c3...d88cfd` and three distinguished mutations |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable local candidates, clean pinned mathlib, eight Lean probes, and the `M3` boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains `M3`; substantive packages remain open |
| isolated `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain` | 0 | no output; pinned mathlib worktree clean |
| placeholder scan below | 1 | no matches; exit 1 is ripgrep's no-match result |
| artifact JSON validation and blocker-invariant check | 0 | JSON parsed; identity, base/tree, hashes, blocked state, empty receipts, failed gate, retry condition, and self-test absence agreed |
| scoped tracked and no-index whitespace checks | 0 | no whitespace errors; each no-index check returned its expected clean-difference exit 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean countermodel recipe:

```bash
set -euo pipefail
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0120
lean_root=$repo_root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0120-proof-72a35d5f-slot19.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$lean_root"
base=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground 900 \
  lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$base" LEAN_NUM_THREADS=1 timeout --foreground 900 \
  lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Proof.olean" "$tmp/Proof.lean"
```

The relevant output was:

```text
def Stage1Instances.THMM0120.MoriConeTheoremTarget.{u, uK, uN, uC} : Prop :=
forall (D : Stage1Instances.THMM0120.ConeTheoremData.{u, uK, uN, uC}),
  @AlgebraicGeometry.IsProper.{u} D.X D.S D.f ->
    D.definedOverBaseField -> D.projective -> D.normal -> D.qFactorial -> D.klt -> D.Conclusion
STATEMENT_EXIT=0
'Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
PROOF_EXIT=0
```

The displayed arrows were normalized to ASCII. The complete captured output had SHA-256
`d1c53ea898cc37d74a3c615477e00bc35b4cd8ab287349b05fb107d95fe0721b`.
The temporary `Statement.olean` had SHA-256
`f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16`, and the temporary
`Proof.olean` had SHA-256
`cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec`, before cleanup.

Exact placeholder scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' \
  Stage1_Instances/THM-M-0120 -g '*.lean'
```

The unchanged content inputs at this base are: statement SHA-256
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, countermodel proof
SHA-256 `e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`, registry SHA-256
`cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`, typed graphs SHA-256
`9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`, and anchor audit
SHA-256 `71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

No `.stage1-worker-selftest.json` is written because the assigned positive proof deliverable is
blocked rather than genuinely self-tested as complete.
