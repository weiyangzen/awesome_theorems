# Anchor audit validation record

Item: `S56-M-1011-ANCHOR_AUDIT`  
Base revision: `01e0cab0efda724de1660ee854e9a38cebf1e0ab`

## Result

The pinned mathlib revision contains both standard Prokhorov directions. The compact-closure to
tightness theorem matches the corresponding frozen direction. The tightness to compact-closure
theorem requires `T2Space X`, however, while the frozen statement supplies only a
`PseudoMetricSpace X`. `AnchorAudit.lean` checks the two upstream declarations together under the
extra separation assumption and separately verifies that `T2Space X` cannot be synthesized from
the frozen instance context. The wrapper's reported axiom closure is `propext`,
`Classical.choice`, and `Quot.sound`; it contains no placeholder.

Consequently the exact frozen root is `M5`, not `M0-W`. This is a statement/candidate assumption
mismatch discovered by the audit. The statement must be re-frozen with `MetricSpace X` or explicit
`T2Space X`, or a different proof of the non-T2 target must be supplied.

The bounded external search found `FormulaRabbit81/ProkhorovTheorem` at immutable commit
`92d1b9006ca1a8e903a96fbf46ac15782f1e6e95`. Its README identifies it as a historical development
repository for code subsequently moved to mathlib. Its apparent equivalence uses `MetricSpace`, its
relevant unfinished sources contain `sorry` (and one contains `stop`), it uses Lean 4.24.0-rc1 with
mathlib `eed770a...`, and no license file was present in the audited archive. It is therefore an
invalid integration candidate. No dependency was cloned, fetched, installed, or built.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1011/AnchorAudit.lean` from `Formalizations/Lean` | 0 | both anchors checked; extra-`T2Space` wrapper elaborated; frozen-context instance synthesis was expected to fail; axiom report contained no `sorryAx` |
| `python3 Stage1_Instances/THM-M-1011/check_anchor_audit.py` | 0 | statement/pin/source hashes matched; four candidates audited; root classified `M5` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1011` | 0 | rank 260; planned; theorem incomplete |
| GitHub repository API searches serialized in `anchor-audit.json` | 0 | one Prokhorov Lean repository found; subsequent API requests hit HTTP 403, recorded as a limitation |
| `git ls-remote https://github.com/FormulaRabbit81/ProkhorovTheorem.git HEAD refs/heads/main` | 0 | immutable HEAD `92d1b900...` |
| immutable raw-file and codeload inspection | 0 | archive SHA-256 `dcc970c8...`; incompatible toolchain and placeholder-bearing files recorded |
| `python3 -m json.tool Stage1_Instances/THM-M-1011/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1011 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This phase is self-tested anchor-audit work pending master acceptance. It does not repair or
re-freeze the upstream statement, close the exact root, establish `H0` or `R0`, or complete the
theorem. The first failed gate is exact statement match.
