# Validation record

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0419` | 0 | rank 74, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0419/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorry\|axiom' Stage1_Instances/THM-M-0419/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no matches (`rg` returns 1 when no lines match) |
| `git diff --check -- Stage1_Instances/THM-M-0419 .stage1-worker-selftest.json` | 0 | no whitespace errors |

That block is intake-only validation. It introduced no Lean declaration and claimed no kernel-proof
result. The statement-phase evidence follows.

## Statement phase

Base revision: `7fe8e74dc1d7b1678d428039fd13be71de273dd8`.

Commands below were run from `Formalizations/Lean` where noted, using the existing pinned `.lake`
environment. Expected-failure probes count as passing only when their exit is `1` for the listed
diagnostic.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0419/Statement.lean` | 0 | Printed the closed `Statement.{uK} : Prop`, `StatementShape`, and the explicit universe/typeclass expansion. |
| `lake env lean ../../Stage1_Instances/THM-M-0419/minimality/WithoutCyclotomic.lean` | 1 expected | `Unknown identifier CyclotomicField`; the weaker Galois-only import is insufficient. |
| `lake env lean ../../Stage1_Instances/THM-M-0419/mutations/RemovedHypothesis.lean` | 1 expected | Cannot synthesize `Field K` / `Semiring K`. |
| `lake env lean ../../Stage1_Instances/THM-M-0419/mutations/ChangedDomain.lean` | 1 expected | Cannot synthesize `Field ℤ`. |
| `lake env lean ../../Stage1_Instances/THM-M-0419/mutations/ChangedBinderScope.lean` | 1 expected | `Unknown identifier n`. |
| `lake env lean ../../Stage1_Instances/THM-M-0419/mutations/BoundaryZero.lean` | 1 expected | `rfl` cannot identify `n = 0` with `n ≠ 0`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0419/{intake,statement}.json` (each file) | 0 | Both structured records parse as JSON. |
| `rg -n 'sorry\|axiom' Stage1_Instances/THM-M-0419 --glob '*.lean'` | 1 | No matches in Lean sources. |
| `git diff --check -- Stage1_Instances/THM-M-0419 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The statement source SHA-256 is
`db9efe3e6fbf82023500558480b83a88b583a51444272f2ee642a05fd38a0422`; the captured elaborator
output SHA-256 is `d30ce90a242e9fe3900ec73e893184ad8878c5b90f5362a4f70ca3846342faeb`.
This is statement elaboration, not a proof of the defined proposition.

## Anchor-audit phase

Base revision: `71fb75ff5b70107068a33e8f5e3f3746a5ae4aa3`.

The node-specific command receipt is `anchor-audit-validation.md`; structured candidate and search
evidence is `anchor-audit.json`. The audit re-elaborated 13 pinned mathlib support anchors and the
frozen statement. It also inspected the immutable external
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50` candidate and classified
it as zero-credit because its source has 22 `sorry` occurrences. This completes a bounded anchor
audit pending master acceptance; it does not establish proof closure.
