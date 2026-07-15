# THM-M-0812 obligation-tree validation

## Scope

This record covers the version-1 obligation registry, the seven typed graph
families, the schema-1.1 dependency-reuse ledger, and the conditional Lean
composition harness for `S56-M-0812-OBLIGATION_TREE`. It does not cover proof,
validation, release, audit completion, or theorem completion.

The frozen registry has 40 root-relevant semantic obligations and 40
substantive local ledgers, each with a budget at most 100. The graph bundle has
204 typed edges across proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs. Thirty-four source-shaped child relations
remain explicitly unverified; the two checked composition certificates only
show how three open proof packages would assemble the exact root.

## Dependency result

The observed v2 graph digest is
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`
and the target context digest is
`bc99f9e70a837e425f01f88835dda207b07138301527ae3715e6640b0998be7d`.
There are no hard parents, transitive ancestors, incoming hard edges, or reuse
hints. Five weak shared-module groups were inspected against actual peer
artifacts; all are `not_applicable`, no result is reused, and no proof or phase
credit transfers.

## Commands

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 1 | expected worker-local inventory blocker: the immutable checked-in v2 DAG differs from a fresh discovery build after adding target-owned Lean/JSON evidence; the worker must not rewrite the authoritative DAG |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | same expected integration-lane regeneration blocker; the supplied graph/context digests remain bound in the dependency ledger |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0812` | 0 | rank 1371, planned, L0/rework-required, theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0812/build_obligation_artifacts.py --check` | 0 | deterministic registry, graphs, validation specs, and readable projection match |
| `python3 -B Stage1_Instances/THM-M-0812/check_obligation_tree.py --worker-packet .stage1-worker-selftest.json` | 0 | 40 obligations, 204 typed edges, 40 ledgers, 34 open decompositions, exact conditional composition, and dependency ledger passed |
| checker-internal pinned `lake env lean` replay of `ObligationTree.lean` with a temporary `Statement.olean` | 0 | three conditional declarations report only `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `858d98fcae39d09792e16eadea6f66c992a2a0ed90c6606d91347cdb2afa5705` |
| JSON parsing, Python AST parsing, comment-aware prohibited-construct scan, per-file text checks, and scoped `git diff --check` | 0 | artifacts are structured and clean; no proof escape or whitespace diagnostic |

The automation-provided untracked `Formalizations/Lean/.lake` symlink was used
read-only. No `lake update`, `lake build`, clone, fetch, dependency checkout, or
`.lake` mutation was performed.

## Boundary

The predecessor anchor audit is provisional `[_]`, so this receipt cannot be
master accepted before dependency-ordered predecessor acceptance. The exact
root remains `H1/M3/R2`. Matching attainment, the alternating-path equal-cover
construction, weak duality, every internal composition not represented by the
two conditional certificates, H0 source review, R0 reconstruction, provenance,
trust, hermetic replay, independent verification, release, and master
acceptance remain open.
