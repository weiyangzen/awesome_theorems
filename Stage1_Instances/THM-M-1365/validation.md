# Intake validation

Base revision: `10064cd912bf0d94ab6c8d818dd3a30551a921cd`.

This validation covers manifest membership, the fail-closed planned dossier, source-family
discrimination, JSON and scoped invariants, and a narrow pinned Lean API probe. The canonical
`.lake` symlink and dependency artifacts were used read-only. No `lake update`, build, fetch, clone,
or dependency mutation was run. The worker tree is nonrelease evidence because the owned dossier
and the automation-provided `.lake` symlink are untracked.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1365` | 0 | rank 975; planned; L0/rework_required; no accepted legacy artifact; theorem_complete false |
| `git status --short` | 0 | before edits, only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree match the structured intake record |
| `git blame -L 9950,9955 -- Docs/researches/math_theorems.md` and duplicate-record blame | 0 | both uncited six-line records originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| publisher PDF retrieval, `pdfinfo`, and bounded `pdftotext` extraction for Smale 1967 Section 1.5 | 0 | publisher scan SHA-256 `759e0601e50ceebc812c4a4c67e5b9ed59534848c6d342a2e2cf56871db19551`; candidate results (5.1), (5.3), (5.4), and (5.5) are distinct |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned mathlib source is clean |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1365/IntakeProbe.lean)` | 0 | eight generic APIs elaborated; stdout SHA-256 `fee81f942f0db786a0fa927f041ed2ea6b9b62f1404f43f5ff9374b75e665176` |
| `rg -n -i --glob '*.lean' 'Smale.?horse\|horseshoe\|horse.?shoe\|马蹄' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected) | no exact named target hit; bounded intake discovery only |
| `python3 -m json.tool` over `instance.json`, `task-dag.json`, `intake-receipt.json`, and the worker packet | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1365-pycache python3 -m py_compile Stage1_Instances/THM-M-1365/check_intake.py` | 0 | scoped checker compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1365/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, H5/M4/R4 boundary, source hashes, null formal target, exact artifact inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1365/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited-construct scan over the owned Lean file | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 per new file means only that the file is new |
| `git diff --check -- Stage1_Instances/THM-M-1365 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-1365-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source selection and independent review,
canonical Lean elaboration and statement mutations, complete anchor audit and discovery freeze,
obligation registry, typed graphs, proof, composition, trust closure, hermetic replay, deterministic
release bundle, and independent verification remain open. Those failures prevent statement,
audit-completion, and theorem-completion claims but do not invalidate the planned intake.
