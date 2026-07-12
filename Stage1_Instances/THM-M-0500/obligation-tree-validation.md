# THM-M-0500 obligation-tree validation

Validation date: 2026-07-12 (Asia/Shanghai). Base revision:
`e9252b1cfdc99a094324c8a10d260769df2eca15`.

The obligation phase freezes 14 semantic obligations with denominator SHA-256
`c06d16baf16004048b78be89babd76c454d2d44d1ed271ecc51cb376425908a1`. The seven
separate graph families contain 26 typed reciprocal/support edges. The proof graph is acyclic and
its exact root-reachable set is checked structurally. The Lean harness checks only the conditional
composition from non-summability and support packages to the canonical root.

## Executed commands

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1..1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0500` | 0 | rank 877, planned, legacy artifacts unaccepted, theorem completion false |
| `python3 Stage1_Instances/THM-M-0500/check_obligation_tree.py` | 0 | 14 obligations, 26 typed edges, exact denominator, open M3 root |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0500/ObligationTree.lean` | 0 | conditional composition elaborated; exact two upstream boundary types printed; axioms are `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 -m json.tool` on the registry, graph bundle, validation specs, receipt, and instance | 0 | all five structured artifacts are valid JSON |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b\|sorryAx' Stage1_Instances/THM-M-0500 -g '*.lean'` | 1 | expected no-match result; no prohibited placeholder or custom axiom in owned Lean source |
| `git diff --check -- Stage1_Instances/THM-M-0500 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The worker clone reused the canonical pinned `.lake` artifacts. No update, build, fetch, clone, or
other dependency mutation was run.

## Status boundary

This validates the registry freeze, graph typing/reciprocity/reachability, structured recipes, and
conditional composition. It does not integrate or accept the pinned proof bodies. Primary-source
H0, readable R0, full transitive provenance/trust closure, audit completion, proof acceptance,
release validation, and theorem completion remain open. The minimal root cut is
`M0500-T-NONSUM` plus `M0500-L-SUPPORT`.
