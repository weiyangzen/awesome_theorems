# THM-M-0424 proof recheck at `031437b3` (slot 10)

Item: `S56-M-0424-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T23:11:34+08:00`

Base revision: `031437b3091b838bb0200e432b96ced6b34104e2`

Base tree: `176564c09ede7e686005c8051df537617d84b7c5`

## Verdict

`blocked`. A positive proof body cannot inhabit the exact frozen Lean target.
The owned, placeholder-free declaration

```text
Stage1Instances.THM_M_0424.UniverseCounterexample.not_brauerGroupStatement :
  Not Stage1Instances.THM_M_0424.BrauerGroupStatement.{1,0}
```

was replayed at Lean trust level zero against this base. A universe-polymorphic
positive proof would specialize to `{1,0}` and contradict that kernel-checked
theorem.

At this specialization, take `K := Type 0 : Type 1` with the field structure
provided by `Infinite.nonempty_field`. Any
`BrauerGroupLawData.{1,0} K` contains `oneRep : CSA.{1,0} K` and an algebra
equivalence from its carrier in `Type 0` to `K`. Its underlying equivalence
would prove `Small.{0} (Type 0)`, contradicting `not_small_type`.

This refutes only the frozen Lean encoding, not the classical Brauer-group
theorem. Exact-target consistency first fails at
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0424-S-BOUNDARY`, witnessed through
`M0424-C-ONE`. Repair requires reopening the statement phase to relate the
field and representative universes (or to impose a sufficient explicit size
boundary), publishing a new expression fingerprint, and refreezing every
dependent artifact. This proof worker cannot silently substitute that repaired
target.

An independent downstream blocker remains. Pinned
`Mathlib.Algebra.BrauerGroup.Defs` explicitly leaves the tensor-product
abelian-group structure as TODO 1. The pinned dependency closure contains no
`CommGroup (BrauerGroup K)` instance or terminal body for the complete quotient
group construction. Partial representative constructions cannot inhabit the
false frozen universal package or close tensor-CSA preservation, congruence,
descent, and the group laws.

No positive proof body or receipt was added. Lifecycle remains `planned`; the
accepted structured root vector remains `[H1, M3, R3]`; the proof item remains
`[ ]`; and theorem completion remains false. This packet proposes the corrected
machine diagnosis `[H1, M5, R3]`, because rev-5.6 classifies an invalid frozen
target as M5, but a proof worker cannot rewrite the authoritative prerequisite
artifacts or accept that debt-vector transition. The direct prerequisite
`S56-M-0424-OBLIGATION_TREE` is only provisional `[_]`, not master-accepted
`[x]`. This is the fifty-fifth unresolved head-specific retry recorded in the
owned dossier. The rev-5.6 five-tick split threshold has been exceeded, so the
master or scheduler must split or reopen the invalid statement dependency
before another proof retry. This worker does not own the execution DAG.
Because the assigned phase is not complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Scoped validation

All checks ran in this worker clone. The automation-provided `.lake` symlink to
the canonical pinned artifacts was used read-only. Lean outputs were confined
to a disposable `/tmp` directory and removed by a trap. No `lake update`,
`lake build`, dependency clone or fetch, network access, or `.lake` mutation
was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0 | Rank 78; lifecycle planned; theorem incomplete. |
| DAG query for the proof node and its direct prerequisite | 0 | Obligation tree is `[_]` with one attempt; proof is `[ ]` with zero attempts. |
| `LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-0424/check_statement.py` | 0 | Exact expression hash `62cfee70820b2f8bc4e924505b8984993322f623109868957b726b3446fc3aa8`; all four mutations killed. |
| `python3 Stage1_Instances/THM-M-0424/check_anchor_audit.py` | 0 | Six immutable candidates verified; exact root remains M3. |
| `python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py` | 0 | 18 obligations and 35 typed edges passed; denominator `83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00`; root open M3. |
| Isolated trust-zero `lake env lean` recipe below | 0 | Statement, universe counterexample, and conditional composition elaborated; exact target was refuted at `{1,0}`; all four counterexample declarations and the conditional adapter reported exactly `propext`, `Classical.choice`, and `Quot.sound`; every `assert_no_sorry` passed. |
| Scoped prohibited-construct scan of all owned Lean files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, declared `axiom`, `constant`, `opaque`, `unsafe`, `external`, `native_decide`, or `implemented_by`. |
| Search for a `CommGroup (BrauerGroup ...)` instance in the pinned dependency closure | 1 | Expected no-match; the audited definitions file still leaves this construction open. |
| Search for tensor-product central/simple preservation in pinned mathlib | 0 | Only one converse-centrality implementation line; no tensor-CSA body. |
| Pinned toolchain and dependency identity checks | 0 | Lean 4.29.0; mathlib and flt-regular revisions and trees matched their pins; inspected dependency worktrees were clean. |
| `python3 -m json.tool` plus `jq` assertions on this packet | 0 | JSON syntax, identity, base, retry 55, blocked state, negative completion flags, path scope, prerequisite state, and no-self-test boundary passed. |
| `git diff --check -- Stage1_Instances/THM-M-0424 .stage1-worker-selftest.json` | 0 | No whitespace errors in the current owned delta. |
| Trailing-whitespace scan of both new artifacts | 1 | Expected no-match. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful narrow Lean replay used a fresh `/tmp` output directory:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-0424"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-0424-031437b3-slot10.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
base_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$lean_root"
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600s \
  lake env lean --trust=0 -t0 --root="$target" \
  -o "$tmp/Statement.olean" "$target/Statement.lean" \
  >"$tmp/statement.out" 2>&1
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 600s \
  lake env lean --trust=0 -t0 --root="$target" \
  -o "$tmp/UniverseCounterexample.olean" \
  "$target/UniverseCounterexample-2026-07-14-head-5753c6ed.lean" \
  >"$tmp/counterexample.out" 2>&1
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600s \
  lake env lean --trust=0 -t0 --root="$target" \
  -o "$tmp/ObligationTree.olean" "$target/ObligationTree.lean" \
  >"$tmp/obligation-tree.out" 2>&1
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

Pinned environment: Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; flt-regular revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` with tree
`32c9eace926573a9981787ae97643e520353c893`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Resume only after statement repair and dependent rev-5.6 refreezing are
accepted, followed by real placeholder-free construction and group-law bodies
or an immutable compatible pinned proof. This artifact claims no proof-node
state transition, audit completion, validation, release, or master acceptance.
