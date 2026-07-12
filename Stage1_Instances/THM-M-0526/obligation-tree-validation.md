# Obligation-tree validation record

Item: `S56-M-0526-OBLIGATION_TREE`  
Base revision: `d32ee3e587dde284252b4e4a328278a11472c6c3`

## Frozen architecture

`obligation-registry.json` freezes 17 required canonical obligations, nine logical leaves, and a
denominator digest of `6ee9cb595c6fee2025b76834826de8a48bb4a0bcb6fa86a8d3d91a17632452f5`.
All 17 nodes remain open; the frozen root cut set is the nine leaves. `typed-graphs.json` keeps
proof, refinement, provenance, evidence, trust, documentation, and workflow edges separate.

`ObligationTree.lean` checks the exact interfaces and child-to-parent composition for the fixed-cover
pushout and the canonical root. It introduces no theorem axiom or placeholder. The axiom reports for
both certificates are exactly `[propext, Classical.choice, Quot.sound]`; in particular, neither
contains `sorryAx`. These reports concern composition terms under open typed package hypotheses and
are not proof closure.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target coverage valid |
| `python3 scripts/stage1_target.py check` | 0 | ordered 1546-target manifest valid |
| `python3 Stage1_Instances/THM-M-0526/check_obligation_tree.py` | 0 | 17 obligations, nine leaves, 16 proof edges, all seven graph types, digest and acyclicity validated |
| `rm -rf /tmp/thm-m-0526-olean && mkdir -p /tmp/thm-m-0526-olean/Stage1_Instances/THM-M-0526 && lake env lean -R ../.. -o /tmp/thm-m-0526-olean/Stage1_Instances/THM-M-0526/Statement.olean ../../Stage1_Instances/THM-M-0526/Statement.lean && LEAN_PATH=/tmp/thm-m-0526-olean lake env lean ../../Stage1_Instances/THM-M-0526/ObligationTree.lean` (cwd `Formalizations/Lean`) | 0 | exact target dependency and both composition certificates elaborated; axiom reports printed; only the pre-existing unused-section-variable warning in `Statement.lean` occurred |
| `git diff --check` | 0 | no whitespace errors |

The `/tmp` output directory avoids writing compiled artifacts into the repository or the canonical
pinned `.lake` dependency tree. The worker clone's `Formalizations/Lean/.lake` is a pre-existing
untracked symlink to the canonical pinned artifacts and was used read-only.

## Boundary

This phase is self-tested pending master acceptance. It freezes architecture and verifies typed
composition only. It provides zero closed logical leaves, zero terminal proof bodies, no H0/R0,
and no theorem proof, audit completion, or theorem completion. The next proof phase must implement
the nine-leaf cut set (splitting further whenever a substantive ledger would exceed 100 steps) and
then check every nonleaf composition against those implementations.
