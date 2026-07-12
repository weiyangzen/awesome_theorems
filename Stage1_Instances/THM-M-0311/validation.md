# Intake validation

Base revision: `8f8873f36acbc62e9b41b932a8bb65bf355c8ccf`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. It does not establish canonical statement identity, source fidelity, proof-body
provenance, or theorem closure. The canonical `.lake` dependency symlink was used read-only; no
dependency update, fetch, clone, or build was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0311` | exit 0; rank 813, planned, L0/rework_required, legacy artifacts unaccepted, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0311/IntakeProbe.lean)` | exit 0; `Lp` and `Lp.instCompleteSpace` types printed and real/complex exponent-2 completeness instances synthesized |
| `python3 -m json.tool Stage1_Instances/THM-M-0311/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0311/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0311 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are primary-source inspection and independent review; exact canonical
Lean elaboration, expression fingerprint, and statement mutations; discovery and obligation
registry freezes; formal-anchor and provenance audit; proof/composition evidence; hermetic replay;
and release acceptance. These prevent theorem completion but do not invalidate a truthful
`planned` intake.
