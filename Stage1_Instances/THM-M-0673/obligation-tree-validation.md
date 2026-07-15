# THM-M-0673 obligation-tree validation

Item: `S56-M-0673-OBLIGATION_TREE`. Base revision:
`f3b9f5fc99b4675558801fcc47f610b046eb5d14` (tree
`5a074129aa628a1d735fc06a68164a056f1d62be`).

## Frozen result

Registry version 1 contains 28 unique semantic obligations. Its canonical denominator SHA-256 is
`4266ee40d8be778685c48d8781aab55dd6d57301e7d9ded13523ea4353c58fe6`; the pre-status registry
scope SHA-256 is `aefa3236248ea7500e3dd48e01e953f978f8425c78ac11103364ce9cabce3e77`.
Seven separate typed graph families contain 124 directed edges. Every machine-required obligation
is reachable from the root through acyclic `proof_requires` edges, and each such edge has a reverse
`composes` edge.

The checker obtains the pinned Lean binary and `LEAN_PATH` through `lake env`, compiles
`Statement.lean` to a temporary `Statement.olean`, and elaborates `ObligationTree.lean` with
`--trust=0`. The temporary directory is removed automatically. No repository or dependency build
artifact is written, and `.lake` is not updated. The checked route consumes an explicit
`BoundedFormulaRealizePackage`; it never invokes the audited mathlib proof and therefore supplies
conditional composition evidence only.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 -B Stage1_Instances/THM-M-0673/build_obligation_artifacts.py` | 0 | deterministically wrote 28 obligations, 124 typed edges, and 28 structured node recipes; denominator and registry hashes above |
| `LC_ALL=C LANG=C NO_COLOR=1 python3 -B Stage1_Instances/THM-M-0673/check_obligation_tree.py` | 0 | source hashes, schemas, denominators, ledgers, all seven graphs, reciprocity, cycles, root reachability, receipt linkage, prohibited-token scan, and temporary scoped Lean elaboration passed; stdout SHA-256 `b0fce724...cfc8` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure and 1546-target standard passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered rework-required targets passed |
| `python3 scripts/stage1_target.py show THM-M-0673` | 0 | rank 717, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0673/{obligation-registry,typed-graphs,validation-specs,obligation-tree-receipt}.json` | 0 | all four structured artifacts parsed |
| `python3 -m py_compile Stage1_Instances/THM-M-0673/{build_obligation_artifacts,check_obligation_tree}.py` with `PYTHONPYCACHEPREFIX=/tmp/...` | 0 | both validators compiled outside the repository |
| deterministic builder rerun plus byte comparison in `/tmp` | 0 | all three generated JSON files were byte-identical |
| `git diff --check -- Stage1_Instances/THM-M-0673 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The scoped Lean output names all four checked compositions and the combined conditional route.
`assert_no_sorry` passes; no `sorryAx` appears. The local composition axioms are within the already
reported candidate profile (`propext`, `Classical.choice`, `Quot.sound`). Neither this profile nor
the transitive TCB is release-accepted at this phase.

## Status boundary

This phase is self-tested pending dependency-ordered master acceptance. The exact pinned theorem
remains an uninstalled `M0-W` candidate, accepted closed obligations remain empty, and the root
stays `[H1, M3, R4]`. Primary-source H0, proof-phase integration and all remaining composition
certificates, provenance and trust closure, independently reviewed R0, hermetic and independent
validation, release, AUDIT-Z, and theorem completion remain open.
