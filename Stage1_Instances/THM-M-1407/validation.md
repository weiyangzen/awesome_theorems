# Intake validation

Base revision: `9cf9d5b9dab219e460bb264ec1e565b071591d89`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify a unique proposition, no canonical
target, expression hash, mutation result, primary-source acceptance, Bernoulli-shift theorem, or
proof is claimed. The shared canonical `.lake` artifacts were used read-only and were not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1407` | exit 0; rank 906, planned, L0/rework_required, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, and `intake-receipt.json` | exit 0; all three structured artifacts are valid JSON |
| `python3 Stage1_Instances/THM-M-1407/check_intake.py` | exit 0; `intake invariant check: ok`; IDs, manifest/DAG membership, planned lifecycle, null target, empty accepted state, six open downstream tasks, completion flags, receipt boundary, and artifact inventory agree |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1407/IntakeProbe.lean)` | exit 0; five generic infinite-product, reindexing, coordinate, measure-preservation, and ergodicity APIs elaborated under Lean 4.29.0 |
| bounded pinned-mathlib Bernoulli-shift/system name search | exit 1 as expected for no matches; intake-only negative name result, not a full anchor audit |
| prohibited Lean construct scan on the owned path | exit 1 as expected for no matches; no `sorry`, `admit`, `axiom`, or `opaque` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1407 .stage1-worker-selftest.json` | exit 0; no whitespace errors |

These checks validate a truthful `planned` intake only. All dependent phases and master acceptance
remain open. Exact primary-source selection and independent review; statement elaboration and all
four required mutation classes; immutable anchor audit; obligation and discovery freezes; proof;
hermetic replay; and release acceptance remain downstream failures.
