# Intake validation

Base revision: `e3d0fd205c9c81486cb86f68cdc66d4d4e5bb264`.

Validation is limited to manifest membership, dossier structure, JSON integrity, scoped planned
intake invariants, forbidden proof-token hygiene, and whitespace. The repository record does not
identify an exact equation, so no Lean file was invented and no elaboration or kernel-proof result
is claimed. The canonical `.lake` link was not accessed or mutated.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0524` | exit 0; rank 896, planned, L0/rework_required, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0524/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0524/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; IDs, planned lifecycle, null canonical claim, empty accepted state, open downstream DAG, false completion flags, and artifact inventory agree |
| `git diff --check -- Stage1_Instances/THM-M-0524` | exit 0; no whitespace errors |

The final forbidden-token scan and JSON checks for the receipt and worker manifest are recorded in
`intake-receipt.json`. Known downstream failures remain intentionally open: exact primary-source
inspection and independent review; canonical statement elaboration and mutation tests; anchor
audit; obligation, provenance, trust, and evidence graphs; proof; hermetic replay; and independent
release acceptance. They prevent theorem completion but do not invalidate a truthful `planned`
intake.
