# Obligation-tree validation record

Item: `S56-M-0414-OBLIGATION_TREE`  
Base revision: `6e0ec7fe6fe851da29c6202c7ad2345f35f17800`

## Frozen result

Registry version 1 contains four required machine obligations and no exclusions: the exact root,
the UFM bridge, the explicit finite-product bridge, and the separate release trust gate. The human
source denominator excludes only the governance-only trust gate. Historical statement aliases and
the legacy wrapper are explicitly non-denominator surfaces and cannot duplicate proof-body credit.

The typed graph bundle separates proof, refinement, provenance, evidence, trust, documentation, and
workflow edges. The proof graph is acyclic; both mathematical children are root-reachable, while the
trust node is linked only as a release gate. `components_compose` kernel-checks exact conditional
child-to-parent composition. It does not prove or accept either child.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1..1546 pass |
| `python3 scripts/stage1_target.py show THM-M-0414` | 0 | rank 69, planned, L0/rework-required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0414/ObligationTree.lean` | 0 | exact anchor types print; conditional composition elaborates; axioms are `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0414/validate_obligation_tree.py` | 0 | 4 obligations, 2 proof edges, acyclic reachability, separate trust gate, all ledgers at most 100 |
| `python3 -m json.tool` on registry, graph bundle, and proof-unit manifest | 0 | all three parse |
| `git diff --check -- Stage1_Instances/THM-M-0414` | 0 | no whitespace errors |

Artifact SHA-256 values at validation:

- `ObligationTree.lean`: `a90129d8ce1293e658ff04e09c689142d1fd04fe2a04729572ad7320c766c413`
- `obligation-registry.json`: `441286a90669b8da023fdf1d4167306df19010c5eec1d371ff0ae072329cdfba`
- `typed-graphs.json`: `81df7d3a7871a3a6eb2ec15b98f24d9d432501536c6bd7c7f587e3e8f6da8b86`
- `proof-units.json`: `aa8721e5bce677ec448020a3a3870bae2903d38af2a60cd295e70a4a65557f8d`
- `obligation-tree.md`: `807f869df8023fd984ff643b76ced2ecb8871306bc1dfad67db6bfed84dc310b`
- `validate_obligation_tree.py`: `0d737df7003ed436726c15b3bbf46819453cb284f36ddcd7d4fe99845b77c8cc`

The pre-existing untracked `Formalizations/Lean/.lake` symlink/artifact surface was reused and not
modified by dependency update, fetch, or build commands.

## Boundary

This self-test covers the obligation-tree deliverable only. The terminal theorem bodies remain
proof-phase work; transitive provenance, full TCB, source H0, readable R0, hermetic replay, and
independent validation remain open. Audit completion and theorem completion are false. No master
checklist state or authoritative DAG was edited.
