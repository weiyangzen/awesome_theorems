# Intake validation

Base revision: `74980872e6ba4cca3e08b1b728b5cf3695421b94`.

Validation is limited to target membership, standard consistency, dossier structure, JSON syntax,
and a narrow pinned Lean API probe. The pre-existing untracked `Formalizations/Lean/.lake` link was
used read-only; this is dirty-worktree, nonrelease evidence. Because the repository does not supply
a proposition or unique calculus, no canonical target, expression hash, mutation result, or proof
closure is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0693` | exit 0; rank 734, planned, hard-statement-first lane, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| scoped repository and pinned-mathlib `rg` searches for the target, sequent calculus, and Gentzen | exit 0; repository contains only topic/rule descriptions and adjacent proof-system material; no exact target-local proposition or mathlib sequent-calculus module was found |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0693/IntakeProbe.lean` | exit 0; checked language, bounded-formula, theory, list, and membership API types against pinned mathlib |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0 for both files |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `rg -n '\b(sorry|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0693 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0693 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures remain explicit: proposition and calculus selection, exact primary-source
passage and independent review, canonical Lean elaboration and mutations, obligation/discovery
freezes, anchor audit, proof and composition, hermetic replay, independent verification, and master
acceptance. They prevent statement and theorem completion but do not invalidate a truthful
self-tested `planned` intake.
