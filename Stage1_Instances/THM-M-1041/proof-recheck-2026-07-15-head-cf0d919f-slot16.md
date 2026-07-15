# THM-M-1041 proof-phase recheck at current base

Item: `S56-M-1041-PROOF`

Intent: `prove`

Recorded: `2026-07-15T22:29:48+08:00`

Base revision: `cf0d919f2dfc00f3f777e9319188dec0f644d159`

Base tree: `993e3e180c52396b1dd8c970410284d8c3e5bf8d`

## Verdict

`blocked`; no state change. No eligible proof body was implemented or found for
the exact root `Stage1Instances.THM_M_1041.HilleYosidaContractionTarget`.
The item stays `[ ]`, lifecycle stays `planned`, root vector stays
`[H2, M4, R4]`, and neither audit completion nor theorem completion is claimed.

The target is the full real Banach-space contraction Hille--Yosida
equivalence. A premise-free proof must inhabit both `ForwardPackage` and
`ConversePackage`. The checked `root_of_directionPackages` theorem only
composes those two arguments; it constructs neither and receives no root proof
credit. The minimal open root cut remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse construction is `M1041-C-YOSIDA-APPROX`. Closing
the exact target requires new proofs of generator closedness and density; a
Laplace/Bochner resolvent with both inverse laws and its contraction estimate;
and Yosida approximants, a limiting semigroup, semigroup laws, strong
continuity, contraction, and exact generator identification.

Frozen proof inputs and pins are byte-identical to their target-changing state
at `76c08cb569093ff0ea02564e80dced5284ebd59d`. Repository history, duplicate
`THM-M-0330`, and legacy `S1_M_234` contain definitions, abstract interfaces,
transports, or conditional composition only. A fresh search of all 9,676 Lean
sources in the pinned package cache found no Hille--Yosida or strongly
continuous semigroup generator declaration. The audited external candidates
remain outside the pinned closure and incomplete for the exact root; none was
fetched, built, integrated, or credited.

No statement shortcut is available. The `NNReal` right-neighborhood filter is
nontrivial, so the generator predicate is not vacuous. The identity semigroup
and zero generator give a consistent special case, not the universally
quantified theorem. Both resolvent inverse equations and the norm bound remain
substantive. Assuming a direction package, weakening the equivalence, or
replacing its analytic predicates with abstract fields would introduce an
unproved premise or substitute a different theorem.

There are 43 prior dated unresolved proof JSON records and 44 including this
one. This is beyond the mandatory five-tick split threshold in blueprint
section 10.2 and the execution skill. The master should accept or repair the
obligation-tree prerequisite and split the proof item into dependency-legal
children for the fourteen frozen packages. This worker did not edit the
authoritative DAG or generated checklist.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned cache was reused read-only. No `lake update`, `lake build`,
dependency clone/fetch/checkout, or `.lake` mutation was performed. Lean object
output was isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; date --iso-8601=seconds; uname -srmo; git status --short --untracked-files=all` | 0 | Base and tree match above; initial status contained only the automation-provided untracked `.lake` symlink. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check; python3 scripts/stage1_target.py show THM-M-1041` | 0 | Passed all 1546 targets; rank 234 remains `planned`, L0/rework-required, and theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Expression hash `e6e5f0cb...f7768d` matched; all three structural mutations were killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | Passed 21 obligations and 56 typed edges; denominator `b9ebe90e...b39c42`; root and both packages remained M4. |
| Direct pinned `lean --trust=0 -t0` replay | 0 | Exact statement and conditional composition elaborated; `root_of_directionPackages` reported `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical scan | 1 expected | No match among 9,676 pinned Lean source files. |
| Scoped prohibited-token scan | 1 expected | No prohibited proof-device token in owned Lean sources; supporting lexical evidence only. |
| Compare proof inputs and pins with `76c08cb5...59d` | 0 | Statement, composition, registry, graphs, audit, validation specs, Lake manifest, and toolchain are unchanged. |

Exact narrow Lean replay:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-head-cf0d919f-slot16.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 \
  "$lean" --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 \
  "$lean" --trust=0 -t0 ObligationTree.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry Condition

The master should accept or repair the obligation-tree prerequisite and split
this oversized proof item into dependency-legal children for the fourteen
frozen packages. Then implement them without placeholders. The alternative is
an immutable compatible exact Lean 4 proof already in the pinned closure that
passes exact-type, provenance, placeholder, axiom, composition, and trust
checks.

This is fresh current-base, warm-cache, nonrelease blocker evidence only. It
does not satisfy `S56-M-1041-PROOF`, change scheduler state, close either
direction package or the root, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance. Because the
proof phase is not genuinely complete, `.stage1-worker-selftest.json` is
deliberately absent.
