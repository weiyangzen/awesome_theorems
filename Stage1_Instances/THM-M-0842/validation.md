# Intake validation

Validation was run on 2026-07-13 in the isolated scheduler worker clone at base revision
`444860f481e8bbf64a3357008fd4d01a52006f08`. The initial worktree had only the
automation-provided untracked `Formalizations/Lean/.lake` symlink; it points to the canonical
pinned artifacts and was used read-only. This is nonrelease worker evidence, not a clean or
hermetic release run.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0 / rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0842` | exit 0; rank 1399, planned lifecycle, no legacy slot, legacy artifacts unaccepted, theorem completion false |
| `git status --short --untracked-files=all` | exit 0; initially only `Formalizations/Lean/.lake`; preserved without mutation |
| `git blame -L 6180,6185 -- Docs/researches/math_theorems.md` | exit 0; all six catalog lines trace to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| author index and scan retrieval from the URLs in `instance.json` | exit 0 in the source-audit run; index: 30,459 bytes and SHA-256 `4c81a5de...0fd7`; scan: 15,346,005 bytes, 41 pages, SHA-256 `5d2046b0...f72f` |
| bounded `rg` for Simonovits / stability / edit-distance declarations in pinned mathlib and repo-local Lean | completed; no target-level declaration located; adjacent Turán, coloring, extremal-number, and deletion APIs only |
| bounded public Lean discovery over a current external archive and local mathlib history | completed; located Erdős-Stone asymptotic/minimum-degree work, not the requested structural stability theorem; discovery only |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0842/IntakeProbe.lean` | exit 0; nine adjacent pinned graph interfaces elaborated; no target theorem or proof body declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0842-pycache python3 -m py_compile Stage1_Instances/THM-M-0842/check_intake.py` | exit 0; scoped validator compiled without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-0842/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; authority identity, source and dependency hashes, null canonical target, `H1/M4/R4` boundary, artifact hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0842/check_intake.py` | exit 0; public replay mode passed without depending on the scheduler packet |
| prohibited-construct scan over `IntakeProbe.lean` | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped newline/trailing-whitespace checks and `git diff --check --no-index /dev/null` for each new file | exit 0; no whitespace errors |

The first Lean probe attempted the same file before its explicit `Coloring` import was added and
failed only on unknown identifier `SimpleGraph.Colorable`; the corrected narrow probe above then
exited 0. No `.lake` dependency or cache source was updated, fetched, or built.

## Validated boundary

The self-test validates a `planned` dossier, source-family discrimination, scope map,
source-statement crosswalk, pinned adjacent-API probe, and open downstream task DAG. It does not
validate a canonical proposition, a proof, or a terminal assurance decision.

## Known open gates

Variant selection, exact primary-source statement and dependency mapping, corrections and errata,
independent source review, ordered Lean binders, minimal imports, expression and environment
fingerprints, checked transports, structural mutations, exhaustive formal-candidate discovery,
obligation and discovery hashes, typed graphs, proof bodies, composition, axioms and provenance,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion all remain open. These gates truthfully remain
downstream of a self-tested planned intake.
