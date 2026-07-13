# Intake validation

Validation date: 2026-07-13 (Asia/Shanghai).
Base revision: `04d551db74b7e1d7d9d261bba4727b3daf8a70d5`.
Base tree: `ee8a3d7a6c48598ca61028d71e21e0802ed968e1`.

This evidence covers a fail-closed planned dossier, source and substitution boundaries, the open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical LP proposition or proof because none is supplied by the catalog. The worker reused the
automation-provided canonical `.lake` symlink read-only. No `lake update`, `lake build`, dependency
clone or fetch, package mutation, theorem declaration, or proof was run. The dirty worker run is
nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; the package source was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1492` | 0 | rank 1169, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the pre-existing automation symlink `Formalizations/Lean/.lake` existed; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 10903,10908 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded repository and pinned-mathlib search for linear programming, simplex, Farkas, and duality | 0 | cone TODO text and a meta linarith simplex certificate oracle found; no source-selected target declaration found |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes recorded above |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1492/IntakeProbe.lean)` | 0 | seven adjacent proper-cone, separation, and meta simplex-certificate APIs elaborated; stdout SHA-256 `afe16cb8bf7b69ccfe66c78b007bd89c06b10c712cd8ddadbfb1417678387133`; no target declaration checked |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all four JSON documents parse after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1492-pycache python3 -m py_compile Stage1_Instances/THM-M-1492/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-1492/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and DAG identity, exact source excerpts and hashes, planned H5/M4/R4 boundary, null target, artifact inventory, handoff, and six open tasks agree |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1492` | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1492 .stage1-worker-selftest.json` plus per-new-file no-index checks | 0 | no whitespace, final-newline, CR, NUL, or trailing-space defect |

## Known downstream failures

- No stable truth-valued proposition is selected. The complete LP model, definitions, binders,
  hypotheses, conclusion, primary source, corrections or errata, and independent review remain
  open.
- No canonical Lean expression, expression or environment hash, minimal imports, checked alternate
  encoding, or statement mutation certificate exists.
- The API probe establishes only adjacent feasibility. Its meta simplex definitions are not a
  kernel theorem and do not upgrade the root from `M4`.
- Anchor audit, obligation registry and typed graphs, proof, composition and trust checks, readable
  reconstruction, hermetic replay, deterministic evidence bundle, and independent release
  verification remain open.

These failures block statement and ordinary theorem execution but do not invalidate a truthful,
self-tested `planned` intake. After the final artifact edits, the recorded structure, Lean probe,
JSON, Python, prohibited-construct, and hygiene checks were rerun on 2026-07-13 at 14:39
(Asia/Shanghai) and passed with the results above. Only the integration lane may accept the
provisional worker receipt.
