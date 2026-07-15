# THM-M-0120 proof-phase recheck at base `d5ab961c`

Item: `S56-M-0120-PROOF`

Intent: `prove`

Base revision: `d5ab961cb3cd92c7febcf21fb9ab746fde231c24`

## Verdict

`blocked`. The exact frozen proposition cannot have a truthful positive proof body. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

was freshly elaborated at Lean trust level zero. Its countermodel uses the proper identity on
`Spec (AlgebraicClosure Rat)` and makes every explicit geometric proposition true. But the frozen
structure leaves the numerical data independent: `N1 = Real`, `moriCone = {-1}`, the canonical
pairing is the identity, and the rational-curve carrier is empty. Decomposition of `-1` therefore
forces a nonnegative component that equals `-1`, a contradiction.

This refutes the abstract Lean encoding, not the mathematical Mori cone theorem. A universe-zero
counterexample rules out a universe-polymorphic positive proof. Weakening or replacing the target,
or adding `Conclusion` or one of its output packages as an assumption, would be a substituted or
circular theorem and is outside this proof item.

The first failed gate is exact-target consistency at `M0120-S-DATA` and
`M0120-S-BOUNDARY`. Statement work must connect the numerical curve space, effective cone,
canonical pairing, rational curves, and contractions to the projective klt pair by intrinsic
definitions or noncircular semantic laws. A repaired statement needs a new accepted expression
fingerprint, anchor audit, and obligation registry before proof execution can resume.

The prerequisite obligation-tree item remains provisional `[_]`, while the proof item remains
`[ ]`. The dossier also contains more than five unresolved proof rechecks although scheduler
authority records `attempts: 0` and no children. Only the master may reconcile those ticks and
split or redirect the task; this worker did not edit scheduler authority.

## Validation

All checks ran in this worker clone against the existing pinned artifacts. No `lake update`,
`lake build`, clone, fetch, dependency repair, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable candidates, clean pinned mathlib, eight probes, and M3 boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains M3 |
| root `lake env lean` trust-zero replay | 1 | pre-existing `flt-regular` `HEAD = refs/heads/.invalid` blocked Lake before Lean was invoked |
| isolated pinned-mathlib `lake env lean --trust=0` replay | 0 | `Statement.lean` and `Proof.lean` elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| placeholder scan over owned Lean files | 1 | expected ripgrep no-match result; no `sorry`, `admit`, `axiom`, `sorryAx`, or `unsafe` token |
| blocker JSON and invariant checks | 0 | identity, hashes, fail-closed flags, cut set, empty accepted receipts, and self-test absence agreed |
| `git diff --check --` target-scoped blocker artifacts | 0 | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

The successful narrow replay copied `Statement.lean` and `Proof.lean` to a fresh `/tmp` directory,
invoked the pinned Lean toolchain from the clean mathlib package, and supplied only the existing
package build directories through `LEAN_PATH`. The observed semantic output was:

### Exact Lean Replay

The root environment failure was reproduced exactly by:

```bash
cd Formalizations/Lean && lake env lean --version
```

The successful trust-zero replay was run from the repository root with this exact recipe:

```bash
set -u
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0120
lake_root=$repo_root/Formalizations/Lean/.lake
mathlib_root=$lake_root/packages/mathlib
tmp=$(mktemp -d /tmp/thm-m-0120-proof-headd5ab961c.XXXXXX)
log=$(mktemp /tmp/thm-m-0120-proof-headd5ab961c-log.XXXXXX)
trap 'rm -rf "$tmp" "$log"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
paths=
for package in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
  path="$lake_root/packages/$package/.lake/build/lib/lean"
  test -d "$path"
  if [ -z "$paths" ]; then paths=$path; else paths="$paths:$path"; fi
done
cd "$mathlib_root"
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
printf 'STATEMENT_EXIT=%s\nPROOF_EXIT=%s\n' \
  "$statement_status" "$proof_status"
sha256sum "$log" "$tmp/Statement.olean" "$tmp/Proof.olean"
test "$statement_status" = 0
test "$proof_status" = 0
```

Its exact relevant output was:

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

The displayed arrows are normalized to ASCII. The captured output SHA-256 was
`19d53d6a657e000a6c2cfd7f6cf0a5e34ffb70112eca7beb74a243e2b472cc59`; temporary statement and
proof olean hashes were respectively `f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16`
and `cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec` before cleanup.

No `.stage1-worker-selftest.json` is written because the requested positive proof deliverable is
blocked, not genuinely self-tested as complete. No proof receipt, audit completion, theorem
completion, release decision, or master acceptance is claimed.
