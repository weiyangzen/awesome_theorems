# Intake validation record

## Boundary

This record validates only the `planned` intake for `S56-M-0038-INTAKE`. The worker clone started
at revision `d66b6e80968b53d5b99774584721ae8976f303a5` with the scheduler-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned dependency artifacts. The symlink and
dependency repositories were used read-only; no Lake update, build, fetch, or clone command was
run.

The Lean probe declares no theorem. It authenticates adjacent central-simple-algebra quotient APIs
only. It does not define index or degree, select their relation, elaborate a canonical target, or
transfer state from a sibling target.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0038` | 0 | rank 1516; planned; no legacy slot; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | initial status contained only the scheduler-provided untracked `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base commit `d66b6e80968b53d5b99774584721ae8976f303a5`; tree `aaa82721074fccea81033a9a18d21652af89f8e4` |
| `git blame -L 291,296 -- Docs/researches/math_theorems.md` | 0 | all six catalogue lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref exact-name/bibliographic queries and Bing exact-phrase RSS queries | 0 | no matching `Sigmund Morill` algebraist, theorem, or 1937 source identified; negative mutable discovery only |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned mathlib worktree clean |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `cd Formalizations/Lean && lake --version` | 0 | Lake 5.0.0-src+98dc76e |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0038/IntakeProbe.lean` | 0 | four substrate APIs elaborated; `is_eqv` reports `[propext, Classical.choice, Quot.sound]`; output SHA-256 `fbd3c35a...2d055` |
| bounded declaration search for `index`, `degree`, or `exponent` under pinned `Mathlib/Algebra/BrauerGroup` and `Mathlib/Algebra/Central` | 1 | expected no-match exit; no such declaration in this bounded surface |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0038-pycache python3 -m py_compile Stage1_Instances/THM-M-0038/check_intake.py` | 0 | checker compiles without repository cache output |
| `python3 -B Stage1_Instances/THM-M-0038/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, null-target boundary, source/pin hashes, owned files, receipt, packet, recipes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0038/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| `rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]' Stage1_Instances/THM-M-0038 -g '*.lean'` | 1 | expected no-match exit; no prohibited proof construct or declaration |
| per-file `git diff --no-index --check /dev/null <path>` for every owned artifact and packet | 0 | all untracked deliverables pass whitespace checks |
| `git diff --check -- Stage1_Instances/THM-M-0038 .stage1-worker-selftest.json` | 0 | no tracked diff diagnostics; per-file no-index checks cover untracked artifacts |

## Result

The planned intake is self-tested and proposes only worker state `[_]`. Its first downstream
failure is exact source-statement identity: no independently reviewed source resolves the author,
defines index and degree, or states the relation between them. All six downstream tasks remain
open, and no theorem-completion claim is made.
