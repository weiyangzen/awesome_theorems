# Obligation-tree validation

Item: `S56-M-0772-OBLIGATION_TREE`  
Theorem: `THM-M-0772`  
Base revision: `296128439d8baef83209914498e4befec8693f22`  
Validation date: 2026-07-12 (Asia/Shanghai)

All commands ran in this worker clone. Lean used the already materialized pinned Lake artifacts;
no update, build, clone, fetch, or other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0772/build_obligation_artifacts.py` | 0 | Wrote 13 frozen obligations and 25 typed edges |
| `python3 Stage1_Instances/THM-M-0772/check_obligation_tree.py` | 0 | Registry denominator, node schema, seven graph partitions, reciprocal proof edges, reachability, acyclicity, recipes, no-placeholder scan, and open-root boundary passed |
| `lake env lean ../../Stage1_Instances/THM-M-0772/ObligationTree.lean` (from `Formalizations/Lean`) | 0 | Conditional child-to-root composition and audited bridge signature elaborated; composition axiom set was empty and bridge axiom set was `[propext, Classical.choice, Quot.sound]` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard validator passed for 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | Ordered manifest passed: 1546 unique L0/rework-required targets |
| `python3 scripts/stage1_target.py show THM-M-0772` | 0 | Rank 580, planned statement-first lane, theorem incomplete |
| `python3 -m json.tool` on the registry, typed graphs, and validation specs | 0 | All structured artifacts parsed |
| scoped SHA-256 regeneration comparison | 0 | Generated structured artifacts were byte-identical after regeneration |
| `git diff --check -- Stage1_Instances/THM-M-0772 .stage1-worker-selftest.json` | 0 | No whitespace errors |

This self-test validates only the obligation-tree deliverable. The root is deliberately open at
`M3`, with `M0772-X-MATHLIB-BODY` as the frozen remaining cut set. The mathlib bridge remains a
provisional `M0-W` candidate until downstream proof and provenance acceptance. Human-source review,
release-grade trust closure, hermetic replay, independent validation, and master acceptance remain
known failures; no theorem-completion claim is made.
