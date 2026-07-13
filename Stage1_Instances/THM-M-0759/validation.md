# Intake validation record

## Scope

This record covers only `S56-M-0759-INTAKE`: target membership, the fail-closed `planned` instance,
the theorem dossier, scope map, source-statement crosswalk, six-task open DAG, and a discovery-only
pinned Lean API probe. It is nonrelease evidence from an isolated dirty worker clone. The
automation-provided untracked `Formalizations/Lean/.lake` symlink was used read-only; no `lake
update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

The exact-statement gate remains blocked because "the theory of finite automata" is a subject, not
a binder-complete proposition. That expected downstream blocker does not prevent a truthful
planned intake from being self-tested. The intake receipt is provisional and awaits master
acceptance. Because the provisional root is `H5`, ordinary proof execution is also blocked until
the integration lane approves a redirection to one exact theorem, splits the topic, or rejects it.

## Environment

- Repository base: `d05520867fab3367a9b61b9544c3e12241204f54`
- Repository tree: `fb2cfc62077d5b53e9938632cd6361dd60872067`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- Mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- Mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, x86_64
- Validation date: 2026-07-13, Asia/Shanghai

## Commands and results

All commands ran from the repository root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0759` | 0 | rank 1345, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 5591,5596 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| exact line-range hashes for the catalog, Stage0 record, and computer-science survey | 0 | hashes are frozen in `instance.json` and checked by `check_intake.py` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0759/IntakeProbe.lean)` | 0 | 20 adjacent language, DFA/NFA/epsilon-NFA, regularity, pumping, regular-expression, and Myhill-Nerode interfaces elaborated; no target theorem or proof body declared |
| bounded automata-topic `rg` over repo-local Lean and pinned mathlib | 0 | exact-topic occurrences were pinned mathlib API/documentation; no target-specific repo-local automata artifact was found; discovery only |
| `python3 -m json.tool` over owned JSON and the worker packet | 0 | all structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0759-pycache python3 -m py_compile Stage1_Instances/THM-M-0759/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0759/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, pinned inputs, null target boundary, artifact hashes, provisional handoff, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0759/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| prohibited-construct `rg` over target Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped tracked and per-file no-index `git diff --check` | 0 | no whitespace diagnostics in changed files |

## Structured recipes

The provisional receipt records two replayable recipes: the owned structural checker and the
narrow pinned Lean probe. Both cover only `S56-M-0759-INTAKE`, no canonical obligation, no target
declaration, and no proof body. Both passed with exit zero. Exact output and input hashes are bound
in `intake-receipt.json`.

## Result and boundary

The assigned intake is self-tested and proposed as worker state `[_]`; only the integration lane
may accept it. The root moves only from unclassified metadata to the provisional vector
`[H5, M4, R4]`. `H5` applies to the catalog wording, not to finite-automata mathematics. The first
theorem gate remains exact source-statement identity and theorem selection. Canonical statement
and Lean expression, H0, M0, R0, obligation registry, typed graphs, proof, audit completion,
theorem completion, hermetic release, and independent verification all remain open.
