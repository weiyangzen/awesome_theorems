# Intake validation

Base revision: `ffe94ac84965dc19f4923f88b7566072ddee37ae` (tree
`876a17f277d84dcf06ca672e5cd351edaa294495`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source
provenance, pinned environment identity, a narrow Lean API probe, bounded local name search,
proof-escape hygiene, and whitespace. The repository record is not a proposition, so elaborating a
purported canonical target would invent missing mathematics. `IntakeProbe.lean` therefore checks
only possible encoding substrate; it introduces no theorem and supplies no statement or proof
credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1430` | 0 | rank 928, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git rev-parse HEAD`, `git rev-parse HEAD^{tree}`, and `git status --short` | 0 | base and tree match this record; preflight had only `?? Formalizations/Lean/.lake` |
| `git blame -L 10446,10451 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref DOI metadata query for the 1980 Mandelbrot paper | 0 | author, year, journal, volume, issue, pages, and DOI confirmed as bibliographic discovery only |
| Publisher PDF retrieval for DOI `10.1111/j.1749-6632.1980.tb29690.x` | 22 | HTTP 403; exact source passage, assumptions, and proof were not inspected or credited |
| `python3 -m json.tool Stage1_Instances/THM-M-1430/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1430/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1430/intake-receipt.json` | 0 | valid JSON after finalization |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON after finalization |
| `python3 Stage1_Instances/THM-M-1430/check_intake.py` | 0 | target identity, H5/M4/R4 planned boundary, null target, empty accepted state, artifact hashes, and six open tasks agree |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1430-pycache python3 -m py_compile Stage1_Instances/THM-M-1430/check_intake.py` | 0 | scoped intake validator compiles without generated files in the owned path |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| first `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1430/IntakeProbe.lean)` | 1 | three check names were unavailable (`Complex.instNorm`, `Function.iterate`, unimported `norm`); the probe was corrected to checked expressions and an explicit norm import before evidence was recorded |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1430/IntakeProbe.lean)` | 0 | nine adjacent pinned complex-number, quadratic-map, iteration, range, norm, and bounded-set API expressions elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` and package status | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; package status clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| bounded `Mandelbrot` / complex-dynamics / quadratic-parameter-space search under pinned mathlib | 1 | expected target-name no-match; unrelated algebraic uses of "quadratic polynomial" were ignored; intake discovery only, not an anchor audit |
| immutable raw-source inspection of `girving/ray@0ca7b1e746b2911557ac76f56259068cfd1423ab` | 0 | found a remote Mandelbrot definition and connectedness theorems under Lean v4.27.0-rc1/mathlib `725c803...`; recorded as an unintegrated future audit candidate only |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, or `opaque` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1430 .stage1-worker-selftest.json` plus owned-file invariants | 0 | no whitespace diagnostics; the scoped validator checks every untracked owned file |

Known downstream failures remain deliberately open: an approved target correction or redirection;
an immutable primary-source theorem, exact passage, assumptions, errata audit, and independent
review; quadratic-family, parameter, critical-orbit, boundedness, binder, conclusion, and boundary
choices; canonical Lean elaboration, expression/environment fingerprints, checked transports, and
statement mutations; immutable formal-anchor audit; discovery and obligation freezes; proof and
composition; hermetic replay; deterministic evidence bundling; independent release verification;
and master acceptance. These block ordinary theorem execution and completion but do not invalidate
a truthful, self-tested `planned` intake.
