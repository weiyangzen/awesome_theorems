# Intake validation record

Base revision: `bce5c3a2691f71daf054f0f11b5cf66c120a7306`.

The structural preflight commands were run from the repository root on 2026-07-12. Dossier-local
checks below are the smallest real validation for an intake that intentionally introduces no Lean
declaration. The absence of a Lean run is a statement-boundary result, not kernel evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1556` | 0 | rank 568; planned; L0/rework_required; no accepted legacy artifacts; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1556/instance.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1556/task-dag.json >/dev/null` | 0 | open DAG is valid JSON |
| `python3 - <<'PY' ... PY` (scoped assertions over `instance.json`, `task-dag.json`, and owned files) | 0 | `intake invariant check: ok`; identity, planned lifecycle, empty accepted state, incomplete theorem, null canonical claim, exact downstream chain, open states, and owned-file existence checked |
| `git diff --check -- Stage1_Instances/THM-M-1556` | 0 | no whitespace errors |

Known failures are the missing unique source proposition, exact source transcription and review,
canonical Lean target and environment fingerprint, anchor audit, obligation registry, proof,
hermetic validation, and independent release verification. These failures block every dependent
node and theorem completion; they do not prevent a truthful, self-tested `planned` intake.
