# Intake validation record

Validation date: 2026-07-12 (Asia/Shanghai). Base revision:
`b33312e792c156f58e747a0f53dfa36691ee0658`.

| Command (from repository root) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0169` | 0 | Rank 666; planned; L0/rework_required; theorem_complete false |
| `python3 Stage1_Instances/THM-M-0169/check_intake.py` | 0 | Dossier identities, planned/open invariants, dependencies, and merge-target references pass |
| `python3 -m json.tool Stage1_Instances/THM-M-0169/intake.json >/dev/null` | 0 | Valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0169/task-dag.json >/dev/null` | 0 | Valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0169 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The source discovery used:

```text
curl -L --fail --silent --show-error --max-time 30 -A Mozilla/5.0 \
  -o /tmp/hilbert1901.pdf \
  'https://www.ams.org/journals/tran/1901-002-01/S0002-9947-1901-1500557-5/S0002-9947-1901-1500557-5.pdf?download=1'
pdftotext -layout /tmp/hilbert1901.pdf /tmp/hilbert1901.txt
sha256sum /tmp/hilbert1901.pdf
```

All three commands exited 0; the digest is recorded in `source_statement_crosswalk.md`. Network
retrieval is discovery evidence, not a hermetic or immutable source receipt.

No `lake env lean` command is applicable to this intake artifact: the exact proposition and imports
are intentionally blocked on the source-regularity decision and belong to the dependent statement
phase. Thus this record supplies structural intake evidence only, not kernel, source-acceptance, or
theorem-completion evidence. Known failure: no independent integration-lane review has occurred.
