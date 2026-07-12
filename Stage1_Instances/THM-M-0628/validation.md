# Intake validation

Validation date: 2026-07-13 (Asia/Shanghai).
Base revision: `3815f6945257af057dfb5e6b6dfe2be5b6f451d9`.
Base tree: `21a4f0ff758e83ab68c05b7741cdc4720f95cb1c`.

The worker reused the automation-provided canonical `.lake` symlink read-only. No `lake update`,
`lake build`, dependency clone/fetch, package mutation, theorem declaration, or proof was run. The
preflight worktree contained only that symlink, so this is dirty nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0628` | 0 | rank 1048, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 4657,4662 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| source, Stage0, manifest, blueprint, DAG, skill, guideline, neighbor, and pinned-mathlib inspection | 0 | received wording is a topic family; multiple proposition-changing conventions and theorem families remain open |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3...16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and status | 0 | pinned revision `8a178386...e95`, tree `bdc39a31...e2b`; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0628/IntakeProbe.lean)` | 0 | eleven adjacent local-compactness and R1-dependent APIs elaborated; output SHA-256 `f37e817b...776e`; no target declaration checked |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts parse as valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0628-pycache python3 -m py_compile Stage1_Instances/THM-M-0628/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-0628/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, planned H5/M4/R4 boundary, null target, final tested-input hashes, exact artifacts, new-file text hygiene, packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0628` | 1 | expected no-match: no prohibited declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0628 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; untracked new-file hygiene is checked by `check_intake.py` above |

## Known downstream failures

- The catalog gives no truth-valued proposition or primary source. Exact theorem text,
  incorporated definitions, assumptions, proof boundary, corrections/errata, translation, and an
  independent source review remain open.
- The local-compactness convention, separation assumptions, exact theorem family, binders,
  conclusion, and degenerate cases are not selected.
- No canonical Lean expression, minimal import result, expression or environment fingerprint,
  checked alternate encoding, or statement mutation certificate exists.
- The API probe establishes adjacent feasibility only. It does not locate a source-identical root,
  perform the downstream anchor audit, or upgrade the root from `M4`.
- Obligation registry and typed graphs, proof, composition and trust checks, readable
  reconstruction, hermetic replay, deterministic evidence bundle, and independent release
  verification remain open.

These failures block statement and theorem execution but do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze the ambiguity and ownership boundary. Only
the integration lane may accept the provisional worker receipt.
