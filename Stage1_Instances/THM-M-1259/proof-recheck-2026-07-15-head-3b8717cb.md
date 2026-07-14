# THM-M-1259 proof-phase recheck at current base

Item: `S56-M-1259-PROOF`

Recheck time: `2026-07-15T05:16:40+08:00`

Base revision: `3b8717cbd2522021f51b31515baf8c2db0906f45`

Base tree: `84e0292af3894ac1fd673484d8dad0a65d7103fb`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen target. The existing
owned, placeholder-free declaration

```text
Stage1Instances.THM_M_1259.Counterexample.not_hormanderTarget :
  Not Stage1Instances.THM_M_1259.hormanderTarget
```

kernel-checks against the pinned closure at trust level zero.

The target admits `n = r = 0` and quantifies over every measure. At the zero measure, its
smooth-density predicate characterizes only the zero distribution. In zero-dimensional Euclidean
space, bracket generation is automatic, the bundled zero operator maps the nonzero evaluation
distribution to zero, and that zero image is smooth. The target's hypoellipticity conclusion would
therefore make the nonzero evaluation distribution smooth relative to the zero measure, which is a
contradiction.

This refutes only the overbroad frozen Lean encoding, not Hormander's mathematical theorem. No
positive proof body or receipt was added, no obligation was closed, and the item remains `[ ]`.
Lifecycle remains `planned`; the recorded vector remains `[H2, M4, R3]`. The negative evidence
supports a fail-closed `[H5, M5, R3]` classification, but this worker does not modify authoritative
state. Audit and theorem completion are false. `.stage1-worker-selftest.json` is deliberately
absent because the assigned proof phase is incomplete.

## Failed gate and retry

The first failed gate is exact-target consistency. Rev-5.6 classifies a refuted target as `H5` and
blocks ordinary positive proof execution. Repair requires reopening `S56-M-1259-STATEMENT`, binding
a source-audited reference measure and all source-required nondegenerate conditions, and accepting
a new exact-expression fingerprint and obligation-registry version. Anchor audit, obligation-tree
construction, and proof execution must then be repeated against that repaired target.

Even after repair, the localized commutator estimate and regularity bootstrap need real Lean proof
bodies or an eligible immutable pinned proof. The checked theorem
`expandedCore_composes_hormanderTarget` is only a conditional wrapper and cannot close its unproved
analytic-core premise.

Thirteen earlier proof-attempt JSON packets are tracked. This exceeds the five-tick split threshold.
Splitting a positive proof of a refuted proposition cannot help; scheduling must redirect to the
statement dependency rather than issue the same proof task again.

## Validation

All commands ran in this worker clone against existing pinned Lake artifacts. No `lake update`,
`lake build`, dependency clone/fetch, network discovery, or `.lake` mutation was performed. The
automation-provided untracked `Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1259` | 0 | Rank 161; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| isolated pinned `lake env lean --trust=0` replay | 0 | An independent current-turn proof-search replay elaborated `Statement.lean` and `Counterexample.lean` and reported `statement_exit=0` and `counterexample_exit=0`; a separate audit replay also succeeded. |
| prohibited-construct scan over the statement and counterexample | 1 | Expected no-match exit; no `sorry`, `admit`, axiom declaration, unsafe escape, or native/oracle bypass occurs. |
| `cd Formalizations/Lean && lake env lean --version; lake --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| JSON parse and packet invariant checks; `test ! -e .stage1-worker-selftest.json` | 0 | The structured packet is valid and internally consistent; no completion manifest exists. |
| `git diff --check` and normalized no-index whitespace checks | 0 | No whitespace errors in either new owned artifact. |

Exact isolated replay recipe:

```bash
set -euo pipefail
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH="$LP" "$LEAN" --trust=0 -R Stage1_Instances/THM-M-1259 \
  -o "$tmp/Statement.olean" Stage1_Instances/THM-M-1259/Statement.lean
LEAN_PATH="$tmp:$LP" "$LEAN" --trust=0 -R Stage1_Instances/THM-M-1259 \
  Stage1_Instances/THM-M-1259/Counterexample.lean
```

The integrated axiom report for `not_hormanderTarget` is exactly:

```text
[propext, Classical.choice, Quot.sound]
```

Scoped prohibited-construct scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide' \
  Stage1_Instances/THM-M-1259/Statement.lean \
  Stage1_Instances/THM-M-1259/Counterexample.lean
```

The scan returned the expected no-match exit `1`. Source SHA-256 identities are:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `8258728ff71980a4431fb47213487c8d7655c64d0dd0f3ab2e9b058f8a95c0c7` |
| `Counterexample.lean` | `91e1610bf3fab308b7d8025415eae1db9e2d284a7e06c415baf3be47bfa74ad1` |
| `obligation_registry.json` | `2eb6b3db5d79dbed5b9f22dd467cfb964b15a3441927919e635670715342d1a0` |
| `typed_graphs.json` | `d48d5c6724a1716e82685ad535cfc8dcc1df6f3f75fc5fe691d6e13fcab7259b` |

The JSON companion binds these identities, the exact blocker, retry condition, commands, and
changed paths. This current-base packet is durable blocker evidence only; it is not a proof receipt
and does not satisfy `S56-M-1259-PROOF`.
