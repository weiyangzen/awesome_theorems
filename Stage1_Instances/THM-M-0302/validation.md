# Intake validation record

## Scope

This record covers only `S56-M-0302-INTAKE`: target membership, a fail-closed `planned` instance,
the theorem dossier, scope map, source-statement crosswalk, six-task open DAG, and a discovery-only
pinned Lean API probe. It is nonrelease evidence from an isolated dirty worker clone. The
automation-provided untracked `Formalizations/Lean/.lake` symlink was used read-only; no
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

The exact-statement gate remains blocked because no primary theorem text or locator was admitted
and the received record omits proposition-changing definitions, constants, binders, and the choice
between exponential-integrability and distribution-tail roots. This downstream blocker does not
prevent a truthful planned intake from being self-tested. The intake receipt is provisional and
awaits master acceptance.

## Environment

- Repository base: `940588d30669014430d5a1beb187f2bca118e816`
- Repository tree: `42d80725ccbabcdd826ed2bc8b3622ac31ac7695`
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
| `python3 scripts/stage1_target.py show THM-M-0302` | 0 | rank 1305, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before edits, only the automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 2167,2172 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| exact Crossref and Semantic Scholar DOI metadata queries recorded in `intake-receipt.json` | 0 | title, authors, 1961, journal, volume, pages, and DOI agree; bibliographic discovery only |
| publisher DOI/PDF access attempt recorded in `intake-receipt.json` | 0 | DOI redirect completed but the final publisher response was a Cloudflare HTTP 403 access challenge; no primary text admitted |
| OpenAlex discovery query recorded in `intake-receipt.json` | 22 | HTTP 429; failure receives no source credit |
| Unpaywall discovery query recorded in `intake-receipt.json` | 0 | matching article metadata, `is_oa=false`, and no OA locations; discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0302/IntakeProbe.lean)` | 0 | ten adjacent APIs elaborated; three axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`; no target statement or proof credit |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1 | expected no-match result for BMO and John-Nirenberg names; not a complete anchor audit |
| `python3 -m json.tool` over owned JSON and the worker packet | 0 | structured artifacts parse as JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0302-pycache python3 -m py_compile Stage1_Instances/THM-M-0302/check_intake.py` | 0 | scoped validator compiles without generated files in the owned path |
| `python3 Stage1_Instances/THM-M-0302/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, pinned inputs, H1/M4/R4 boundary, artifact hashes, provisional handoff, and six open tasks agree |
| prohibited-construct `rg` over the target Lean file | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped tracked and no-index `git diff --check` | 0 | no whitespace diagnostics in changed files |

## Structured recipes

The provisional receipt records two replayable recipes: the owned structural checker and the
narrow pinned Lean probe. Both cover only `S56-M-0302-INTAKE`, no canonical obligation, no target
declaration, and no proof body. Both passed with exit zero. Exact stdout signatures and artifact
hashes are bound in `intake-receipt.json`.

## Result and boundary

The assigned intake is self-tested and proposed as worker state `[_]`; only the integration lane
may accept it. The root moves only from unclassified metadata to provisional `[H1, M4, R4]`. H1
records the strongly identified classical published theorem family, not an admitted exact primary
statement or proof-source crosswalk. Canonical statement and Lean expression, H0, M0, R0,
obligation registry, typed graphs, proof, audit completion, theorem completion, hermetic release,
and independent verification all remain open.
