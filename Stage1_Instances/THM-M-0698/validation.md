# Intake validation

Base revision: `74980872e6ba4cca3e08b1b728b5cf3695421b94`.

This validation covers target-set consistency, dossier structure, scoped invariants, and a narrow
pinned Lean API probe. The canonical `.lake` symlink and its existing artifacts were used
read-only. No update, build, fetch, or dependency mutation was run. The probe identifies candidate
types only; it is not a statement receipt, anchor audit, proof-body audit, or proof credit.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0698` | exit 0; rank 739, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0698/instance.json` | exit 0; JSON syntax valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0698/task-dag.json` | exit 0; JSON syntax valid |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0698/IntakeProbe.lean)` | exit 0; all five candidate API types elaborated with Lean 4.29.0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0698 -g '*.lean'` | exit 1 as expected for no matches; the owned Lean file contains no prohibited proof placeholder or axiom declaration |
| `git diff --check -- Stage1_Instances/THM-M-0698` | exit 0; no whitespace errors (files are untracked, so the explicit file-content check below is also required) |
| `for f in Stage1_Instances/THM-M-0698/*; do git diff --no-index --check /dev/null "$f" >/dev/null; test $? -le 1; done` | exit 0; every new owned file passed the explicit whitespace check |

Known downstream work remains deliberately open: primary-source inspection and independent review,
canonical expression serialization and mutation testing, frozen obligation/discovery registries,
formal candidate and proof-body provenance audit, typed graphs, proof/composition evidence, hermetic
replay, and independent release validation. Those boundaries prevent theorem completion but do not
invalidate a truthful `planned` intake.
