# Intake validation record

## Scope

This record covers only `S56-M-0259-INTAKE`: target membership, the fail-closed `planned` instance,
the theorem dossier, scope map, source-statement crosswalk, duplicate boundary, six-task open DAG,
and a discovery-only pinned Lean API probe. It is nonrelease evidence from an isolated dirty worker
clone. The automation-provided untracked `Formalizations/Lean/.lake` symlink was used read-only; no
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

The exact-statement gate remains blocked because the catalog gives an author, year, and Julia-set
topic rather than a proposition. That expected downstream blocker does not prevent a truthful
planned intake from being self-tested. The intake receipt is provisional and awaits master
acceptance.

## Environment

- Repository base: `c6fd6dad8fcfe5fd464416cd452f50286b546978`
- Repository tree: `5a80b61d8fa09336779f8d1453dcfe4299c9472f`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- Mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- Mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux x86_64
- Validation date: 2026-07-13, Asia/Shanghai

## Commands and results

All commands ran from the repository root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0259` | 0 | rank 1267, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before edits, only the automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 1864,1869 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| catalog and Stage0 excerpt hashing | 0 | target record SHA-256 `36bc5c121bf3001673009403df38784fb57efce7031f7439fe13a46f3602b2d8`; duplicate record `589d866392f6fd515e0f428dbb6741fa70b5dba112668c15cd8eb6c66cf372ee`; target Stage0 block `a57b061620d0d01d0eaca973ccf7076cb48c8247795d237b465ade0946434359` |
| inspection of arXiv `math/9410221v1` already present in temporary storage | 0 | 199514-byte, 17-page PDF SHA-256 `e8f777c2bda3133b0b30241702d447410826a892d507e12d8d68c9042d0a0b81`; Theorem 5.2 is ambiguity evidence only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0259/IntakeProbe.lean)` | 0 | ten adjacent complex, one-point, meromorphic, iteration, periodic-point, closure, and frontier APIs elaborated; stdout SHA-256 `add9f3853a3cdd29a2710ef63f22e5f0479ac804f4d479027135b11b1b9ec55c`; no target declaration |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1 | expected no-match for McMullen, Julia-set, Mandelbrot, complex/rational dynamics, and Lattes terms; intake discovery only |
| inspection of `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_259.lean` | 0 | file header identifies `THM-M-0504` and Riemann-hypothesis consequences; numeric filename is unrelated to this target |
| `python3 -m json.tool` over owned JSON and the worker packet | 0 | instance, open task DAG, provisional receipt, and worker handoff parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0259-pycache python3 -m py_compile Stage1_Instances/THM-M-0259/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 Stage1_Instances/THM-M-0259/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, pinned inputs, H5/M4/R4 null-target boundary, duplicate freeze, artifact hashes, handoff, and six open tasks agree |
| prohibited-construct `rg` over target Lean files | 1 | expected no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped tracked and no-index `git diff --check` | 0 | no whitespace diagnostics in changed files |

## Structured recipes

The provisional receipt records two replayable network-denied recipes: the owned structural checker
and the narrow pinned Lean probe. Both cover only `S56-M-0259-INTAKE`, no canonical obligation,
theorem declaration, or proof body. Their exact stdout and artifact hashes are bound in
`intake-receipt.json`.

## Result and boundary

The assigned intake is self-tested and proposed as worker state `[_]`; only the integration lane
may accept it. The root moves only from unclassified inventory metadata to the provisional vector
`[H5, M4, R4]`. The first theorem gate remains exact source-statement identity and authoritative
duplicate resolution. Canonical statement and Lean expression, H0, M0, R0, obligation registry,
typed graphs, proof, audit completion, theorem completion, hermetic release, and independent
verification all remain open.
