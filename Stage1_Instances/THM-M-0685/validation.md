# Intake validation

Base revision: `d4da54fa4b81642d3c351d58820f005903bbe09e`.

Validation is limited to target membership, standard consistency, dossier structure, JSON syntax,
and a narrow pinned Lean API probe. The pre-existing untracked `Formalizations/Lean/.lake` link was
used read-only; this is dirty-worktree, nonrelease evidence. Because the source-faithful object
calculus and metatheory are not yet fixed, no canonical target, expression hash, mutation result,
or proof closure is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0685` | exit 0; rank 726, planned, hard-statement-first lane, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | exit 0; Lake 5.0.0-src+98dc76e |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | exit 0; `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`, `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| scoped repository and pinned-mathlib `rg` searches for Gentzen, PA consistency, proof calculi, ordinal notation, and epsilon-zero | exit 0; no exact local Gentzen/PA derivability theorem found; semantic first-order satisfiability and set-theoretic epsilon-zero infrastructure located |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0685/IntakeProbe.lean` | exit 0; checked first-order `Theory`, `Theory.IsSatisfiable`, `Ordinal.epsilon`, `epsilon_zero_eq_nfp`, `lt_epsilon_zero`, and `WellFounded` against pinned mathlib |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0 for both files |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0685 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures remain explicit: exact primary-source passage and independent review,
object-theory and proof-calculus selection, consistency and ordinal-notation encoding, metatheory
boundary, canonical elaboration and mutations, obligation/discovery freezes, proof and trust closure,
hermetic replay, independent verification, and master acceptance. They prevent statement and theorem
completion but do not invalidate a truthful self-tested `planned` intake.
