# Intake validation

Base revision: `6446a4b59b8c8950aa4ba92ab10c8d025ce57fc7`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, pinned
environment discovery, and whitespace. The pre-existing untracked `Formalizations/Lean/.lake`
worker artifact makes the tree dirty; it was read only and is nonrelease evidence. Because the
source record does not identify a unique proposition, no canonical Lean file exists and no
elaboration or kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0672` | exit 0; rank 716, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | exit 0; Lake 5.0.0-src+98dc76e |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | exit 0; `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`, `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository `rg` search for the Chinese title, gloss, model companions/completions, and nonstandard analysis | exit 0; found only the underspecified source metadata plus neighboring model-theory material |
| pinned-mathlib `rg` search for model companions/completions, elementary embeddings, ultraproducts, and nonstandard analysis | exit 0; found elementary-map and ultraproduct/Los APIs, but no theorem-specific companion/completion declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0672/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0672/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0672` | exit 0; no output |

There is no truthful `lake env lean <target>.lean` check at intake: selecting transfer, Los's
theorem, a model-companion criterion, or an abstract structure would invent or substitute the root.

Known downstream failures are intentional and fail closed: pinpoint primary-source selection and
independent review, exact statement elaboration and mutation tests, anchor audit, obligation
registry, proof, hermetic replay, and release validation remain open. They prevent statement and
theorem completion but do not invalidate this self-tested `planned` intake.
