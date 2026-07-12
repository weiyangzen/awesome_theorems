# Obligation-tree validation record

Item: `S56-M-0646-OBLIGATION_TREE`  
Base revision: `302112912689e2e6fcac50a7c0b0ab94afaef090`  
Validation date: 2026-07-12 (`Asia/Shanghai`)

## Result

Registry version 1 freezes thirteen unique obligations against the exact `Statement.lean` and
anchor-audit hashes. Its denominator is
`ed7e70d34e6d75e3dea6c14c9ae794e000d0a897a1ddc4e91168d68069b222d1`: eleven obligations require
machine treatment, eleven require human-source treatment, all thirteen require readable treatment,
and two are informational overlays. No obligation is excluded or recorded closed.

The bundle contains 36 edges across separate proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs. Proof edges are reciprocal and acyclic. Every node has a typed
semantic ledger and a step budget of at most 30. Eight distinct mathlib terminal bodies are pinned
and deduplicated, so the local assembly theorem and wrapper declarations cannot inflate proof-body
coverage.

`ObligationTree.root_compose` kernel-checks the exact root composition from the explicit pinned
elementary-equivalence interface. Its axiom report is `propext` and `Quot.sound`. This phase does
not discharge that interface: the root remains open at `M4`, with immediate cut set `B-EQUIV`.

## Commands and results

All commands used existing pinned artifacts. No Lake update/build, dependency fetch/clone, or
`.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0646/build_obligation_artifacts.py` | 0 | deterministically wrote 13 obligations and 36 typed edges; denominator `ed7e70d3...b222d1` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0646/ObligationTree.lean` | 0 | root, conditional composition, and eight imported construction boundaries elaborated; composition axioms were `propext`, `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0646/check_obligation_tree.py` | 0 | hashes, denominators, schemas, graph reciprocity, acyclicity, reachability, recipes, cut set, and placeholder hygiene passed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0646` | 0 | rank 692, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0646 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This node is self-tested pending master acceptance. It freezes architecture only and supplies no
accepted proof node, `H0` source review, `R0` readable reconstruction, hermetic validation,
independent verification, audit completion, or theorem-completion credit.
