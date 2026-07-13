# Intake validation

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source and non-substitution
boundaries, the open task DAG, scoped intake invariants, adjacent pinned Lean APIs, and direct
read-only elaboration of the exact-topic pinned Archive source. It does not validate a canonical
Heron proposition or credit a proof because the source-selected statement is not frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after the
  candidate replay.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned Heron Archive source SHA-256:
  `fc81c1b1a23ff20f5b008d9ee5dcc09abc46ab3cb3e014320c8513bf3cff1d9f`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0203` | exit 0; rank 1535, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before editing | exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 1464,1469 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository crosswalk inspection | exit 0; the catalog and Stage0 supply no formula, area or triangle definition, binders, hypotheses, proof/source locator, correction history, reviewer, or formal artifact |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above; empty package status |
| bounded exact-topic search in repo-local Lean and pinned mathlib | exit 0; located `Theorems100.heron`, its `docs/100.yaml` mapping, supporting Euclidean triangle APIs, and no target-owned legacy artifact; this is not an exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean .lake/packages/mathlib/Archive/Wiedijk100Theorems/HeronsFormula.lean)` | exit 0; exact pinned source elaborated directly in 4.3 seconds with empty stdout SHA-256 `e3b0c442...b855`; mathlib status stayed clean; candidate-source replay only, not repo-local import closure or root credit |
| prebuilt Archive-object inspection | exit 0; zero files under the pinned build's `Archive` library and no `HeronsFormula.olean`; no build was attempted |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0203/IntakeProbe.lean)` | exit 0; seven adjacent geometry, trigonometric, and square-root APIs elaborated; stdout SHA-256 `a218873f...2411a`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `python3 -c` AST parse of `check_intake.py` | exit 0; scoped validator syntax is valid without generating owned files |
| `python3 -B Stage1_Instances/THM-M-0203/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest/DAG identity, H1/M3/R4 null-target boundary, source and pin hashes, candidate boundary, artifact inventory, provisional packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0203/check_intake.py` | exit 0; public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over the owned Lean file | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` loop plus scoped `git diff --check` | exit 0 for whitespace validation; no trailing-space diagnostics |

## Known open gates

An accepted immutable source edition and exact proposition, definition/assumption/conclusion and
proof-boundary mapping, translation, historical attribution, corrections and errata, independent
source review, triangle and area definitions, point-versus-side domain, dimension, ordering,
nondegeneracy, semiperimeter, square-root-versus-squared equality, orientation, and every boundary
case remain open. So do exact target elaboration and mutations, Archive import integration,
exhaustive anchor/provenance/trust audits, discovery and obligation freezes, typed graphs, proof and
composition, readable reconstruction, hermetic replay, deterministic evidence bundling,
independent verification, master acceptance, audit completion, and theorem completion. These gates
do not invalidate a truthful self-tested `planned` intake.
