# Intake validation

Base revision: `028e2535b68678b8296e63e2cacb05ed9775a2d8` (tree
`2845b046547e71984e5d93f4f04045663bd3bcbb`).

Validation is limited to target membership, repository-standard consistency, dossier structure,
JSON syntax, planned-state invariants, pinned toolchain identity, a bounded pinned-mathlib name
search, proof-hole hygiene, and whitespace. The source record does not determine a proposition, so
elaborating an invented Lean target would be substitution rather than validation. `IntakeProbe.lean`
therefore checks only generic candidate APIs; it introduces no theorem and supplies no statement or
proof credit.

The automation-provided `Formalizations/Lean/.lake` symlink exposes the canonical pinned artifacts.
It was present before this work and was used read-only. No update, build, dependency clone, fetch,
or `.lake` mutation was run.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1401` | 0 | rank 900, planned, L0/rework_required, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1401/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1401/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1401/intake-receipt.json` | 0 | valid JSON after finalization |
| `python3 Stage1_Instances/THM-M-1401/check_intake.py` | 0 | identity, lifecycle, rank, null target, empty accepted state, artifact inventory, open downstream DAG, and false completion flags agree |
| `python3 -m py_compile Stage1_Instances/THM-M-1401/check_intake.py` | 0 | intake validator compiles |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1401/IntakeProbe.lean)` | 0 | six generic stream, semiconjugacy, iteration, and periodic-point APIs elaborated; no target theorem is stated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n 'subshift\|shift space\|symbolic dynamics\|Bernoulli shift' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matches; bounded name search only, not a complete anchor audit |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^\s*axiom\b' Stage1_Instances/THM-M-1401` | 1 | no forbidden Lean proof-hole declarations in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-1401 .stage1-worker-selftest.json` | 0 | no whitespace errors after finalization |

Known downstream failures remain deliberately open: exact primary-source identity and independent
review; canonical statement elaboration, expression/environment fingerprints, checked transports,
and mutations; immutable formal anchor audit; obligation and typed-graph freeze; proof; hermetic
replay; deterministic evidence bundle; and independent release verification. These prevent audit
and theorem completion but do not invalidate a truthful `planned` intake.
