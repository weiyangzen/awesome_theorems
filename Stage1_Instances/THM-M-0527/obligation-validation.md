# THM-M-0527 obligation-tree validation

Item: `S56-M-0527-OBLIGATION_TREE`  
Base revision: `296128439d8baef83209914498e4befec8693f22`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The validator recomputed the frozen denominator, checked 34 unique registry
and node identities, required the node ledger fields and leaf budgets, checked
seven graph types plus reciprocal edge indexes, rejected duplicate edges, and
proved that the proof graph is acyclic and reaches all obligations from the
root. It found 40 typed edges. The exact statement also elaborated under the
pinned Lean 4.29.0 toolchain. The pre-existing untracked `.lake` link/artifact
was reused without dependency mutation.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0527/build_obligation_artifacts.py` | 0 | wrote 34 obligations and 40 typed edges |
| `python3 Stage1_Instances/THM-M-0527/check_obligation_tree.py` | 0 | PASS; denominator `3b54d00c...35df1`; root open M3 |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks passed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0527/Statement.lean)` | 0 | exact target elaborated and printed |
| `python3 Stage1_Instances/THM-M-0527/check_statement.py` | 0 | three mutations killed; pinned toolchain and mathlib revision matched |
| `git diff --check -- Stage1_Instances/THM-M-0527 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Generated content hashes before this validation record and self-test manifest:

```text
8d63fae58b561e019f54fd213b37c6e055a4f5e96a33b8233128e938c5eab80b  obligation-registry.json
f152d6bb427c32658bf62750cb6eca0655575577d297cb17e90bfae27c65d87b  typed-graphs.json
7b8a69c13592e24f5566a924cf135d5b4248a383ae008d6ee1b25f7bd423908a  obligation-tree-receipt.json
```

## Status boundary

This self-tests only the architecture freeze. All obligations remain open;
planned signatures and budgets are not proofs. No theorem completion or master
acceptance is claimed.
