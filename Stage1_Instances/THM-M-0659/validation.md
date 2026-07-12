# Intake validation record

Base revision: `734cdf53ab1cc41c766d2a40058a1929f6e1311a`.

This validation is intentionally limited to manifest membership, dossier structure, JSON syntax,
the pinned Lean executable's availability, and fail-closed intake invariants. The repository does
not identify an exact proposition, so elaborating a guessed target would be invalid evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0659` | exit 0; rank 704, L0/rework_required, planned, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `python3 -m json.tool Stage1_Instances/THM-M-0659/intake.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0659/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; identity, rank, lifecycle, empty accepted states, exact open dependency chain, owned artifacts, and no theorem-completion claim checked |
| `if rg -n '[[:blank:]]+$' Stage1_Instances/THM-M-0659; then exit 1; else echo 'owned artifact whitespace check: ok'; fi` | exit 0; no trailing whitespace found |

Known downstream failures are exact source theorem/page and errata, independent source review,
canonical Lean target and environment fingerprint, statement mutations, formal-candidate audit,
obligation registry, proof, composition, provenance/trust closure, hermetic replay, and independent
verification. These prevent all theorem-completion claims but do not invalidate a `planned` intake.
