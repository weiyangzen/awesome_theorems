# Exact-statement gate: blocked

Item: `S56-M-0566-STATEMENT`  
Theorem: `THM-M-0566`  
Base revision: `c26ceea288012d86365a4383608c4188480e7735`

## Decision

The authoritative repository wording does not determine an exact proposition. It gives the name
`庞特里亚金示性类` (Pontryagin characteristic classes) and the gloss `实向量丛的整系数示性类`
(integral characteristic classes of real vector bundles). A characteristic class is an assignment
or family of cohomology classes, not by itself a truth-valued statement with ordered binders,
hypotheses, and a conclusion.

The conventional formula
`p_i(E) = (-1)^i c_(2i)(E tensor C) in H^(4i)(X; Z)` does not resolve the ambiguity. Depending on
the source and conventions, it can serve as a definition or be part of distinct theorems about
existence, pullback naturality, the total-class Whitney product formula, stability, vanishing by
rank, or universal classes. The repository source selects none of them. It also does not fix:

- topological, smooth, numerable, oriented, or stable real bundles and hypotheses on the base;
- the integral cohomology model, grading, index range, sign convention, and complexification;
- rank-zero, empty-base, disconnected-base, `i = 0`, trivial-bundle, or above-rank behavior; or
- whether an integral equality or a rationalized comparison is intended.

These choices yield inequivalent targets. Selecting one because it is conventional or easier to
encode would broaden or substitute the theorem. Defining a structure whose fields assume the
desired characteristic-class laws and projecting one of those fields would assume, rather than
state faithfully, the requested mathematics.

The statement phase therefore fails at canonical human-claim identity. No Lean module, declaration
or expression, minimal import set, elaborated-expression hash, checked alternate transport, or
mutation-test credit is claimed. There is no truthful `lake env lean <target>.lean` command to run:
an arbitrary proposition that elaborates would be fake evidence for this deliverable.

## Pinned boundary and validation

Commands ran in the worker automation clone on 2026-07-12. The existing canonical `.lake`
artifacts were read only. No `lake update`, build, dependency clone/fetch, or `.lake` mutation was
performed. The untracked `Formalizations/Lean/.lake` symlink predates this phase and was not changed.

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
| `python3 scripts/stage1_target.py show THM-M-0566` | 0 | rank 614, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| scoped repository `rg` for Pontryagin spellings and `THM-M-0566` | 0 | found source metadata, generic references, and an unrelated legacy API audit; no exact target-specific Lean proposition |
| pinned-mathlib `rg` for Pontryagin and characteristic-class spellings | 0 | found only Pontryagin-duality modules, not characteristic classes of real vector bundles |

## Retry condition

An accountable source reviewer must approve an immutable primary-source edition and exact
theorem/page (or explicitly approve a corrected proposition), then freeze the bundle and base
categories, coefficients, grading, normalization, binders, hypotheses, one conclusion, and all
degenerate cases. A later statement run can then encode that claim with minimal pinned imports,
serialize its elaborated expression and environment fingerprint, and execute the removed-hypothesis,
changed-domain, binder-scope, and boundary-case mutations required by section 5.1.

First failed gate: exact source-statement identity. The assigned phase is not genuinely self-tested
to completion, so no `.stage1-worker-selftest.json` is emitted. Statement acceptance, master
acceptance, downstream-node credit, audit completion, and theorem completion remain false.
