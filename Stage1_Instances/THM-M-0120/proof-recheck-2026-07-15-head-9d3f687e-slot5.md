# THM-M-0120 proof-phase recheck at base `9d3f687e`

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `9d3f687e9bf0fe3120397744332e909472c52dfd`

Base tree: `558507d70ac5e5e38486f214a3e0ce7b33f7ae9b`

## Verdict

`blocked`. No positive proof body can truthfully inhabit the exact frozen proposition. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

was freshly recompiled with Lean trust level zero. It gives a concrete countermodel to the
universal target. The proper morphism is the identity on `Spec (AlgebraicClosure Rat)`, and all six
explicit input propositions are true (`IsProper` plus the five `Prop` fields required by the
target). The statement nevertheless leaves its numerical data independent: `N1 = Real`,
`moriCone = {-1}`, `canonicalPairing = LinearMap.id`, and `RationalCurve = Empty`. The required
decomposition of `-1` produces a component in the nonnegative part that is both `-1` and
nonnegative, a contradiction. Refutation at universe specialization `{0, 0, 0, 0}` rules out a
universe-polymorphic positive proof.

This refutes the current abstract Lean encoding, not the mathematical Mori cone theorem. Replacing
the target, narrowing its binders, or assuming `Conclusion` or any required output package would
be theorem substitution or circularity and is outside this proof item's ownership. The item
remains `[ ]`. No proof receipt, provisional state, audit completion, theorem completion, release
decision, or master acceptance is claimed. The predecessor graph remains authoritatively
`H2 / M3 / R4`; this proof attempt proposes `H5 / M5 / R4` only for integration review.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY` at `M0120-S-DATA` and
`M0120-S-BOUNDARY`. `S56-M-0120-STATEMENT` must be reopened so that the numerical curve space,
effective cone, canonical pairing, rational curves, and contractions are defined intrinsically or
connected to the projective klt pair by noncircular semantic laws. Positive proof execution may
resume only after the repaired target has a new accepted expression fingerprint, anchor audit, and
obligation registry. The prerequisite obligation-tree node is provisional rather than
master-accepted, and the owned task DAG records no accepted states.

Before this recheck, the dossier already contained 34 Markdown and 24 JSON proof recheck artifacts
while the authoritative execution DAG still recorded `attempts = 0` and no child nodes. Section
10.2 requires an item to be split after five unresolved execution ticks. The master must reconcile
whether these rechecks map to execution ticks and, if so, redirect work to statement repair or
bounded child items rather than continue rescheduling the same impossible positive proof task.
This worker does not edit the DAG.

## Scoped Validation

All checks ran in this worker clone using the existing pinned dependency artifacts. No
`lake update`, `lake build`, clone, fetch, dependency mutation, or network operation was performed.
The automation-provided untracked `Formalizations/Lean/.lake` symlink makes this dirty, nonrelease
blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned lifecycle; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_statement.py` | 0 | canonical expression hash `074d45c3...d88cfd`; all three structural mutations differed; pinned mathlib and toolchain agreed |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable local candidates, clean pinned mathlib, eight Lean probes, and the `M3` boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains `M3`; substantive packages remain open |
| isolated `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| pinned mathlib revision/tree checks | 0 | mathlib `8a178386...ea95`, tree `bdc39a31...5c2b`; clean worktree |
| placeholder scan below | 1 | no matches; exit 1 is ripgrep's no-match result |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean recipe, run from the repository root:

```bash
set -u
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0120
lake_root=$repo_root/Formalizations/Lean/.lake
mathlib_root=$lake_root/packages/mathlib
tmp=$(mktemp -d /tmp/thm-m-0120-proof-head9d3f687e-slot5.XXXXXX)
log=$(mktemp /tmp/thm-m-0120-proof-head9d3f687e-slot5-log.XXXXXX)
trap 'rm -rf "$tmp" "$log"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
paths=
for package in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
  path="$lake_root/packages/$package/.lake/build/lib/lean"
  test -d "$path" || exit 126
  if [ -z "$paths" ]; then paths=$path; else paths="$paths:$path"; fi
done
cd "$mathlib_root"
LEAN_PATH="$paths" LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Statement.olean" "$tmp/Statement.lean" >"$log" 2>&1
statement_status=$?
proof_status=125
if [ "$statement_status" -eq 0 ]; then
  LEAN_PATH="$tmp:$paths" LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s \
    lake env lean --trust=0 -t0 --root="$tmp" \
      -o "$tmp/Proof.olean" "$tmp/Proof.lean" >>"$log" 2>&1
  proof_status=$?
fi
cat "$log"
printf 'STATEMENT_EXIT=%s\nPROOF_EXIT=%s\n' "$statement_status" "$proof_status"
sha256sum "$log" "$tmp/Statement.olean" "$tmp/Proof.olean"
test "$statement_status" = 0
test "$proof_status" = 0
```

Relevant output:

```text
def Stage1Instances.THMM0120.MoriConeTheoremTarget.{u, uK, uN, uC} : Prop :=
forall (D : Stage1Instances.THMM0120.ConeTheoremData.{u, uK, uN, uC}),
  @AlgebraicGeometry.IsProper.{u} D.X D.S D.f ->
    D.definedOverBaseField -> D.projective -> D.normal -> D.qFactorial -> D.klt -> D.Conclusion
'Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
STATEMENT_EXIT=0
PROOF_EXIT=0
```

Lean printed the arrows above as Unicode. The output, statement olean, and proof olean had SHA-256
values `19d53d6a657e000a6c2cfd7f6cf0a5e34ffb70112eca7beb74a243e2b472cc59`,
`f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16`, and
`cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec` before cleanup.

Exact placeholder scan:

```bash
rg -n --pcre2 \
  '(?x)(\b(?:sorry|admit|sorryAx|unsafe|opaque|extern|implemented_by|native_decide)\b|^\s*axiom\s)' \
  Stage1_Instances/THM-M-0120 -g '*.lean'
```

The unchanged source inputs have these SHA-256 values: statement
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, countermodel proof
`e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`, registry
`cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`, typed graphs
`9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`, and anchor audit
`71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

No `.stage1-worker-selftest.json` is written because the assigned positive proof phase is blocked,
not genuinely self-tested as complete.
