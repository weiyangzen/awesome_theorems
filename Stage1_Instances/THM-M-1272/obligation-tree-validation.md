# THM-M-1272 obligation-tree validation

Item: `S56-M-1272-OBLIGATION_TREE`  
Base revision: `a1b16ca3ed65db2ec65e3d478d1680d9c1f5489d`

## Frozen architecture

The version-1 registry freezes 16 canonical semantic obligations independently of proof
availability. Its denominator is
`sha256:0356add2c87f163bcb8d077ee875da0ab02efd31330529b6c6d0ea453f9b35fd`.
Separate proof, refinement, provenance, evidence, trust, documentation, and workflow graphs preserve
typed boundaries and reciprocal proof composition. Every node has the required rev-5.6 fields, a
substantive semantic ledger, an explicit budget at most 100, ownership, debt, and a structured
network-denied validation recipe.

`root_of_minimax_and_limit_packages` kernel-checks composition of divergent minimax levels and
exact critical representatives into the frozen `FountainTheoremTarget`. Both inputs remain explicit
hypotheses. The first open root cut is therefore `M1272-T-LOWER-BOUND` plus
`M1272-T-CRITICAL-LEVELS`, and the root remains `M3`.

## Commands and exact results

Commands ran from the worker-clone root on 2026-07-12 unless stated otherwise.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1272/build_obligation_artifacts.py` | 0 | deterministically rebuilt 16 obligations with the denominator above |
| `python3 Stage1_Instances/THM-M-1272/check_obligation_tree.py` | 0 | PASS: 16 unique obligations, 29 typed edges, reciprocal/acyclic root graph, complete schemas, recipe coverage, and open-root boundary |
| `python3 Stage1_Instances/THM-M-1272/check_lean_composition.py` | 0 | rebuilt the local statement module, elaborated conditional exact-root composition using existing pinned Lake artifacts, and removed the temporary `.olean`; `#print axioms` reported `propext`, `Classical.choice`, and `Quot.sound` only |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1272` | 0 | rank 165, planned lifecycle, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1272 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The Lean artifact contains no proof placeholder, custom axiom, unsafe declaration, oracle, or proof
of either open package. The clone's pre-existing untracked `Formalizations/Lean/.lake` link reuses
canonical pinned artifacts; no Lake update/build, dependency fetch, or `.lake` mutation was
performed.

## Remaining boundary

Symmetric admissible-class normalization, minimax construction and linking, odd deformation,
levelwise boundedness, Palais-Smale subsequence extraction, and derivative/value limit passage are
open proof work. Primary-source pinpointing, accepted terminal provenance, readable reconstruction,
hermetic release replay, and independent master acceptance also remain open. This phase supplies no
root proof, audit-completion, or theorem-completion claim.
