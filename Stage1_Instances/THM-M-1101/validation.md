# Intake validation

Base revision: `c79a16ad9e45cceab922e8273d0ed3ea7cc8e4a4`.

The preflight worktree contained the repository-provided untracked `Formalizations/Lean/.lake`
link to canonical pinned artifacts. It was used read-only and not modified. This is nonrelease
intake evidence.

Validation is limited to target-set consistency, source-metadata discovery, dossier structure,
planned-intake invariants, JSON syntax, and whitespace. The repository wording does not identify a
canonical proposition, so no unrelated Lean declaration is presented as elaboration or kernel
evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1101` | exit 0; rank 541, planned, L0/rework_required, legacy artifacts unaccepted, theorem_complete false |
| `curl -L --max-time 20 -s 'https://api.crossref.org/works/10.1093/biomet/57.1.97'` | exit 0; publisher deposit identifies Hastings, title, *Biometrika* 57(1), pages 97-109, publication date 1970-04-01, and DOI |
| `rg -n -i 'Metropolis\|Hastings\|acceptance ratio\|detailed balance\|reversible.*kernel' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems --glob '*.lean'` | exit 0; found general reversible-kernel infrastructure, no Metropolis-Hastings construction or identified terminal theorem |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-1101/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1101/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1101` | exit 0; no output |

Known downstream failures are exact primary-source proposition selection and independent review,
canonical Lean elaboration and statement mutations, formal-candidate audit, frozen obligation
graphs, proof, hermetic replay, and independent release validation. They block audit and theorem
completion but do not invalidate this truthful planned intake.
