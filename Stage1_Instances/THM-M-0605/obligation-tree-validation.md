# Obligation-tree validation

Item `S56-M-0605-OBLIGATION_TREE` freezes registry version 1 with 19 unique semantic
obligations and denominator SHA-256
`c6e29bccc0135529afc98b27c38f6c5265449f1fd054602ec55fe9d9e5b6e5b7`. Seven separate typed
graphs contain 90 edges. The structural checker verifies complete node schemas, denominator
projections, typed endpoints and adjacency indexes, reciprocal proof/composition edges,
proof-DAG acyclicity, required-machine reachability, executable validation recipes, budgets at
most 100, and the fail-closed root boundary.

## Exact commands and results

All commands ran on 2026-07-12 from base revision
`b4a9f9e80f3579c12ae2c4dd14b53440530042ec`. The clone is nonrelease-dirty because it contains
this node's owned outputs and the automation-provided untracked `Formalizations/Lean/.lake`
symlink, which reuses canonical pinned artifacts.

| Working directory | Command | Exit | Result |
|---|---|---:|---|
| repository root | `python3 Stage1_Instances/THM-M-0605/build_obligation_artifacts.py` | 0 | generated 19 obligations, denominator `c6e29bcc...e5b7`, and 90 typed edges |
| repository root | `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | `PASS`; open M4 root and witness package |
| `Formalizations/Lean` | `lake env lean ../../Stage1_Instances/THM-M-0605/ObligationTree.lean` | 0 | conditional composition elaborated; axioms exactly `propext`, `Classical.choice`, `Quot.sound` |
| repository root | `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets passed |
| repository root | `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets and ranks passed |
| repository root | `python3 scripts/stage1_target.py show THM-M-0605` | 0 | rank 643, planned, theorem incomplete |
| repository root | `python3 -m json.tool` on the three generated JSON artifacts | 0 each | valid JSON |
| repository root | prohibited-device `rg` scan of `ObligationTree.lean` | 1 | expected negative: no match |
| repository root | `git diff --check -- Stage1_Instances/THM-M-0605 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

No `lake update`, build, dependency clone/fetch, network operation, or `.lake` mutation was
performed.

## Status boundary

`exoticSevenSphereExists_of_witness` checks only exact terminal composition. Its manifold,
homeomorphism, and non-diffeomorphism inputs remain open. The mathlib `proof_wanted` marker supplies
no proof credit. The first remaining root cut is `M0605-T-WITNESS`. Primary-source H0 review,
substantive bundle/topology/obstruction proofs, provenance/trust closure, R0 review, hermetic replay,
independent validation, and master acceptance remain open. Root debt stays H1/M4/R3 and the theorem
is not complete.
