# Exact-statement gate: blocked

Item: `S56-M-0565-STATEMENT`  
Theorem: `THM-M-0565`  
Base revision: `2534080bb6434bc903d482fcebdf9e0a05b94398`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository's source record. The
complete mathematical wording is `实向量丛的模2示性类` ("mod-2 characteristic classes of real
vector bundles"). This names the Stiefel-Whitney class family, but it is not a proposition and
supplies no primary-source theorem, theorem/page locator, ordered hypotheses, or conclusion.

At minimum, an exact proposition would have to choose among existence, uniqueness from axioms, a
combined axiomatic characterization, pullback naturality, the Whitney sum formula, normalization,
rank vanishing, or an obstruction theorem. Those claims are not interchangeable. Even a selected
characterization would still have to freeze:

- the category of real vector bundles and hypotheses on the base space;
- finite-rank versus stable bundles and the rank convention;
- the cohomology theory, grading, and concrete `F_2` coefficient model;
- whether `w_0 = 1`, vanishing above rank, pullback naturality, and the sum formula are definitions,
  hypotheses, or conclusions;
- the normalization bundle or classifying-space convention; and
- rank-zero, empty, disconnected, and non-paracompact boundary cases.

Choosing any of these alternatives without an authoritative source decision would invent missing
mathematics or substitute a convenient theorem. Introducing an abstract record whose fields assume
the desired classes and laws would likewise not elaborate the source claim. Both moves are
forbidden by sections 2 and 5.1 of the rev-5.6 standard.

The accepted intake artifacts already expose this ambiguity: `instance.json` records
`repository_topic_label_not_yet_a_unique_proposition`, and `scope-map.md` requires selection and
inspection of one exact primary theorem before statement freeze. Thus the intake dependency is
present, but its explicit retry condition has not been satisfied.

## Pinned environment and discovery evidence

Validation ran in the worker clone on 2026-07-12 (Asia/Shanghai). The pre-existing untracked
`Formalizations/Lean/.lake` link/path was read only. No `lake update`, `lake build`, dependency
clone/fetch, or other dependency mutation was performed.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Exact result or scope |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0565` | 0 | rank 613; planned; `L0`; `rework_required: true`; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| `rg -n -i 'Stiefel.?Whitney\|斯蒂菲尔.?惠特尼\|实向量丛的模2示性类\|w_[012]\|w₁\|w₂' --glob '!Stage1_Instances/THM-M-0565/**' --glob '!Docs/Stage1_Blueprint_rev-5.6.md' .` | 0 | found the same underspecified source metadata, unrelated notation, and one API wish-list reference; no source-frozen proposition or target-specific Lean declaration |
| `rg -n -i 'Stiefel.?Whitney\|StiefelWhitney\|characteristic class\|classifying space\|real vector bundle' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | found generic real-vector-bundle and unrelated classifying-space material, but no Stiefel-Whitney declaration or theorem-specific API |

There is no honest `lake env lean <target>.lean` command to run: the required canonical expression
does not exist. Elaborating a generic vector-bundle type or an assumed characteristic-class
interface would test only substrate syntax and would be fake evidence for this statement phase.

## Gate result and retry condition

First failed gate: section 5.1 exact-statement identity. Consequently minimal imports, an
elaborated-expression fingerprint, checked alternate encodings, and meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary mutation tests cannot be produced. Machine status remains
`M4`; no statement acceptance, audit completion, proof credit, or theorem completion is claimed.

Retry only after an accountable source reviewer selects an immutable primary-source edition and
exact theorem/page, resolves errata, and freezes the proposition and every convention listed above.
A later statement worker can then encode that exact proposition, minimize pinned imports, and run
the required elaboration and mutation checks. The assigned phase is not genuinely self-tested to
completion, so no `.stage1-worker-selftest.json` is emitted.
