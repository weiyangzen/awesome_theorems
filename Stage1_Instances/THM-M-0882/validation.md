# Intake validation

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d` (tree
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`). Validation ran on 2026-07-13 in the isolated worker
clone.

Validation is limited to target-set consistency, dossier and scope invariants, repository-source
provenance, pinned environment identity, a narrow Lean API probe, bounded local topic discovery,
proof-escape hygiene, JSON validity, and whitespace. The catalog gloss is not a binder-complete
proposition, so elaborating a purported canonical Margulis theorem would invent missing mathematics.
The probe therefore checks only possible substrate and receives no statement or proof credit.

The preflight worktree contained only the automation-provided untracked `Formalizations/Lean/.lake`
symlink to canonical pinned artifacts. It was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was performed. This is nonrelease worker
evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0882` | 0 | rank 1434, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | isolated base recorded; initial status contained only the pre-existing automation `.lake` symlink |
| `git blame -L 6460,6465 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -m json.tool` over the three structured owned artifacts and root packet | 0 | valid JSON after finalization |
| `python3 -B Stage1_Instances/THM-M-0882/check_intake.py` and worker replay with `--worker-packet .stage1-worker-selftest.json` | 0 | stable owned-path recipe and worker handoff check agree on target identity, planned H1/M4/R4 boundary, null canonical target, exact inventory, source pins, and six open tasks |
| `sha256sum` over the root packet and all non-receipt owned artifacts | 0 | exact SHA-256 values are bound in `intake-receipt.json`; the mutable provisional receipt excludes itself to avoid recursive hashing |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake 5.0.0 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0882/IntakeProbe.lean)` | 0 | nine adjacent pinned graph/modular APIs elaborated; combined stdout/stderr SHA-256 `55cab969...92c9`; no target theorem stated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a31...c2b`; source tree clean |
| `rg -n -i --glob '*.lean' '\b(margulis\|concentrators?\|expanders?\|gabber[ -]?galil\|isexpander\|vertexexpansion\|edgeexpansion\|cheegerconstant)\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 | expected no exact-topic match; intake discovery only, not an anchor audit |
| `rg -n -i --glob '*.lean' 'sorry\|admit\|sorryax\|^[[:space:]]*(axiom\|constant\|opaque)[[:space:]]\|unsafe' Stage1_Instances/THM-M-0882` | 1 | expected no-match exit; no prohibited declaration in the API-only probe |
| scoped `git diff --check`, per-file no-index whitespace checks, and owned-file invariants | 0 | no whitespace diagnostics; no-index exit 1 accepted only as the expected new-file difference |

Known downstream failures remain deliberately open: master acceptance of this provisional intake;
immutable source admission and independent review; exact source identity and concentrator/expander
transport; graph, carrier, generator, parameter, expansion, constant, explicitness, quantifier, and
boundary decisions; canonical Lean elaboration, fingerprints, checked transports, and mutations;
formal anchor audit; obligation and typed-graph freezes; proof and composition; trust closure;
readable reconstruction; hermetic replay; deterministic evidence bundling; and independent release
verification. These block theorem execution and completion but do not invalidate a truthful,
self-tested `planned` intake.
