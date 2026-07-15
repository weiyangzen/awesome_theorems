# THM-M-0424 proof retry at `97cd9c49`

Item: `S56-M-0424-PROOF`. Intent: `prove`. Recorded on 2026-07-15
(Asia/Shanghai) from base revision
`97cd9c492d95baa9b55d2d8b341844107f07e686` and base tree
`bdd31de5f2fcd38078e4b5793b400a8105a3b8ba`.

## Verdict

This proof retry is **blocked**. It adds no positive proof body, closes no
obligation, and deliberately emits no `.stage1-worker-selftest.json`.

The exact frozen target is false. The tracked placeholder-free declaration

```text
Stage1Instances.THM_M_0424.UniverseCounterexample.not_brauerGroupStatement :
  Not Stage1Instances.THM_M_0424.BrauerGroupStatement.{1, 0}
```

kernel-checks the first failed gate,
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0424-S-BOUNDARY`. At `u = 1` and
`v = 0`, instantiate the quantified field with `Type 0 : Type 1` using
`Infinite.nonempty_field`. The required `oneRep : CSA.{1,0} K` has a carrier
in `Type 0`, while `oneRep_equiv_base` makes that carrier algebra-equivalent
to `K`. This implies `Small.{0} (Type 0)`, contradicting `not_small_type`.
Thus no positive body for the frozen universal proposition can exist.

Changing the carrier universe or adding a size premise here would substitute
a repaired theorem for the frozen theorem and is outside this proof phase.
The statement phase must reopen and publish a new expression fingerprint;
then the statement, anchor, registry, graph, and validation artifacts must be
refrozen and accepted.

There is also a secondary implementation blocker: pinned
`Mathlib.Algebra.BrauerGroup.Defs` explicitly leaves the tensor-product
abelian-group construction as TODO 1. The pinned dependency closure contains
no `CommGroup (BrauerGroup K)` body or terminal implementation of tensor-CSA
packaging, stable-equivalence congruence, quotient descent, the group laws, or
the opposite-algebra inverse.

The direct DAG prerequisite `S56-M-0424-OBLIGATION_TREE` remains provisional
`[_]`, not master-accepted `[x]`. Lifecycle remains `planned`; the root vector
remains `[H1, M3, R3]`; proof state remains `[ ]`; and theorem completion is
false. This is unresolved retry 43. The five-tick split threshold is exceeded,
so the master or scheduler must reopen the invalid statement dependency and
split the proof work before another positive retry. This worker does not own
the execution DAG. Its authoritative `attempts` field still says 0 despite 42
earlier integrated blocker pairs; the master must reconcile that discrepancy.

## Scoped Validation

All checks ran in this worker clone. The automation-provided `.lake` symlink
to the canonical pinned artifacts was used read-only. Lean outputs were
confined to a disposable `/tmp` directory and removed by a trap. No
`lake update`, `lake build`, dependency clone or fetch, checkout, network
access, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0 | Rank 78; lifecycle planned; theorem incomplete. |
| DAG query for `S56-M-0424-OBLIGATION_TREE` and `S56-M-0424-PROOF` | 0 | Direct dependency is `[_]` with attempts 1; proof is `[ ]` with attempts 0. |
| `LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-0424/check_statement.py` | 0 | Exact expression hash `62cfee70820b2f8bc4e924505b8984993322f623109868957b726b3446fc3aa8`; all four mutations killed. |
| `python3 Stage1_Instances/THM-M-0424/check_anchor_audit.py` | 0 | Six immutable candidates verified; exact root remains M3. |
| `python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py` | 0 | 18 obligations and 35 typed edges passed; denominator `83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00`; root open M3. |
| `cd Formalizations/Lean && timeout --foreground 45s lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| Isolated trust-zero replay below | 0 | Exact target refuted at `{1,0}`; all four counterexample declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`; every `assert_no_sorry` passed; the conditional composition adapter also replayed. |
| Scoped prohibited-construct scan of all owned Lean files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, declared `axiom`, `constant`, `opaque`, `unsafe`, `external`, `native_decide`, or `implemented_by`. |
| Search for `CommGroup (BrauerGroup ...)` in the pinned closure | 1 | Expected no-match; no terminal Brauer-group law body. |
| Pinned toolchain and dependency integrity recipe | 0 | Lean 4.29.0; mathlib and flt-regular revisions and trees matched their pins; inspected dependency worktrees were clean. |
| `python3 -m json.tool` plus structured blocker assertions | 0 | JSON parsed; identity, base, blocked state, retry 43, negative completion flags, two changed paths, and absent self-test claim matched. |
| Scoped artifact integrity, whitespace, and path-scope checks | 0 | Both new files have no whitespace errors or trailing blanks; the owned delta contains exactly those two files. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is deliberately absent. |

The successful narrow Lean replay used a fresh temporary output directory:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-0424"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-0424-97cd9c49-slot14.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
base_path=$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)
lean_bin=$(cd "$lean_root" && lake env which lean)
(cd "$lean_root" && LC_ALL=C LANG=C NO_COLOR=1 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$base_path" timeout --foreground --kill-after=5s 600s \
  "$lean_bin" --trust=0 -t0 --root="$target" \
  -o "$tmp/Statement.olean" "$target/Statement.lean") \
  >"$tmp/statement.out" 2>&1
(cd "$lean_root" && LC_ALL=C LANG=C NO_COLOR=1 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$base_path" timeout --foreground --kill-after=5s 600s \
  "$lean_bin" --trust=0 -t0 --root="$target" \
  -o "$tmp/UniverseCounterexample.olean" \
  "$target/UniverseCounterexample-2026-07-14-head-5753c6ed.lean") \
  >"$tmp/counterexample.out" 2>&1
(cd "$lean_root" && LC_ALL=C LANG=C NO_COLOR=1 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$base_path" timeout --foreground --kill-after=5s 600s \
  "$lean_bin" --trust=0 -t0 --root="$target" \
  -o "$tmp/ObligationTree.olean" "$target/ObligationTree.lean") \
  >"$tmp/obligation-tree.out" 2>&1
sha256sum "$tmp/statement.out" "$tmp/counterexample.out" \
  "$tmp/obligation-tree.out" "$tmp/Statement.olean" \
  "$tmp/UniverseCounterexample.olean" "$tmp/ObligationTree.olean"
```

The statement, counterexample, and conditional-composition output SHA-256
values were respectively
`efa2ea0ea05ce852276dd67e3abe1c6f3c705670f8c435bebcf57be1456b4e51`,
`c309037999d6b2be51e46f3e5a1e3ce8f67255764f213671c71f0df4696e8dcb`,
and `5ab61e156db84519f832ef8bece82fc844740903e13b2e8144b23da07d5a74af`.
Their `.olean` SHA-256 values were respectively
`3cf07b674053f73ba89b4b05c86e12c87cece6b588f3ee71ff389db747a1c2c2`,
`73972a794d9812a5d5398ecf4b35ab924352e1d526e1a8d77ebca72bdd5177a2`,
and `006e305c920b1023956ed2c09271722f8ee7f91dddfff40a128e86ff090bc526`.

## Retry Condition

Reopen `S56-M-0424-STATEMENT`, relate the field and CSA carrier universes (or
add a sufficient explicit size boundary), publish and master-accept a new
exact fingerprint, and refreeze all dependent architecture. Split this proof
item. Resume positive proof work only after placeholder-free bodies for the
repaired tensor-product and group-law obligations exist locally or an
immutable, compatible terminal proof is pinned and checked.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0424-PROOF`, change `[ ]`, close the root, or support audit completion,
theorem completion, validation, release, or master acceptance.
