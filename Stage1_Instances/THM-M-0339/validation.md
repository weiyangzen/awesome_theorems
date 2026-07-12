# Intake validation

Base revision: `3d8dd27e4ff1200a2d9c8daaa9cae8072eca6241`.

Validation covers manifest membership, dossier structure, JSON integrity, primary-source retrieval,
and a narrow pinned Lean API probe. The existing canonical `.lake` link/artifacts were used read-only;
no dependency update, fetch, or build was run. The pre-existing untracked `Formalizations/Lean/.lake`
entry makes this nonrelease evidence. No canonical expression, mutation result, or proof is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0339` | exit 0; rank 832, planned, legacy artifacts unaccepted, theorem_complete false |
| `curl -L --fail https://arxiv.org/pdf/1306.3969 -o /tmp/mss-kadison-singer.pdf` and `pdftotext -layout ...` | exit 0; arXiv v4 primary source retrieved and pp. 1-3 inspected |
| `python3 -m json.tool Stage1_Instances/THM-M-0339/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0339/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0339/IntakeProbe.lean)` | exit 0; all six pinned API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0339` | exit 0; no output |

Known downstream failures are intentionally open: exact endpoint selection, implication-boundary
freeze, canonical statement elaboration and mutation tests, anchor audit, obligation/provenance
graphs, proof, hermetic replay, source/formal independent review, and release acceptance. They block
theorem completion but do not invalidate a truthful `planned` intake.
