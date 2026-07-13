# Intake validation

Validation date: 2026-07-13 (Asia/Shanghai).
Base revision: `04d551db74b7e1d7d9d261bba4727b3daf8a70d5`.
Base tree: `ee8a3d7a6c48598ca61028d71e21e0802ed968e1`.

The worker reused the automation-provided canonical `.lake` symlink read-only. No `lake update`,
`lake build`, dependency clone or fetch, package mutation, theorem declaration, or proof was run.
The dirty worker snapshot is nonrelease evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1490` | 0 | rank 1167; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 10889,10894 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `rg -n -i --glob '*.lean' 'optimization[ _-]*theory\|mathematical[ _-]*optimization\|优化理论\|数学优化' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match for the exact broad topic phrases; generic minimizer APIs and foreign `THM-M-1270` wrappers were separately inspected |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned package worktree remained clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1490/IntakeProbe.lean` | 0 | six distinct minimizer/convexity APIs elaborated; three theorem probes each report `[propext, Classical.choice, Quot.sound]`; stdout+stderr SHA-256 `c2753a35cefe4d2af1f85ee062d1a98b3d1d1d60ead60ceec169cfbb698f2a3d`; no canonical target or proof body declared |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all JSON documents parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1490-pycache python3 -m py_compile Stage1_Instances/THM-M-1490/check_intake.py` | 0 | scoped validator compiled without adding generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1490/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, planned H5/M4/R4 boundary, null target, source and owned-artifact hashes, exact recipe output, handoff, ownership delta, and six open tasks agree |
| `rg -n --glob '*.lean' 'sorry\|admit\|sorryAx\|(^\|[^A-Za-z])(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1490/IntakeProbe.lean` | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1490 .stage1-worker-selftest.json` plus new-file hygiene checks | 0 | no whitespace, final-newline, CR, NUL, or trailing-space defect |

## Known downstream failures

- No stable mathematical proposition is selected. Claim family, objective, domain, constraints,
  solution notion, assumptions, algorithm, binders, conclusion, primary source, proof boundary,
  corrections, boundary cases, and independent reviews remain open.
- No canonical Lean expression, expression or environment fingerprint, minimal imports, checked
  alternate encoding, or statement mutation certificate exists.
- The API probe establishes adjacent pinned substrate only. It neither identifies a source-exact
  root nor upgrades the machine vector from `M4`.
- Complete formal anchor and proof-body audit, obligation registry, typed graphs, proof, composition,
  trust closure, readable reconstruction, hermetic replay, deterministic bundle, independent
  verification, release, and master acceptance remain open.

These failures block statement and theorem execution but do not invalidate a truthful, self-tested
`planned` intake. Only the integration lane may accept the provisional worker receipt.
