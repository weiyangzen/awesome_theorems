# THM-M-0995 obligation-tree validation

Item: `S56-M-0995-OBLIGATION_TREE`  
Base revision: `eb5f7c9057a60dace86040954ad22ca44a040954`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Registry version 1 freezes thirteen unique obligations against the exact statement and anchor-audit
files. Denominator `40ec266a8614befd347bb0f00848703182aac04f6446a113a6a2e6b1a0348794`
covers nine machine-required nodes, ten human-source-required nodes, thirteen readable-required
nodes, and four informational overlays. No obligation is excluded or recorded closed.

The typed bundle has 24 edges across separate proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs. Proof edges are reciprocal, acyclic, and root-reachable. All
semantic units have explicit ledgers and budgets at most 100 steps.

The narrow Lean check first elaborated `Statement.lean` to a temporary local `Statement.olean`, then
elaborated `ObligationTree.lean` with the existing pinned Lake environment, and finally removed the
temporary artifact. `root_compose` checked the exact conditional composition and reported only
`propext`, `Classical.choice`, and `Quot.sound`. No dependency update, build, clone, fetch, or network
access was used.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0995/build_obligation_artifacts.py` | 0 | deterministically wrote 13 obligations, 24 typed edges, and the denominator above |
| `cd Stage1_Instances/THM-M-0995 && LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) $(cd ../../Formalizations/Lean && lake env which lean) -o Statement.olean Statement.lean && LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) $(cd ../../Formalizations/Lean && lake env which lean) ObligationTree.lean; rc=$?; rm -f Statement.olean Statement.ilean; exit $rc` | 0 | exact statement and all package types elaborated; conditional composition axiom report was `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0995/check_obligation_tree.py` | 0 | hashes, denominator, typed edges, reciprocity, acyclicity, reachability, recipes, cut set, budgets, and placeholder hygiene passed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0995` | 0 | rank 275, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0995 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This obligation-tree node is self-tested pending master acceptance. It freezes architecture only.
The root remains `M3` with cut set `L-IND-MGF`, `L-SUM-MGF`, `L-CHERNOFF`, `L-OPTIMIZE`, and
`B-ZERO-DENOM`. This work supplies no proof closure, H0 source review, R0 reconstruction,
audit-completion, release, or theorem-completion claim.
