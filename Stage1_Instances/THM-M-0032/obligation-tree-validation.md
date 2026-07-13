# THM-M-0032 obligation-tree validation

Item: `S56-M-0032-OBLIGATION_TREE`

Base revision: `540472523b6c0717ed925193071191f81f62d6eb`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 38 obligations and 83 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. The denominator
SHA-256 is `7ddbec795ccfc7f42c1efc171aee6f2e8d1a82af6f5bb5d2382c926d64d451c7`.

The proof graph selects Kaplansky's criterion and expands its theorem-specific prime-element
premise through a minimal prime over a principal ideal, height-one principality, dimension
induction, localization, invertible-ideal trivialization, and primality lifting. It explicitly
rejects the invalid higher-dimensional shortcut that every nonzero prime ideal is principal.

The checked Lean harness consumes the regular-local domain, prime-element, and generic Kaplansky
packages to return the actual frozen target. The first two remain explicit premises. Therefore no
obligation is accepted closed, and the root remains `H1/M3/R4`, `audit_complete=false`, and
`theorem_complete=false`.

## Commands and results

Commands ran inside this worker clone. The automation-provided canonical `.lake` symlink was used
read-only. No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation ran.
Temporary Lean module output and Python bytecode were confined to `/tmp` and removed after checks.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0032` | 0 | rank 1076; planned; L0/rework-required; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0032/build_obligation_artifacts.py` | 0 | wrote 38 obligations, 83 typed edges, and denominator `7ddbec79...451c7` |
| `python3 -B Stage1_Instances/THM-M-0032/check_obligation_tree.py` | 0 | deterministic registry, instance hash, exclusions, node schemas, seven typed graphs, reciprocal proof edges, root reachability, recipes, source pins, receipt, worker packet, and open closure passed |
| from `Formalizations/Lean`, `lake env lean --root=../.. ../../Stage1_Instances/THM-M-0032/Statement.lean -o /tmp/stage1-thm-m-0032-obligation-lean/Statement.olean`, then elaborate `ObligationTree.lean` with that temporary directory prepended to the pinned Lake `LEAN_PATH` | 0 | exact statement and conditional compositions elaborated; only `propext`, `Classical.choice`, and `Quot.sound`; obligation stdout SHA-256 `fc1829fe...5e12` |
| `python3 -m json.tool` on registry, graph bundle, validation specs, receipt, and root worker packet | 0 | all structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0032-obligation-pycache python3 -m py_compile Stage1_Instances/THM-M-0032/build_obligation_artifacts.py Stage1_Instances/THM-M-0032/check_obligation_tree.py` | 0 | generator and validator compiled outside the repository tree |
| scoped scan for `sorry`, `admit`, `sorryAx`, bodyless axioms, unsafe/opaque bodies, external/native shortcuts, TODO, and FIXME in `ObligationTree.lean` | 1 (expected no match) | no prohibited proof escape or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0032 .stage1-worker-selftest.json` plus no-index checks for new files | 0 | no whitespace diagnostics |

## Status boundary

This is provisional warm worker evidence pending dependency-ordered master acceptance. The domain
and prime-element packages are open; the generic Kaplansky wrapper and conditional composition do
not prove them. Primary-source H0, independently reviewed R0, transitive provenance and trust,
hermetic replay, independent validation, deterministic release evidence, `AUDIT-Z`, validation,
release, and theorem completion remain open.
