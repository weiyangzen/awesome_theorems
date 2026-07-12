# Intake validation

Validation date: 2026-07-13 (Asia/Shanghai).
Base revision: `35681bf154be61836528486ed7830f619fc03231`.
Base tree: `b45fc969fef64ad53ac30dc548894b08e8bef834`.

The worker reused the automation-provided canonical `.lake` symlink read-only. No `lake update`,
`lake build`, dependency clone/fetch, package mutation, theorem declaration, or proof was run.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1507` | 0 | rank 1045, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 11008,11013 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded repository and pinned-mathlib exact-term search | 0 | unrelated Kantorovich duality and cone TODO text found; no source-selected general Lagrangian-duality target |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1507/IntakeProbe.lean)` | 0 | five adjacent proper-cone, dual and separation APIs elaborated; output SHA-256 `e972dd85ca6dfa3c76033895c7dc9fa3b4caea7a8164028a76f58d42113fc0c4`; no target declaration checked |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all four JSON documents parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1507-pycache python3 -m py_compile Stage1_Instances/THM-M-1507/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-1507/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/item identity, planned H5/M4/R4 boundary, null target, exact artifact inventory, source hashes, handoff and six open tasks agree |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1507` | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1507 .stage1-worker-selftest.json` plus new-file hygiene checks | 0 | no whitespace, final-newline, CR, NUL, or trailing-space defect |

## Known downstream failures

- No stable mathematical proposition is selected. The complete optimization model, definitions,
  binders, assumptions, conclusion, constraint qualifications, edge cases, primary source and
  independent source review remain open.
- No canonical Lean expression, expression or environment hash, minimal imports, checked alternate
  encoding, or statement mutation certificate exists.
- The API probe establishes only adjacent feasibility. It does not locate or validate a
  source-identical proof and does not upgrade the root from `M4`.
- Anchor audit, obligation registry and typed graphs, proof, composition and trust checks, readable
  reconstruction, hermetic replay, deterministic evidence bundle and independent release
  verification remain open.

These failures block statement and theorem execution but do not invalidate a truthful,
self-tested `planned` intake. Only the integration lane may accept the provisional worker receipt.
