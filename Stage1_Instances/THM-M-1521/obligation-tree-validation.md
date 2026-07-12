# THM-M-1521 obligation-tree validation

Commands ran in the worker clone using the existing pinned Lake artifacts. No
dependency was fetched or updated.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1521/build_obligation_artifacts.py` | 0 | generated registry denominator `44b4406c73f0cc21bf502625c0c5d174c91f898e77b027121ec25f1a0818a5fb` |
| `python3 Stage1_Instances/THM-M-1521/check_obligation_tree.py` | 0 | compiled the statement to a temporary module cache with `lake env lean`, elaborated the exact conditional composition (axioms `[propext, Classical.choice, Quot.sound]`), and validated ten obligations and 21 typed edges including proof reciprocity, acyclicity, root reachability, hashes, schemas, and the open closure boundary |
| `python3 -m json.tool Stage1_Instances/THM-M-1521/obligation-registry.json` | 0 | registry parses |
| `python3 -m json.tool Stage1_Instances/THM-M-1521/typed-graphs.json` | 0 | graph bundle parses |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `git diff --check -- Stage1_Instances/THM-M-1521 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Status boundary: the obligation-tree item is self-tested and awaits master
acceptance. The root remains M3 with both imported bridge obligations open for
the proof phase. `audit_complete=false` and `theorem_complete=false`.
