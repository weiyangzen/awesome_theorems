# Intake validation

Base revision: `ffe94ac84965dc19f4923f88b7566072ddee37ae` (tree
`876a17f277d84dcf06ca672e5cd351edaa294495`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, pinned
environment identity, a narrow Lean API probe, a bounded local name search, proof-escape hygiene,
and whitespace. The catalog record is not a proposition, so elaborating a purported canonical Lean
target would invent missing mathematics. `IntakeProbe.lean` therefore checks only possible
substrate; it introduces no theorem and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1427` | 0 | rank 925, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short` | 0 | before owned edits, only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present |
| `git rev-parse HEAD` | 0 | `ffe94ac84965dc19f4923f88b7566072ddee37ae` |
| `git rev-parse HEAD^{tree}` | 0 | `876a17f277d84dcf06ca672e5cd351edaa294495` |
| `git blame -L 10425,10430 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `for f in Stage1_Instances/THM-M-1427/*.json .stage1-worker-selftest.json; do python3 -m json.tool "$f" >/dev/null \|\| exit; done` | 0 | all four structured artifacts are valid JSON |
| `python3 Stage1_Instances/THM-M-1427/check_intake.py` | 0 | target identity, H5/M4/R4 planned boundary, null formal target, empty accepted state, exact artifact inventory, receipt/self-test agreement, and six open tasks agree |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1427-pycache python3 -m py_compile Stage1_Instances/THM-M-1427/check_intake.py` | 0 | intake validator compiles without adding generated files to the owned path |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1427/IntakeProbe.lean)` | 0 | ten adjacent pinned analytic, meromorphic, composition, iteration, fixed-point, and periodic-point API checks elaborated; no target theorem was stated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned package worktree clean |
| `sha256sum Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Blueprint_rev-5.6.md skills/execute-stage1-rev56/SKILL.md Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | all seven hashes agree with `instance.json` and the provisional receipt |
| `rg -n --glob '*.lean' -i 'Julia.?set\|Mandelbrot\|complex dynamical\|complex dynamics\|rational dynamics\|holomorphic dynamics\|Fatou' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | only three unrelated measure-theoretic Fatou-lemma lines matched; no named complex-dynamics target was found; intake discovery only |
| `test -f Formalizations/Lean/.lake/packages/mathlib/Mathlib/AlgebraicGeometry/RationalMap.lean` | 0 | the separate scheme-theoretic rational-map module exists but is not an analytic-dynamics target |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1427` | 1 | expected no-match exit; no prohibited proof escape in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-1427 .stage1-worker-selftest.json` | 0 | no tracked-diff whitespace diagnostics |
| `for f in Stage1_Instances/THM-M-1427/* .stage1-worker-selftest.json; do git diff --no-index --check -- /dev/null "$f" >/dev/null; code=$?; test "$code" -le 1 \|\| exit "$code"; done` | 0 | every untracked added file passed whitespace checking; diff exit 1 was accepted as normal |

## Known downstream failures

An approved truth-valued target correction, immutable pinpoint primary-source theorem, complete
assumption and errata crosswalk, and independent source review remain open. So do the exact Lean
target and minimal imports, elaborated expression and environment fingerprints, checked transports,
statement mutations, immutable formal-anchor audit, discovery and obligation freezes, typed graphs,
proof and composition, hermetic replay, deterministic evidence bundle, independent release
verification, and master acceptance.

These failures block ordinary theorem execution and completion. They do not invalidate a truthful,
self-tested `planned` intake whose assigned deliverable is the dossier, scope map, and
source-statement crosswalk.
