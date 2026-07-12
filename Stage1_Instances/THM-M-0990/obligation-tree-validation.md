# Obligation-tree validation record

Item: `S56-M-0990-OBLIGATION_TREE`  
Base revision: `145913a43751692bfcac4bceaaf3debfe4574cf6`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Registry version 1 freezes 18 unique semantic obligations against the statement and anchor-audit
hashes. The frozen denominator is
`fa799ae86623298ad54105d2041f7903144cc398f769b7da7a3865507a9921f6`: 16 obligations require
machine treatment, 14 require human-source treatment, all 18 require readable treatment, and two
are informational overlays. There are no exclusions and no recorded closed obligations.

The graph bundle contains 43 typed edges in separate proof, refinement, provenance, evidence,
trust, documentation, and workflow graphs. Proof edges are reciprocal and acyclic. Every node has
debt, provenance, validity, validation, semantic-ledger, and readable-target fields, with a step
budget no greater than 100.

`ObligationTree.root_compose` kernel-checks the conditional final composition. Its axiom report is
`propext`, `Classical.choice`, and `Quot.sound`. This is composition evidence, not proof of the
Lyapunov CLT. The root remains open at `M3`; the frozen cut set is
`M0990-T-TRIANGULAR-BRIDGE` because no exact pinned terminal theorem was found.

## Commands and results

All commands used existing pinned artifacts. No Lake update/build, dependency fetch/clone, or
`.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0990/build_obligation_artifacts.py` | 0 | deterministically wrote 18 obligations and 43 typed edges; denominator `fa799a...921f6` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0990/ObligationTree.lean` | 0 | root shape and conditional composition elaborated; axioms were `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0990/check_obligation_tree.py` | 0 | hashes, denominators, node schemas, typed reciprocity, reachability, recipes, cut set, and placeholder hygiene passed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0990` | 0 | rank 270, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0990 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This node is self-tested pending master acceptance. It freezes architecture only and supplies no
accepted proof node, primary-source review, readable reconstruction review, hermetic validation,
independent verification, audit completion, or theorem-completion credit.
