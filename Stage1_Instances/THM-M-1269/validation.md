# Intake validation record

Base revision: `73a92b5e63e8eb3c93a5c95d5aead1658ca24c79`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1269` | 0 | rank 445, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1269/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\bsorry\b|\baxiom\b|\bplaceholder\b' Stage1_Instances/THM-M-1269` (inside a fail-on-match shell check) | 1 | Overbroad hygiene check found the truthful prose phrase `axiom audit`; this was a check-design failure, not a proof marker |
| `find Stage1_Instances/THM-M-1269 -name '*.lean' -print -quit` | 0 | empty output: the intake introduces no Lean proof file, so proof-marker scanning is not applicable |
| `git diff --check -- Stage1_Instances/THM-M-1269 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean theorem is
introduced, so no kernel result is claimed. Primary-source identification,
exact statement elaboration, master acceptance, and every dependent phase
remain outstanding.

## Statement validation record

Statement-phase base revision: `8da22023e24f307fb21f41ed93f69f2b8fa82879`.
The existing `.lake` path is a worker-clone symlink to the canonical pinned
artifacts; no dependency update, fetch, build, or mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1269` | 0 | rank 445, planned, hard-mathlib-anchor lane, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1269/Statement.lean)` | 0 | Lean printed the four proposition types and the canonical normalized body; no elaboration errors |
| `python3 -m json.tool Stage1_Instances/THM-M-1269/statement.json >/dev/null && python3 -m json.tool Stage1_Instances/THM-M-1269/intake.json >/dev/null` | 0 | statement record and reconciled intake are valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1269 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The normalized body printed by Lean is
`fun X F => Nonempty X -> BddBelow (range F) -> exists sequence, Tendsto
(fun n => F (sequence n)) atTop (nhds (sInf (range F)))` (with Lean's Unicode
syntax in the actual output). Its whitespace-normalized UTF-8 serialization has SHA-256
`2400402b5b59e3d5e0f3dfebf1a67101fdac06364114b48f9ef5d5d0be6c4516`.
The mutations ensure the omitted hypotheses and the stronger attainment claim
remain visibly distinct proposition surfaces; they are not proofs or accepted
counterexamples. Statement elaboration is self-tested, while proof closure and
master acceptance remain open.
