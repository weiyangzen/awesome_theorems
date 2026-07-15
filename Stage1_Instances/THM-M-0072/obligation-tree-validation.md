# THM-M-0072 obligation-tree validation

Item: `S56-M-0072-OBLIGATION_TREE`

Base revision: `3c2814a370c2fee02158ca79aa44a48e411c4d18`

Base tree: `e1bd7e27bd922b779322c089410a471b6a1535f0`

Validation date: `2026-07-15` (`Asia/Shanghai`)

## Frozen Result

The version-1 registry freezes 28 unique root-relevant obligations with denominator SHA-256
`7f5030b02a13572f021c17ac32f2472098e2a5de881bc5a4999716dd411f717b`.
It follows Thompson's printed page-411 transfer proof rather than inferring a route from the
available mathlib names. The seven graph families contain 97 typed edges. Two required proof
relations have reciprocal checked `composes` edges; 20 source-derived internal relations remain
unverified `logical_decomposition` edges and receive no closure credit.

The exact Lean harness proves the inside-maximal boundary and checks the two-branch merge. Its
outside-transfer package remains an explicit premise, so the root stays open. Accepted closed
obligations and receipt IDs remain empty; the vector stays `H1/M3/R4`; audit and theorem completion
are false.

## Commands And Results

All commands ran from the repository root. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation ran.

| Command | Exit | Exact result and boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0072` | 0 | rank 1102, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0072/build_obligation_artifacts.py --write` | 0 | wrote 28 obligations and 97 typed edges; denominator `7f5030b0...717b` |
| `python3 -B Stage1_Instances/THM-M-0072/build_obligation_artifacts.py --check` | 0 | generated registry, graphs, and validation specifications match byte-for-byte |
| `python3 -B Stage1_Instances/THM-M-0072/check_obligation_tree.py` | 0 | schemas, denominator, layers, node ledgers, readable anchors, recipes, graph endpoints/reciprocity/acyclicity/reachability, workflow, hygiene, conditional Lean composition, and open-root boundary passed; Lean output SHA-256 `71e7333f...2bdc` |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0072-obligation-pycache python3 -m py_compile Stage1_Instances/THM-M-0072/build_obligation_artifacts.py Stage1_Instances/THM-M-0072/check_obligation_tree.py` | 0 | both Python tools compiled without repository cache output |
| `python3 -m json.tool` over all changed JSON and `.stage1-worker-selftest.json` | 0 | every structured artifact parsed |
| comment-aware prohibited-construct scan over `ObligationTree.lean` | 0 | no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe/opaque body, oracle, native shortcut, or external implementation |
| `git diff --check -- Stage1_Instances/THM-M-0072 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The checker obtains the pinned Lean executable and `LEAN_PATH` through `lake env`, copies
`Statement.lean` and `ObligationTree.lean` into a temporary directory, first creates a temporary
`Statement.olean`, and then elaborates the composition module against that actual declaration. It
does not write build output under the owned target or dependency tree.

## Status Boundary

This worker packet covers the obligation-tree phase only. `M0072-T-OUTSIDE` is the minimal open
machine cut. Its ten expanded proof packages, 20 internal composition certificates, full
provenance/trust closure, primary-source H0, independently reviewed R0, hermetic replay, second
runner, validation, release, `AUDIT-Z`, `THEOREM-Z`, theorem completion, and dependency-ordered
master acceptance all remain open. The pre-existing shared `.lake` link also makes this warm worker
evidence nonrelease.
