# Intake validation

Validation date: 2026-07-13 (Asia/Shanghai).
Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800`.
Base tree: `400e6edf1f69b971b60a367e3ea29be359b07907`.

The worker reused the automation-provided canonical `.lake` symlink read-only. No `lake update`,
`lake build`, dependency clone/fetch, package mutation, theorem declaration, or proof was run. The
preflight worktree contained only that symlink, so this is dirty nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0745` | 0 | rank 1332, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 5493,5498 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| source, Stage0, manifest, blueprint, DAG, skill, guideline, neighbor, and pinned-mathlib inspection | 0 | received wording is a topic family; multiple proposition-changing definitions and result families remain open |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3...16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | 0 | pinned revision `8a178386...e95`, tree `bdc39a31...e2b`; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0745/IntakeProbe.lean)` | 0 | eight materially different adjacent computability APIs elaborated; output SHA-256 `b746af8b...ccd9`; no canonical target or proof body declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts parse as valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0745-pycache python3 -m py_compile Stage1_Instances/THM-M-0745/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0745/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, planned H5/M4/R4 boundary, null target, final input hashes, exact artifacts, packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0745` | 1 | expected no-match: no prohibited declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0745 .stage1-worker-selftest.json` plus scoped new-file hygiene | 0 | no whitespace error; the intake validator checks final newlines, EOF, CR, NUL, and trailing whitespace for untracked artifacts |

## Known downstream failures

- The catalog gives no truth-valued proposition or primary source. Exact theorem text,
  incorporated definitions, assumptions, proof boundary, corrections/errata, translation, and an
  independent source review remain open.
- The computational model, carrier, exact property, binders, conclusion, transports, and
  degenerate cases are not selected.
- No canonical Lean expression, minimal import result, expression or environment fingerprint,
  checked alternate encoding, or statement mutation certificate exists.
- The API probe establishes adjacent feasibility only. It does not perform the downstream anchor
  audit or upgrade the root from `M4`.
- Obligation registry and typed graphs, proof, composition and trust checks, readable
  reconstruction, hermetic replay, deterministic evidence bundle, and independent release
  verification remain open.

These failures block statement and theorem execution but do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze the ambiguity and ownership boundary. Only
the integration lane may accept the provisional worker receipt.
