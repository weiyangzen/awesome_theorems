# Obligation-tree validation record

Item: `S56-M-0988-OBLIGATION_TREE`  
Base revision: `3c49a04f350afa3376ed84e511f0c4e1e03dbe06`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Registry version 1 freezes 18 unique semantic obligations against the exact statement and anchor
audit hashes. The frozen denominator is
`e5bd80bd684e277b213f25d9bf0a41a2611240e81ff8efd7f3198f20e7bfbdbb`: 16 obligations require
machine treatment, 14 require human-source treatment, all 18 require readable treatment, and two
are informational overlays. There are no exclusions and no recorded closed obligations.

The graph bundle contains 29 typed edges across separate proof, refinement, provenance, evidence,
trust, documentation, and workflow graphs. Proof edges are reciprocal, acyclic, and make the exact
pinned theorem bridge reachable from the root through the conditional assembly node. The
refinement graph exposes both variance branches and the centering, scaling, construction, moment,
iid, characteristic-function, and transport obligations hidden inside the terminal mathlib body.
Every node has the required debt, provenance, validity, validation, ledger, and readable-target
fields, with a substantive step budget no greater than 100.

`ObligationTree.root_compose` kernel-checks the exact parent composition while accepting the pinned
bridge as an explicit premise. Its axiom report is `propext`, `Classical.choice`, and `Quot.sound`.
This is composition evidence, not unconditional proof evidence. The root remains open at `M1` with
cut set `M0988-X-PINNED` for the later proof phase.

## Commands and results

All commands used the existing pinned artifacts. No Lake update/build, dependency fetch/clone, or
`.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0988/build_obligation_artifacts.py` | 0 | deterministically wrote 18 obligations and 29 typed edges; denominator `e5bd80...fbdbb` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0988/ObligationTree.lean` | 0 | exact root and conditional composition elaborated; axiom report was `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0988/check_obligation_tree.py` | 0 | hashes, denominators, node schemas, typed reciprocity, reachability, recipes, cut set, and placeholder hygiene passed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0988` | 0 | rank 268, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0988 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This node is self-tested pending master acceptance. It freezes architecture only and supplies no
accepted proof node, primary-source review, readable reconstruction review, hermetic validation,
independent verification, audit completion, or theorem-completion credit.
