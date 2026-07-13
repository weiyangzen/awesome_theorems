# Intake validation record

## Scope and verdict

This record covers only `S56-M-0258-INTAKE`: the planned dossier, scope map,
source-statement crosswalk, identity-conflict boundary, generic pinned Lean API probe, and six open
downstream tasks. It does not validate a canonical theorem statement or proof.

Worker self-test verdict: `pass`, proposed scheduler state `[_]`, pending integration-lane master
acceptance. Lifecycle remains `planned`; root vector is provisionally `[H5, M4, R4]`; audit and
theorem completion are false.

## Input boundary

- Repository base: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
  `5a80b61d8fa09336779f8d1453dcfe4299c9472f`).
- Pinned toolchain: Lean `4.29.0` at `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`).
- The pre-existing untracked `Formalizations/Lean/.lake` symlink was reused read-only. No update,
  build, dependency clone, fetch, pull, or other `.lake` mutation was run.
- The worker input is nonrelease-dirty because of that pre-existing automation symlink and the new
  owned artifacts. No clean-room, hermetic, offline-replay, or independent-runner claim is made.

## Commands and exact results

All commands ran from the repository root unless a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0258` | 0 | rank 1266; planned; L0/rework; no legacy slot; legacy artifacts unaccepted; theorem completion false |
| `git status --short --untracked-files=all` (initial) | 0 | only pre-existing `?? Formalizations/Lean/.lake` |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree recorded above |
| `git blame -L 1857,1862 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `rg -n -i --glob '*.lean' 'Denjoy[ _-]*Wolff\|Wolff[ _-]*Denjoy\|Teichm[uü]ller[ _-]*(space\|boundary\|compactification)\|Thurston[ _-]*(boundary\|compactification)\|Gardiner[ _-]*Masur' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 | expected no-match result; no exact-topic occurrence in this bounded search |
| `lake env lean ../../Stage1_Instances/THM-M-0258/IntakeProbe.lean` (`cwd=Formalizations/Lean`) | 0 | eight generic APIs elaborated; complete stdout SHA-256 `5ec5d2e656509f2115e3991d380ccc17d8743575569c2c442f2a913af9c2d7e4` |
| `python3 -B Stage1_Instances/THM-M-0258/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | `intake invariant check: ok (THM-M-0258 planned; H5/M4/R4; six open tasks)` |
| `rg -n -i 'sorry\|admit\|sorryax\|axiom\|constant\|opaque\|unsafe' Stage1_Instances/THM-M-0258 --glob '*.lean'` | 1 | expected no-match result; no proof escape declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0258 .stage1-worker-selftest.json` plus per-file `git diff --no-index --check /dev/null <file>` checks | 0 | no whitespace diagnostics; no-index exit 1 was accepted only for the expected new-file differences |

The bounded name search is discovery evidence, not an exhaustive external anchor audit or global
absence claim. The Lean command checks API availability only. It neither elaborates a canonical
target nor reaches a proof body.

## Structured recipes

The provisional receipt records two replayable recipes with explicit `cwd`, argv array, empty
environment allowlist, 120-second timeout, denied network, expected exit 0, exact output policy,
covered node `S56-M-0258-INTAKE`, and covered declarations. Recipe and input-manifest hashes exclude
the self-referential receipt and root packet. The integration lane must recapture content-addressed
logs and inputs before acceptance.

## Known failures

The title, attribution, year, and gloss do not select one stable proposition. There is no accepted
source edition or theorem locator, exact Lean target, checked transport, statement mutation,
anchor audit, obligation registry, typed graph, proof, composition certificate, trust closure,
readable reconstruction, hermetic replay, deterministic evidence bundle, independent verification,
release decision, or master acceptance. These are truthful downstream blockers, not failures of
the intake self-test.
