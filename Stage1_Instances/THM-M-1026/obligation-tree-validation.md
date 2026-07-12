# Obligation-tree validation record

Item: `S56-M-1026-OBLIGATION_TREE`  
Base revision: `10f401f7930445a054adc972ae261c1a33df716e`

## Frozen architecture

Registry version 1 contains 16 unique canonical obligations: 14 machine-required obligations and
two informational source/provenance overlays. Its denominator SHA-256 is
`e74cb65a6278468b7696e4ce10a93ccbe318c57ff57bf51b541680529880f3b2`. The typed bundle separates
proof, refinement, provenance, evidence, trust, documentation, and workflow graphs and contains 46
typed directed edges. Every proof requirement has a reciprocal composition edge.

The minimal open root cut is the exact necessity and converse propositions. `ObligationTree.lean`
checks only that these two complete directions compose to the frozen biconditional. This conditional
interface is not evidence that either direction is proved.

## Commands and results

All commands ran in this worker clone on 2026-07-12. Lean used existing pinned Lake artifacts. No
dependency was fetched, updated, or built.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1026/build_obligation_artifacts.py` | 0 | deterministically generated registry, typed graphs, and validation specifications |
| `python3 Stage1_Instances/THM-M-1026/check_obligation_tree.py` | 0 | PASS; 16 obligations, 46 edges, frozen denominator matched, root open at M3 |
| `cd Formalizations/Lean && lake env lean -R ../.. -o ../../Stage1_Instances/THM-M-1026/Statement.olean ../../Stage1_Instances/THM-M-1026/Statement.lean` | 0 | produced the local statement module needed by the narrow import check |
| `cd Formalizations/Lean && LEAN_PATH=../../Stage1_Instances/THM-M-1026 lake env lean -R ../.. ../../Stage1_Instances/THM-M-1026/ObligationTree.lean` | 0 | checked `root_of_directions`; axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1026` | 0 | rank 502, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool` on all three generated JSON artifacts | 0 | valid JSON |
| prohibited-token scan over this phase's Lean and structured artifacts | 0 | no proof-gap declaration |
| `git diff --check -- Stage1_Instances/THM-M-1026 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The temporary `Statement.olean`/`Statement.ilean` files used for the narrow module import were
removed immediately after elaboration and are not evidence artifacts.

## Status boundary

This node is self-tested architecture evidence pending master acceptance. Necessity, converse,
primary-source pinpointing, transitive TCB closure, readable reconstruction, proof, hermetic replay,
and independent validation remain open. Root machine debt remains `M3`; theorem completion is false.
