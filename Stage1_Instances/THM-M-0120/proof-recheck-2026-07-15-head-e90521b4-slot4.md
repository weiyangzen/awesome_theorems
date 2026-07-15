# THM-M-0120 proof-phase recheck at base `e90521b4`

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `e90521b4b150b98d81c4dca2462ad36b64d4673e`

Base tree: `f12951f481d2b51f33d6d300dc2874b3c49ed0e0`

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
resume only after the repaired target has a new accepted expression fingerprint and obligation
registry, followed by a fresh anchor audit and proof execution. The prerequisite obligation-tree
item is currently only provisional `[_]`, not master-accepted.

The owned dossier contains more than five unresolved proof rechecks while the authoritative
execution DAG still records `attempts = 0` and no child nodes. Section 10.2 requires an item to be
split after five unresolved execution ticks. The master must reconcile whether these rechecks map
to execution ticks and, if so, redirect work to statement repair or bounded child items rather than
continue rescheduling the same impossible positive proof task. This worker does not edit the DAG.

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
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable local candidates, clean pinned mathlib, eight Lean probes, and the `M3` boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains `M3`; substantive packages remain open |
| isolated pinned-mathlib `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| pinned Lean 4.29.0 executable with `--version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and clean-worktree check | 0 | revision `8a178386...a95`; tree `bdc39a31...e2b`; worktree clean |
| placeholder scan below | 1 | no matches; exit 1 is ripgrep's no-match result |
| structured blocker invariant and JSON validation | 0 | current-base identity, hashes, failed gate, cut set, empty receipts, and self-test absence agreed |
| scoped whitespace checks | 0 | no whitespace errors in both new owned-path artifacts |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean recipe:

```bash
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0120
mathlib=$repo_root/Formalizations/Lean/.lake/packages/mathlib
tmp=$(mktemp -d /tmp/thm-m-0120-proof-heade90521b4.XXXXXX)
log=$(mktemp /tmp/thm-m-0120-proof-heade90521b4-log.XXXXXX)
trap 'rm -rf "$tmp" "$log"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp/"
paths=$(find "$repo_root/Formalizations/Lean/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd: -)
cd "$mathlib"
{
  LEAN_PATH="$paths" LEAN_NUM_THREADS=1 timeout --foreground 300 \
    lake env lean --trust=0 -t0 --root="$tmp" \
      -o "$tmp/Statement.olean" "$tmp/Statement.lean"
  printf 'STATEMENT_EXIT=%s\n' "$?"
  LEAN_PATH="$tmp:$paths" LEAN_NUM_THREADS=1 timeout --foreground 300 \
    lake env lean --trust=0 -t0 --root="$tmp" \
      -o "$tmp/Proof.olean" "$tmp/Proof.lean"
  printf 'PROOF_EXIT=%s\n' "$?"
} >"$log" 2>&1
cat "$log"
sha256sum "$log" "$tmp/Statement.olean" "$tmp/Proof.olean"
```

Relevant output:

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

Lean printed the arrows above as Unicode. The captured output SHA-256 was
`d1c53ea898cc37d74a3c615477e00bc35b4cd8ab287349b05fb107d95fe0721b`. The temporary
statement and proof oleans had SHA-256 values
`f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16` and
`cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec` before cleanup.

Exact placeholder scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|\bopaque\b|\bextern\b|implemented_by|native_decide' \
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
