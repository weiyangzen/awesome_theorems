# Intake validation

Validation date: 2026-07-13 (Asia/Shanghai).
Base revision: `d1b510bacab792f84a99231485cf4429fdb78978`.
Base tree: `f77c4e4db196fc0ecc271815514a411d06ea6053`.

The worker reused the automation-provided canonical `.lake` symlink read-only. No `lake update`,
`lake build`, dependency clone/fetch, package mutation, theorem declaration, or proof was run. The
preflight worktree contained only that symlink, so this is dirty nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0632` | 0 | rank 1325, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 4685,4690 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| scoped catalog, Stage0, manifest, DAG, blueprint, skill, guideline, neighbor, and pinned-mathlib inspection | 0 | received wording is a topic family; multiple proposition-changing Baire theorem formulations remain open |
| Crossref DOI lookup and publisher chapter-page inspection for `10.1007/978-3-642-52814-9_3` | 0 | identified Yosida's 1965 pages 68-81 applications chapter and publisher abstract; no exact Chapter 0 theorem text or source credit obtained |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3...16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | 0 | pinned revision `8a178386...e95`, tree `bdc39a31...e2b`; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0632/IntakeProbe.lean)` | 0 | nine distinct adjacent Baire definition, consequence, first/second theorem, and subspace APIs elaborated; output SHA-256 `698e2320...2e2`; no target declaration checked |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts parse as valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0632-pycache python3 -m py_compile Stage1_Instances/THM-M-0632/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-0632/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, planned H5/M4/R4 boundary, null target, source/environment hashes, exact artifact inventory, packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0632` | 1 | expected no-match: no prohibited declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0632 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; the scoped validator checks all new-file text hygiene |

## Known downstream failures

- The catalog gives no truth-valued proposition or cited primary source. Exact theorem text,
  incorporated definitions, assumptions, proof boundary, corrections/errata, translation,
  historical-name resolution, and independent source review remain open.
- The defining property, first/second Baire theorem, preservation/consequence, or
  functional-analysis application is not selected; domains, binders, conclusion, and degenerate
  cases remain open.
- No canonical Lean expression, minimal import result, expression or environment fingerprint,
  checked alternate encoding, or statement mutation certificate exists.
- The API probe establishes adjacent feasibility only. It does not perform the downstream anchor
  audit, identify a source-identical root, or upgrade the root from `M4`.
- Obligation registry and typed graphs, proof, composition and trust checks, readable
  reconstruction, hermetic replay, deterministic evidence bundle, and independent release
  verification remain open.

These failures block statement and theorem execution but do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze the ambiguity and ownership boundary. Only
the integration lane may accept the provisional worker receipt.
