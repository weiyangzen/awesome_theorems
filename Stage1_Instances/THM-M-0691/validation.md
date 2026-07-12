# Intake validation

Base revision: `74980872e6ba4cca3e08b1b728b5cf3695421b94`.

This validation covers manifest membership, dossier structure, JSON integrity, repository-source
provenance, and a narrow pinned Lean API probe. Because the repository record does not state the
resolution system or a quantified lower bound, no canonical target, expression hash, mutation
result, or proof is claimed. The canonical `.lake` link and existing pinned artifacts were used
read-only; no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0691` | exit 0; rank 732, planned, legacy artifacts unaccepted, theorem_complete false |
| `rg -n -C 12 'THM-M-0691\|Haken定理\|鸽巢原理证明长度' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | exit 0; only the short result-family gloss and open Stage0 fields were found |
| `python3 -m json.tool Stage1_Instances/THM-M-0691/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0691/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0691/IntakeProbe.lean)` | exit 0; all six finite indexing/cardinality API checks elaborated under pinned Lean 4.29.0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0691 -g '*.lean'` | exit 1 as expected for no matches; no prohibited Lean placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0691` | exit 0; no output |

Known downstream work is intentionally open: primary-source passage and errata audit, independent
review, exact statement elaboration and mutation tests, obligation and discovery freezes, formal
anchor audit, proof, hermetic replay, and release acceptance. These prevent theorem completion but
do not invalidate a truthful `planned` intake.
