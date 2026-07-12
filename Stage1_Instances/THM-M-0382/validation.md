# Intake validation

Base revision: `6f601f70dc531aafc2c0e73ea51db67cebeb3ad9`.

Validation is limited to manifest membership, dossier structure, scoped invariants, and a narrow
pinned Lean API probe. Since the repository wording does not select one source-exact proposition,
no canonical target, expression hash, mutation result, formal anchor, or proof is claimed. The
worker's shared canonical `.lake` link was used read-only; no dependency update or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0382` | exit 0; rank 870, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0382/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0382/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0382/IntakeProbe.lean)` | exit 0; seven pinned analytic API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0382` | exit 0; no output |

Known downstream failures are intentionally open: immutable primary-source inspection and review,
canonical clause selection, exact Lean target elaboration and mutation tests, discovery and
obligation freezes, anchor audit, proof, hermetic replay, and release acceptance. They prevent
theorem completion but do not invalidate a truthful `planned` intake.
