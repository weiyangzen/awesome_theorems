# THM-M-0424 proof retry at `5b35bc15`

Item: `S56-M-0424-PROOF`. Intent: `prove`. Recorded at
`2026-07-15T15:57:48+08:00` from base revision
`5b35bc151522d93c7f54966ef64f1fc630371537` and base tree
`fe77824631ab2573a4596bddc1a2534c06cd23f8`.

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
The statement phase must reopen and publish a new expression fingerprint,
then dependent obligation artifacts must be versioned and refrozen.

There is a second, independent proof blocker after that repair. Pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` defines `CSA`,
`IsBrauerEquivalent`, `Brauer.CSA_Setoid`, and the quotient `BrauerGroup`, but
`Mathlib/Algebra/BrauerGroup/Defs.lean` explicitly leaves the tensor-product
abelian-group construction as TODO 1. A source-wide search found no
`CommGroup (BrauerGroup ...)` terminal body. Consequently the tensor-CSA,
tensor congruence, descent, associativity, commutativity, unit, inverse, and
LawData assembly obligations also remain open.

The direct prerequisite `S56-M-0424-OBLIGATION_TREE` is still provisional
`[_]`, not master-accepted `[x]`. This is unresolved retry 36, far beyond the
five-tick split threshold. The master or scheduler must reopen the invalid
statement dependency and split or reconcile the oversized proof work; this
worker did not edit the DAG or generated blueprint.

## Validation

All Lean output was confined to a disposable `/tmp` directory. The
automation-provided `.lake` symlink was reused read-only; no update, build,
clone, fetch, checkout, repair, or network command was run.

| Command | Exit/result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0; 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0; 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0; rank 78, planned, L0/rework-required, theorem incomplete |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600s python3 ../../Stage1_Instances/THM-M-0424/check_statement.py` | 0; exact expression hash `62cfee70820b2f8bc4e924505b8984993322f623109868957b726b3446fc3aa8`; four mutations killed |
| `python3 Stage1_Instances/THM-M-0424/check_anchor_audit.py` | 0; six immutable candidates verified; exact root remains M3 |
| `python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py` | 0; 18 obligations and 35 typed edges passed; root remains open M3 |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 for `Statement.lean`, the universe counterexample, and `ObligationTree.lean`; exact target refuted at `{1,0}`; every negative declaration reported exactly `propext`, `Classical.choice`, and `Quot.sound`; all `assert_no_sorry` checks passed; conditional composition supplies no LawData inhabitant |
| Scoped prohibited-construct scan over owned Lean files | 1; expected no-match |
| Search for a `CommGroup (BrauerGroup ...)` instance in pinned packages | 1; expected no-match |
| Search for tensor-product central/simple preservation in pinned mathlib | 0; only one converse-centrality line, no tensor-CSA body |
| `cd Formalizations/Lean && lake env lean --version` | 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| Pinned checkout identity and status checks | 0; mathlib revision/tree, flt-regular revision, and manifest pins agree; inspected package checkouts were clean |

The successful narrow Lean recipe was:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-0424"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-0424-5b35bc15-slot73.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
base=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$lean_root"
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600s \
  lake env lean --trust=0 -t0 --root="$target" \
  -o "$tmp/Statement.olean" "$target/Statement.lean" \
  >"$tmp/statement.out" 2>&1
LEAN_PATH="$tmp:$base" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 600s \
  lake env lean --trust=0 -t0 --root="$target" \
  -o "$tmp/UniverseCounterexample.olean" \
  "$target/UniverseCounterexample-2026-07-14-head-5753c6ed.lean" \
  >"$tmp/counterexample.out" 2>&1
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600s \
  lake env lean --trust=0 -t0 --root="$target" \
  -o "$tmp/ObligationTree.olean" "$target/ObligationTree.lean" \
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

## Retry condition

Reopen `S56-M-0424-STATEMENT`, relate the field and CSA carrier universes (or
add a sufficient explicit size boundary), publish and master-accept a new
exact fingerprint, and refreeze all dependent architecture. Split this proof
item. Resume positive proof work only after placeholder-free bodies for the
repaired tensor-product and group-law obligations exist locally or an
immutable, compatible terminal proof is pinned and checked.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0424-PROOF`, change `[ ]`, close the root, or support audit completion,
theorem completion, validation, release, or master acceptance.
