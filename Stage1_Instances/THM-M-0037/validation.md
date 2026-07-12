# Intake validation record

## Boundary

This record validates only the `planned` intake for `S56-M-0037-INTAKE`. The worker clone started
at revision `dc2eb1390c8f2a88e7afcbdbd35f92ab43f64fb8` with the scheduler-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned dependency artifacts. The symlink and
its dependency repositories were used read-only; no Lake update, build, fetch, or clone command
was run.

The Lean probe declares no theorem. It authenticates candidate definition and relation APIs only.
It does not elaborate a canonical target, prove the catalogue claim, or transfer any state from
`THM-M-0424`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0037` | 0 | rank 1080; planned; no legacy slot; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | initial status contained only the scheduler-provided untracked `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base commit `dc2eb1390c8f2a88e7afcbdbd35f92ab43f64fb8`; tree `25138aaafcff80ee47bf04805bccd804978e6754` |
| `git blame -L 284,289 -- Docs/researches/math_theorems.md` | 0 | all six catalogue lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 https://api.crossref.org/works/10.1007%2Fbf01187754` | 0 | bibliographic metadata only: Brauer, 1929, pages 79-107, DOI `10.1007/BF01187754`; no article text inspected |
| `curl -L --fail --silent --show-error --max-time 30 https://api.crossref.org/works/10.1515%2Fcrll.1932.167.399` | 0 | bibliographic metadata only: Brauer/Noether/Hasse, 1932, pages 399-404; no article text inspected |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned mathlib worktree clean |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `cd Formalizations/Lean && lake --version` | 0 | Lake 5.0.0-src+98dc76e |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0037/IntakeProbe.lean` | 0 | eight candidate APIs elaborated; `trans` and `is_eqv` report `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `57765ffdef12498d89b2a499069afcbb2d172f8947effad3632c9a72f4f14f93` |
| `python3 -m json.tool Stage1_Instances/THM-M-0037/instance.json` | 0 | structured instance is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0037/task-dag.json` | 0 | open downstream task DAG is valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0037-pycache python3 -m py_compile Stage1_Instances/THM-M-0037/check_intake.py` | 0 | scoped checker compiles without writing cache files into the repository |
| `python3 -B Stage1_Instances/THM-M-0037/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned null-target boundary, source/pin hashes, owned files, receipt, packet, recipes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0037/check_intake.py` | 0 | public replay mode passes without requiring the scheduler-only worker packet |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0037 -g '*.lean'` | 1 | expected no-match exit; no prohibited proof construct or declaration in the discovery-only probe |
| `for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0037/*; do git diff --no-index --check /dev/null "$f"; test $? -le 1; done` | 0 | every untracked owned file and the worker packet pass whitespace checks |
| `git diff --check -- Stage1_Instances/THM-M-0037 .stage1-worker-selftest.json` | 0 | no tracked diff diagnostics; per-file no-index checks cover untracked artifacts |

## Result

The planned intake is self-tested and proposes only worker state `[_]`. The first downstream
failure is the exact statement gate: no independently reviewed pinpoint source proposition or
checked source-to-Lean identity/transport selects among the materially different classification
readings. All six downstream tasks remain open, and no theorem-completion claim is made.
