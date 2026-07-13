# Intake validation record

## Scope

This record covers only `S56-M-0254-INTAKE`: target membership, the fail-closed `planned`
instance, theorem dossier, scope map, source-statement crosswalk, six-task open DAG, and a
discovery-only pinned Lean API probe. It is nonrelease evidence from an isolated dirty worker
clone. The automation-provided untracked `Formalizations/Lean/.lake` symlink was used read-only;
no `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

The exact-statement gate remains blocked because the catalog does not select a truth-valued BMO
characterization and because the John-Nirenberg reading overlaps separately scheduled
`THM-M-0302`. That expected downstream blocker does not prevent a truthful planned intake from
being self-tested. The intake receipt is provisional and awaits master acceptance.

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
| `python3 scripts/stage1_target.py show THM-M-0254` | 0 | rank 1264, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before edits, only the automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 1829,1834 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1829,1834p' Docs/researches/math_theorems.md \| sha256sum` | 0 | catalog block SHA-256 `468bfdeff1d53fbe365091a8b9898eaad036a546b7fe117d3791713130c50394` |
| exact Crossref DOI metadata query recorded in `intake-receipt.json` | 0 | confirmed John/Nirenberg, title, 1961, journal 14(3), pages 415-426, and DOI; bibliographic discovery only, no primary theorem accepted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0254/IntakeProbe.lean)` | 0 | six generic set-average and Euclidean box-volume APIs elaborated; three adjacent axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`; no target statement or proof credit |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1 | expected no-match result for bounded-mean-oscillation and John-Nirenberg terms; not a complete anchor audit |
| `python3 -m json.tool` over owned JSON and the worker packet | 0 | all structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0254-pycache python3 -m py_compile Stage1_Instances/THM-M-0254/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 Stage1_Instances/THM-M-0254/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, pinned inputs, null target boundary, artifact hashes, provisional handoff, and six open tasks agree |
| prohibited-construct `rg` over target Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped tracked and no-index `git diff --check` | 0 | no whitespace diagnostics in changed files |

An initial run of the API probe failed because two box-volume declarations were referenced without
their `Real` namespace. The probe was corrected to `Real.volume_Icc_pi` and
`Real.volume_pi_Ioo`, then the exact recorded structured recipe passed. The failed exploratory run
receives no validation credit and is retained in `intake-receipt.json` as truthful command history.

## Structured recipes

The provisional receipt records two replayable recipes: the owned structural checker and the
narrow pinned Lean probe. Both cover only `S56-M-0254-INTAKE`, no canonical obligation, no theorem
declaration, and no proof body. Both passed with exit zero. Exact stdout signatures and artifact
hashes are bound in `intake-receipt.json`.

## Result and boundary

The assigned intake is self-tested and proposed as worker state `[_]`; only the integration lane
may accept it. The root moves only from unclassified intake metadata to the provisional vector
`[H5, M4, R4]`. Here `H5` classifies the received gloss as not a stable proposition and requiring
a master target decision; it does not classify the actual BMO mathematics as false or open. The
first theorem gate remains exact source-statement identity and reconciliation with `THM-M-0302`.
Canonical statement and Lean expression, H0, M0, R0, obligation registry, typed graphs, proof,
audit completion, theorem completion, hermetic release, and independent verification all remain
open.
