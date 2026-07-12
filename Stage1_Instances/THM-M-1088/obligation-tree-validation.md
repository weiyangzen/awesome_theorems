# Obligation-tree validation record

Item: `S56-M-1088-OBLIGATION_TREE`  
Validation date: `2026-07-12`  
Base revision: `f380c3f234a2eca83382206806bd82232b6e2777`

## Frozen architecture

Registry version 1 contains 19 unique root-relevant semantic obligations. Sixteen are
machine-required; `M1088-X-SOURCE` is a human-source boundary and `M1088-X-PROVENANCE` plus
`M1088-X-TRUST` are informational governance overlays. The frozen denominator digest is
`56fb1860d804859c9580000d4f003ce8ad997dea3f9e40aca50d5b1efe921f3d`.

Seven separate typed graphs contain 43 edges. The proof graph has reciprocal
`proof_requires`/`composes` edges and is acyclic. Support graphs cannot become proof premises.
Every node has the required schema, a substantive ledger, a budget no greater than 100, and a
structured validation recipe with explicit cwd, argv, environment, timeout, network policy, and
covered obligation.

`ObligationTree.lean` independently re-elaborates the exact statement interfaces and checks the
conditional child-to-root composition theorem `target_of_upperTailEngine`. Its axiom report is
`propext`, `Classical.choice`, and `Quot.sound`; there is no `sorryAx`. The exact upper-tail engine
is a parameter of that theorem, not a hidden proof or axiom.

## Commands and results

All Lean commands reused the existing pinned Lake closure. No dependency update, build, clone, or
fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1088/build_obligation_artifacts.py` | 0 | generated 19 obligations, 43 typed edges, and the denominator digest above |
| `python3 Stage1_Instances/THM-M-1088/check_obligation_tree.py` | 0 | PASS; open M3 root and `M1088-T-ENGINE` root cut set |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1088/Statement.lean` | 0 | exact canonical target re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1088/ObligationTree.lean` | 0 | exact conditional composition elaborated; axiom report has no `sorryAx` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and uniform target set valid |
| `python3 scripts/stage1_target.py check` | 0 | ordered 1,546-target manifest valid |
| `python3 scripts/stage1_target.py show THM-M-1088` | 0 | rank 530, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1088 .stage1-worker-selftest.json` | 0 | no whitespace errors |

One initial Lean invocation tried to import the dossier as a Lake module and failed because the
dossier lies outside the Lake module search path. The corrected standalone file re-elaborates the
hash-bound exact interfaces, and the recorded narrow command passes. A separate attempted `lean -R`
invocation was malformed and exited after printing usage; it did not mutate artifacts.

## Open root boundary

This architecture phase is self-tested pending master acceptance. `closed_obligations` remains
empty. Finite-dimensional concentration, covariance normalization, finite exhaustion, mean and
event limit passage, primary-source acceptance, transitive provenance/trust, readable
reconstruction, hermetic replay, and independent verification remain open. The root remains
`[H2, M3, R4]`; no `H0`, `M0`, `R0`, `AUDIT-Z`, or theorem completion is claimed.
