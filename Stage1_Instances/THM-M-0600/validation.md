# Intake validation

Base revision: `a1bd625c34bac608d64b423cf1ca0c9b6db6adb0`.

Validation is limited to repository/manifest consistency, dossier structure, scoped invariants,
source-record discovery, JSON syntax, and whitespace. There is intentionally no `.lean` file in
this intake: a canonical Lean expression has not been selected, so running an unrelated elaboration
would provide false evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0600` | exit 0; rank 638, L0/rework_required, planned, theorem_complete false |
| `rg -n -i 'Morse lemma\|莫尔斯引理\|nondegenerate critical point' Formalizations Docs` | exit 0; repository metadata/source prose found; no theorem-specific Lean declaration found |
| `python3 -m json.tool Stage1_Instances/THM-M-0600/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0600/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0600` | exit 0; no output |

Known downstream failures: pinpoint source inspection and independent review, exact differentiability
and index conventions, canonical Lean elaboration, formal anchor audit, frozen obligation registry,
proof, trust and provenance closure, hermetic replay, readable reconstruction review, and independent
verification remain open. These prevent audit and theorem completion but do not invalidate a
fail-closed planned intake.
