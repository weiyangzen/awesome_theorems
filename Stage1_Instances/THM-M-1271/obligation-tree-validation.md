# Obligation-tree validation record

Item: `S56-M-1271-OBLIGATION_TREE`  
Base revision: `3a3bd9b5ae3837526b6a41daf06c7587654c209d`

## Frozen architecture

The version-1 registry freezes 13 canonical obligations before proof execution. Its denominator is
`sha256:2f6d1a3dc9064aff967ba0cf8443ff438e9cb99e0b2d34994252e6410d2d75bc`.
Separate typed proof, refinement, provenance, evidence, trust, documentation, and workflow graphs
record reciprocal proof composition and non-proof support boundaries. Every node has the rev-5.6
schema, an explicit semantic ledger, a step budget at most 100, ownership, validation recipe, debt,
and an open-state boundary.

`root_of_barrier_and_critical_packages` kernel-checks exact composition from the geometric barrier
package and the analytic critical-point package into `MountainPassTarget`. Both packages remain
explicit hypotheses. The root therefore remains `M3`; this phase supplies no proof or theorem-
completion claim.

## Commands and results

Commands were run from the automation-clone root unless a directory is stated.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1271/build_obligation_artifacts.py` | 0 | deterministically built 13 obligations; denominator matched the value above |
| `python3 Stage1_Instances/THM-M-1271/check_obligation_tree.py` | 0 | PASS; 13 unique obligations, 25 typed edges, reciprocal proof edges, acyclic root reachability, complete node schema, recipe coverage, and open root verified |
| `python3 Stage1_Instances/THM-M-1271/check_lean_composition.py` | 0 | rebuilt the local statement module and elaborated conditional exact-root composition against existing pinned artifacts; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`; temporary `.olean` removed |
| `git diff --check -- Stage1_Instances/THM-M-1271 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The generated `Statement.olean` is validation output and is excluded from the handoff manifest.
No `sorry`, `admit`, custom axiom, `sorryAx`, unsafe declaration, oracle, substituted statement, or
terminal proof-body claim occurs in the obligation-tree Lean artifact.

## Remaining cut set

The first open cut set is `M1271-T-BARRIER` plus `M1271-T-CRITICAL`. Their descendants require
path-height attainment, sphere crossing, construction of a minimax Palais-Smale sequence,
Palais-Smale subsequence extraction, and continuity-based limit passage. Primary-source pinpointing,
readable review, terminal provenance, hermetic release replay, and independent acceptance also
remain downstream gates.
