# THM-M-0120 proof blocker at base `b73dae2e`

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recorded: 2026-07-15T20:51:56+08:00

Base revision: `b73dae2e6741a0be1f316d748a37f487a671cca4`

Base tree: `d582d50d420e2a27b4fb21ed0abea58cee03184f`

## Verdict

`blocked`. No positive proof body can truthfully inhabit the exact frozen proposition. A fresh
trust-zero replay checked the existing placeholder-free countermodel declaration:

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

The countermodel uses the identity (hence proper) morphism on
`Spec (AlgebraicClosure Rat)` and makes every explicit proposition premise true. The statement
does not connect those premises to its numerical data, so it also permits `N1 = Real`,
`moriCone = {-1}`, `canonicalPairing = LinearMap.id`, and `RationalCurve = Empty`. The required
decomposition of `-1` then yields a nonnegative component equal to `-1`, a contradiction.

Refutation at universe specialization `{0, 0, 0, 0}` rules out a universe-polymorphic positive
proof. This refutes only the disconnected Lean encoding, not the mathematical Mori cone theorem.
Narrowing or replacing the target, or assuming `Conclusion` or one of its output packages, would
be theorem substitution or circularity. No Lean source was changed, and this item remains `[ ]`.
No proof receipt, provisional completion state, audit completion, theorem completion, release
decision, or master acceptance is claimed.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY`, at obligations `M0120-S-DATA` and
`M0120-S-BOUNDARY`. The integration lane must reopen `S56-M-0120-STATEMENT` and replace the
disconnected numerical and proposition stand-ins with intrinsic definitions or noncircular
semantic laws tying them to the projective klt pair. Proof work can resume only after a new target
fingerprint is accepted and the anchor audit and obligation registry are rerun and refrozen.

The prerequisite obligation-tree node is still only provisional `[_]`, and the local task DAG has
no accepted states. Before this artifact, the owned dossier already contained 41 structured and
51 readable proof rechecks plus two structured and two readable blocker artifacts, while scheduler
authority still recorded `attempts = 0` and `children = []`. The master must reconcile that history
with the section 10.2 rule requiring split or redirect after five unresolved execution ticks,
rather than schedule another identical proof retry.

## Scoped Validation

All commands ran in this worker clone using only the existing pinned dependency artifacts. No
`lake update`, `lake build`, clone, fetch, network operation, or dependency mutation was performed.
The automation-provided untracked `Formalizations/Lean/.lake` symlink makes this nonrelease
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_statement.py` | 0 | expression SHA-256 `074d45c3...d88cfd`; three mutations differed; pinned toolchain agreed |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable local candidates, clean pinned mathlib, eight probes, and M3 boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 edges passed; root remains M3; packages remain open |
| isolated pinned-mathlib `lake env lean --trust=0 -t0` replay below | 0 | statement and countermodel elaborated; axioms `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...fab16740`, Release |
| pinned mathlib revision, tree, and clean-status checks | 0 | revision `8a178386...ea95`; tree `bdc39a31...5c2b`; clean |
| prohibited-token scan below | 1 | expected no-match result |
| `python3 -m json.tool` and blocker-invariant assertions | 0 | identity, base/tree, hashes, open state, empty receipts, cut set, and self-test absence agreed |
| `git diff --no-index --check /dev/null` for both new artifacts | 0 | expected content differences contained no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent |

Exact Lean replay:

```bash
set -u
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0120
mathlib=$repo_root/Formalizations/Lean/.lake/packages/mathlib
tmp=$(mktemp -d /tmp/thm-m-0120-proof-head-b73dae2e-slot6.XXXXXX)
log=$(mktemp /tmp/thm-m-0120-proof-head-b73dae2e-slot6-log.XXXXXX)
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

The observed exits were `STATEMENT_EXIT=0` and `PROOF_EXIT=0`. The temporary log,
`Statement.olean`, and `Proof.olean` had SHA-256 values
`19d53d6a657e000a6c2cfd7f6cf0a5e34ffb70112eca7beb74a243e2b472cc59`,
`f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16`, and
`cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec` before cleanup.

Exact prohibited-token scan:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|\bopaque\b|\bextern\b|implemented_by|native_decide' \
  Stage1_Instances/THM-M-0120 -g '*.lean'
```

No `.stage1-worker-selftest.json` is written because the requested positive proof phase is
genuinely blocked, not self-tested as complete.
