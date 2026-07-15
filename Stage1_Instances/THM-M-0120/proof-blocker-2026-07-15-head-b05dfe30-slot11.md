# THM-M-0120 proof blocker at base `b05dfe30`

Item: `S56-M-0120-PROOF`

Date: 2026-07-15

Base revision: `b05dfe30bf9c4067039b9414912ec94f3153bb0b`

Base tree: `a0ccbad8cb36717f11ac16baef9a640aed04457e`

## Verdict

`blocked`. The exact frozen target has no truthful positive proof body. The
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

was freshly elaborated at Lean trust level zero from the current source. Its
countermodel uses the proper identity morphism on `Spec (AlgebraicClosure Rat)`
and makes every explicit geometric proposition true. The statement nevertheless
allows unrelated numerical data: `N1 = Real`, `moriCone = {-1}`, the canonical
pairing is the identity, and the rational-curve carrier is empty. Applying the
claimed cone decomposition to `-1` forces a nonnegative component equal to
`-1`, a contradiction.

This refutes the current abstract Lean encoding, not the mathematical Mori cone
theorem. Since the target is universe-polymorphic, the checked universe-zero
countermodel rules out its requested positive proof. Weakening the theorem,
proving a narrower replacement, or assuming `Conclusion` (or one of its output
packages) would be forbidden substitution or circularity.

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY`, with first invalid
obligations `M0120-S-DATA` and `M0120-S-BOUNDARY`. The statement phase must
intrinsically connect the numerical curve space, effective cone, canonical
pairing, rational curves, and contractions to the projective klt pair. A
repaired exact target then needs a new accepted expression fingerprint, anchor
audit, and frozen obligation registry before proof execution can resume.

No `.stage1-worker-selftest.json` is written because the positive proof phase is
blocked, not self-tested as complete. This record supports no proof receipt,
audit completion, theorem completion, release, or master acceptance claim.

## Validation

All commands ran in this worker clone. Lean replay used only the existing pinned
toolchain and dependency build directories. No `lake update`, `lake build`,
clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_statement.py` | SIGTERM | produced no output after about four minutes and was terminated; its temporary source was removed; the direct trust-zero replay below separately elaborated the exact statement and proof |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable candidates, clean pinned mathlib, eight probes, and M3 boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; root remains M3 |
| isolated pinned-mathlib `lake env lean --trust=0 -t0` replay below | 0 | `Statement.lean` and `Proof.lean` elaborated; declaration axioms were `[propext, Classical.choice, Quot.sound]` |
| `rg -n -i '\b(sorry\|admit\|axiom\|unsafe)\b\|sorryAx' Stage1_Instances/THM-M-0120 --glob '*.lean'` | 1 | expected no-match result; owned Lean sources contain no forbidden token |
| `git diff --check -- Stage1_Instances/THM-M-0120` | 0 | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

### Exact Lean Replay

From the repository root:

```bash
set -u
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0120
lake_root=$repo_root/Formalizations/Lean/.lake
mathlib_root=$lake_root/packages/mathlib
tmp=$(mktemp -d /tmp/thm-m-0120-proof-headb05dfe30-slot11.XXXXXX)
log=$(mktemp /tmp/thm-m-0120-proof-headb05dfe30-slot11-log.XXXXXX)
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
'Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
STATEMENT_EXIT=0
PROOF_EXIT=0
```

Evidence hashes:

```text
Statement.lean  69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b
Proof.lean      e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab
replay output   19d53d6a657e000a6c2cfd7f6cf0a5e34ffb70112eca7beb74a243e2b472cc59
Statement.olean f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16
Proof.olean     cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec
```

## Retry Condition

Reopen `S56-M-0120-STATEMENT`; replace the unconstrained stand-ins with
intrinsic definitions or noncircular semantic laws tying all numerical and
contraction data to the geometric pair; accept the repaired target fingerprint;
then rerun statement, anchor-audit, and obligation-tree phases before resuming
this proof item.
