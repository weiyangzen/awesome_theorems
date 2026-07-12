# Intake validation

Base revision: `56160b79dacf85088c6e625d50aac63aa6a0e8f9`.

Validation is limited to target membership, standard consistency, dossier structure, scoped intake
invariants, JSON syntax, and whitespace. The intake truthfully records that the repository wording
does not determine an exact proposition. Consequently there is no canonical Lean declaration to
elaborate at this phase, and no kernel-proof result is claimed.

No `lake update`, `lake build`, fetch, clone, or `.lake` mutation was part of this validation.

## Commands and results

All commands ran in this worker clone at base revision
`56160b79dacf85088c6e625d50aac63aa6a0e8f9`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Passed: 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1554` | 0 | Rank 566, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1554/instance.json` | 0 | Valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1554/task-dag.json` | 0 | Valid JSON |
| scoped Python assertions over the instance, owned files, and task DAG | 0 | `intake invariant check: ok`; planned lifecycle, empty accepted states, null exact target, and six ordered open downstream nodes confirmed |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git diff --check -- Stage1_Instances/THM-M-1554` | 0 | No whitespace errors |

An initial toolchain probe from the repository root, `lake env lean --version`, exited 1 because
that directory has no Lake project/default elan toolchain. Re-running the required probe from the
pinned project directory succeeded as recorded above. This failed location probe is not a Lean
statement failure; no exact statement exists in this intake.

## Known downstream failures

- No immutable pinpoint primary theorem source or errata review is frozen.
- The equation, Bäcklund relations, parameter restrictions, domain, regularity, and boundary cases
  are not selected, so the exact Lean statement and its expression fingerprint do not yet exist.
- Formal-candidate discovery, obligation expansion, proof, composition, trust audit, hermetic
  replay, readable review, and independent verification have not begun.

These failures prevent every theorem-completion claim. They do not invalidate a fail-closed
`planned` intake whose purpose is to expose this ambiguity and open the downstream DAG.
