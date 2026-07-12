# Obligation-tree validation record

Item: `S56-M-0993-OBLIGATION_TREE`  
Base revision: `63c9df120569955b7d80ca9bb1940c30a3b9d18b`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Registry version 1 freezes ten unique obligations against the exact statement and anchor-audit
hashes. Its denominator is
`e70d44f33d60421b5f0e9e0db91f7c8c9ade6c8873859dcbf7b99a7a2b663df1`: eight obligations require
machine treatment, seven require human-source treatment, all ten require readable treatment, and
two are informational overlays. No obligation is excluded or recorded closed.

The bundle contains 21 edges across separate proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs. Proof edges are reciprocal and acyclic. Every semantic leaf
has a typed ledger and a step budget below 100. The three imported terminal bodies have distinct,
immutable provenance IDs, so wrappers and the assembly theorem cannot inflate closure coverage.

`ObligationTree.root_compose` kernel-checks the exact parent composition from explicit sum
integrability, exponential-Markov, and MGF-factorization interfaces. Its axiom report is `propext`,
`Classical.choice`, and `Quot.sound`. This phase does not discharge those interfaces: the root
remains open at `M1`, with cut set `L-SUM-INT`, `L-MARKOV`, and `L-FACTOR`.

## Commands and results

All commands used existing pinned artifacts. No Lake update/build, dependency fetch/clone, or
`.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0993/build_obligation_artifacts.py` | 0 | deterministically wrote 10 obligations and 21 typed edges; denominator `e70d44...663df1` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0993/ObligationTree.lean` | 0 | exact root and conditional composition elaborated; axiom report was `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0993/check_obligation_tree.py` | 0 | hashes, denominators, schemas, graph reciprocity, acyclicity, reachability, recipes, cut set, and placeholder hygiene passed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0993` | 0 | rank 273, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0993 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This node is self-tested pending master acceptance. It freezes architecture only and supplies no
accepted proof node, H0 source review, readable reconstruction review, hermetic validation,
independent verification, audit completion, or theorem-completion credit.
