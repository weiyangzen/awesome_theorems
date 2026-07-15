# THM-M-0120 proof-phase recheck at base `b366bdd9`

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `b366bdd9f72217b5465ccd19133760b911ed0b58`

Base tree: `987b635fe76400c0818b485a6e5fc7a7067311e4`

## Verdict

`blocked`. No positive proof body can inhabit the exact frozen proposition. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

was freshly recompiled from `Statement.lean` and `Proof.lean` with Lean trust level zero. It gives a
concrete countermodel to the universal target. The proper morphism is the identity on
`Spec (AlgebraicClosure Rat)`, and every explicit proposition hypothesis is true, but the frozen
structure leaves its numerical data independent: `N1 = Real`, `moriCone = {-1}`,
`canonicalPairing = LinearMap.id`, and `RationalCurve = Empty`. Decomposition of `-1` would then
produce a nonnegative component that both equals `-1` and is nonnegative, a contradiction.

Refutation at universe specialization `{0, 0, 0, 0}` rules out a universe-polymorphic positive
proof. This refutes the current abstract Lean encoding, not the mathematical Mori cone theorem.
Replacing or weakening the target, narrowing its binders, or assuming `Conclusion` or an output
package would be substitution or circularity and is outside this proof item's ownership. The item
therefore remains `[ ]`; no proof receipt, provisional state, audit completion, theorem completion,
release decision, or master acceptance is claimed. The predecessor obligation-tree item is only
provisional `[_]`, the local task DAG contains no accepted state, and the authoritative root remains
`H2 / M3 / R4`. The countermodel supports a proposed `H5 / M5 / R4` diagnosis for review, not a
worker-authored state change.

## First Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY`, at obligations `M0120-S-DATA` and
`M0120-S-BOUNDARY`. `S56-M-0120-STATEMENT` must be reopened. Its numerical curve space, effective
cone, canonical pairing, rational curves, and contractions must be defined intrinsically or tied to
the projective klt pair by noncircular semantic laws. The integration lane must then freeze and
accept a new expression fingerprint and obligation registry before rerunning anchor audit and proof
work.

Before this artifact, the owned dossier contained 37 structured and 47 readable proof rechecks plus
two structured and two readable blockers, while scheduler authority still recorded `attempts: 0`
and no children. The master must reconcile whether these map to execution ticks. Section 10.2
requires splitting or redirecting an item after five unresolved ticks rather than scheduling
another identical proof retry. This worker does not edit scheduler authority.

## Scoped Validation

All commands ran in this worker clone against existing pinned dependency artifacts. No `lake
update`, `lake build`, clone, fetch, network operation, or dependency mutation was performed. The
automation-provided untracked `Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_statement.py` | 0 | expression SHA-256 `074d45c3...d88cfd`; all three structural mutations differed; pinned Lean 4.29.0 and mathlib `8a178386...a95` agreed |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable candidates, clean pinned mathlib, eight Lean probes, and the `M3` boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains `M3` |
| isolated pinned-mathlib `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386...ea95`; tree `bdc39a31...c19e5c2b` |
| placeholder scan below | 1 | no matches; exit 1 is ripgrep's no-match result |
| artifact JSON and blocker-invariant check | 0 | identity, source hashes, fail-closed state, cut set, and self-test absence agreed |
| temporary-index `git diff --check` over both new artifacts | 0 | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean countermodel recipe:

```bash
set -u
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0120
mathlib=$repo_root/Formalizations/Lean/.lake/packages/mathlib
tmp=$(mktemp -d /tmp/thm-m-0120-proof-head-b366bdd9-slot20.XXXXXX)
log=$(mktemp /tmp/thm-m-0120-proof-head-b366bdd9-slot20-log.XXXXXX)
trap 'rm -rf "$tmp" "$log"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp/"
paths=$(find "$repo_root/Formalizations/Lean/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd: -)
cd "$mathlib"
LEAN_PATH="$paths" LEAN_NUM_THREADS=1 timeout --foreground 300 \
  lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Statement.olean" "$tmp/Statement.lean" >"$log" 2>&1
statement_status=$?
proof_status=125
if [ "$statement_status" -eq 0 ]; then
  LEAN_PATH="$tmp:$paths" LEAN_NUM_THREADS=1 timeout --foreground 300 \
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

Observed output:

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

The complete output, temporary `Statement.olean`, and temporary `Proof.olean` had SHA-256 values
`19d53d6a657e000a6c2cfd7f6cf0a5e34ffb70112eca7beb74a243e2b472cc59`,
`f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16`, and
`cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec`, respectively, before
cleanup.

Exact placeholder scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|\bopaque\b|\bextern\b|implemented_by|native_decide' \
  Stage1_Instances/THM-M-0120 -g '*.lean'
```

No `.stage1-worker-selftest.json` is written because the assigned positive proof deliverable is
blocked rather than genuinely self-tested as complete.
