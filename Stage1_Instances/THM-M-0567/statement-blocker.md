# Exact-statement gate: blocked

Item: `S56-M-0567-STATEMENT`

Theorem: `THM-M-0567`

Base revision: `9898022a0eed3cf9fb3c55a6affb6176224f33cf`

## Decision

The authoritative repository wording does not identify one proposition. It supplies the title
`陈示性类` (Chern characteristic classes) and only the gloss `复向量丛的示性类`
("characteristic classes of complex vector bundles"). A Chern class is a cohomological invariant,
not by itself a truth-valued claim with fixed binders, hypotheses, and conclusion.

The source does not select among existence or uniqueness of the component classes, pullback
naturality, normalization on line bundles, vanishing above the bundle rank, the Whitney direct-sum
formula, a universal-class characterization, or a Chern-Weil comparison. Nor does it fix:

- the category of complex vector bundles, finite-rank convention, or hypotheses on the base;
- the integral cohomology model, coefficients, grading, cup product, and component/total packaging;
- the index range and the conventions for `c_0`, trivial bundles, and ranks below the degree; or
- empty or disconnected bases and the precise pullback/direct-sum operations.

These choices yield inequivalent Lean targets. Selecting a convenient conventional identity would
substitute a theorem not chosen by the source. Introducing an abstract structure whose fields
assume the Chern-class laws and projecting one field would assume the requested mathematics rather
than encode it.

The statement phase therefore fails at canonical human-claim identity, before Lean elaboration.
No canonical module, declaration or expression, minimal-import claim, expression hash, checked
alternate transport, or mutation-test credit is claimed. Running `lake env lean` on an invented
proposition would be fake evidence for this item, so no target file was created.

## Pinned boundary and validation

Commands ran in the worker automation clone on 2026-07-12. Existing canonical `.lake` artifacts
were read only. No `lake update`, build, dependency clone/fetch, or `.lake` mutation was performed.
The untracked `Formalizations/Lean/.lake` path predates this phase and was not changed.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0567` | 0 | rank 615, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| scoped repository `rg` for Chern-class spellings and `THM-M-0567` | 0 | found the broad source metadata and unrelated abstract dependency records; no exact target-specific Lean proposition |
| pinned-mathlib `rg` for Chern-class and Chern-character spellings | 1 | no matching Lean source at the pinned revision (`rg` exit 1 means no match) |

## Retry condition

An accountable source reviewer must approve an immutable primary-source edition and exact
theorem/page (or explicitly approve a corrected proposition), then freeze the bundle/base
categories, coefficients and cohomology model, grading and normalization, ordered binders,
hypotheses, one conclusion, and every boundary case. A later statement run can then encode that
claim with minimal pinned imports, serialize its elaborated expression and environment fingerprint,
and execute the removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations
required by section 5.1.

First failed gate: exact source-statement identity. The assigned phase is not genuinely self-tested
to completion, so no `.stage1-worker-selftest.json` is emitted. Statement acceptance, master
acceptance, downstream-node credit, audit completion, and theorem completion remain false.
