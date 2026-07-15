# THM-M-0120 proof phase blocked at base `eed9e938`

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recheck date: 2026-07-16 (Asia/Shanghai)

Base revision: `eed9e9385a50d42f37cb1e0d8ba8928b163ef76d`

Base tree: `789cff33807f451c3880e716a73e2c0fbd0b2527`

## Verdict

`blocked`. No positive proof body can truthfully inhabit the exact frozen proposition. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

was freshly recompiled with Lean trust level zero. It supplies a concrete countermodel to the
universal target. The proper morphism is the identity on `Spec (AlgebraicClosure Rat)`, and all six
explicit input premises hold (`IsProper` plus the five proposition premises). The statement leaves
its numerical data independent: `N1 = Real`, `moriCone = {-1}`, `canonicalPairing = LinearMap.id`,
and `RationalCurve = Empty`. The required decomposition of `-1` produces a component in the
nonnegative part that is both `-1` and nonnegative, a contradiction.

Refutation at universe specialization `{0, 0, 0, 0}` rules out a universe-polymorphic positive
proof. This refutes the current abstract Lean encoding, not the mathematical Mori cone theorem.
Replacing the target, narrowing its binders, or assuming `Conclusion` or a required output package
would be theorem substitution or circularity and is outside this proof item's ownership.

The item remains `[ ]`. No proof receipt, provisional completion state, audit completion, theorem
completion, release decision, or master acceptance is claimed. Its obligation-tree dependency is
only provisional `[_]`, and the authoritative execution DAG still records `attempts = 0` and no
children.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY`, at obligations `M0120-S-DATA` and
`M0120-S-BOUNDARY`. `S56-M-0120-STATEMENT` must be reopened so that the numerical curve space,
effective cone, canonical pairing, rational curves, and contractions are intrinsic or connected to
the projective klt pair by noncircular semantic laws. Proof execution may resume only after the
repaired target has a new accepted expression fingerprint, anchor audit, obligation registry, and
typed graphs.

Before this artifact, the dossier contained 45 structured and 55 readable proof rechecks plus four
structured and four readable blocker artifacts, while the authoritative DAG still recorded zero
attempts and no child nodes. Section 10.2 requires a split after five unresolved execution ticks.
Only the master can reconcile whether these artifacts map to ticks and redirect work to statement
repair or bounded children. This worker does not edit scheduler authority.

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
| `timeout --foreground --kill-after=5s 300s env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-0120/check_statement.py` | 0 | expression SHA-256 `074d45c3...d88cfd`; all three structural mutations differed; pinned Lean 4.29.0 and mathlib `8a178386...ea95` agreed |
| `timeout --foreground --kill-after=5s 300s env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable local candidates, clean pinned mathlib, eight Lean probes, and the `M3` boundary agreed |
| `timeout --foreground --kill-after=5s 300s env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains `M3`; substantive packages remain open |
| isolated pinned-mathlib `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| pinned mathlib revision/tree/clean-status checks | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; clean |
| prohibited-token scan below | 0 wrapper, 1 `rg` | no matches; `rg` exit 1 is the expected no-match result |
| `python3 -m json.tool` plus blocker-invariant assertions | 0 | artifact identity, base/tree, hashes, fail-closed state, empty receipts, blocker cut set, and self-test absence agreed |
| `git diff --check` plus added-file whitespace checks | 0 | no whitespace diagnostics in either new owned-path artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test correctly absent |

Exact Lean replay:

```bash
set -u
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0120
mathlib=$repo_root/Formalizations/Lean/.lake/packages/mathlib
tmp=$(mktemp -d /tmp/thm-m-0120-proof-headeed9e938-slot6.XXXXXX)
log=$(mktemp /tmp/thm-m-0120-proof-headeed9e938-slot6-log.XXXXXX)
trap 'rm -rf "$tmp" "$log"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp/"
paths=$(find "$repo_root/Formalizations/Lean/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd: -)
cd "$mathlib"
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

Relevant output, with arrows normalized to ASCII:

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

The captured output SHA-256 was `19d53d6a657e000a6c2cfd7f6cf0a5e34ffb70112eca7beb74a243e2b472cc59`.
The temporary statement and proof olean SHA-256 values were respectively
`f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16` and
`cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec` before cleanup.

Exact prohibited-token scan:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|\bopaque\b|\bextern\b|implemented_by|native_decide' \
  Stage1_Instances/THM-M-0120 -g '*.lean'
```

It returned no output and exit 1, ripgrep's no-match status. No
`.stage1-worker-selftest.json` is written because the assigned positive proof phase is blocked rather
than genuinely self-tested as complete.
