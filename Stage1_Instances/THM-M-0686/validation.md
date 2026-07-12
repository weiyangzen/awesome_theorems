# Intake validation

Base revision: `d4da54fa4b81642d3c351d58820f005903bbe09e` (tree
`6c5710487c5a06b5a466d1659a1dec535252ddc3`).

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, pinned
environment discovery, nearby Lean infrastructure, and whitespace. The pre-existing untracked
`Formalizations/Lean/.lake` symlink is canonical shared-cache infrastructure; it was read only and
makes this nonrelease evidence. Because the source record does not identify a proposition, the Lean
probe deliberately checks only relevant APIs and no theorem closure is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0686` | exit 0; rank 727, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | exit 0; Lake 5.0.0-src+98dc76e |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | exit 0; `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`, `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository and pinned-mathlib `rg` searches for the source wording, Gentzen, transfinite induction, ordinal induction, and epsilon-zero APIs | exit 0; source remains underspecified; nearby semantic ordinal APIs found, no exact source-selected root |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0686/IntakeProbe.lean` | exit 0; checked `Ordinal.lt_wf`, `WellFoundedLT.induction`, and `Ordinal.epsilon0_eq_nfp` against pinned mathlib |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, and `statement-blocker.json` | exit 0 for all three files |
| scoped intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0686` | exit 0; no output |

Known downstream failures are intentional and fail closed: primary-source proposition selection and
independent review, exact expression elaboration and mutation testing, immutable anchor audit,
obligation registry, proof, trust closure, hermetic replay, and release validation remain open.
They prevent statement and theorem completion but do not invalidate a self-tested `planned` intake.
