# Exact-statement gate: blocked

Item: `S56-M-1165-STATEMENT`  
Theorem: `THM-M-1165`  
Base revision: `26c19e81aed0ce63fa6787c9db5d397a36f0fb4c`

## Decision

No exact Lean 4 target can be truthfully elaborated from the repository source record. The entire
mathematical wording is `Green函数的特征函数表示` ("an eigenfunction representation of a Green
function"), attributed only to "many mathematicians" in the twentieth century. There is no
primary-source edition, theorem/page, exact formula, or assumptions record.

The wording does not determine:

- the differential operator, its coefficients and realization, or the scalar field;
- the domain/manifold, measure, regularity assumptions, or boundary conditions;
- the eigenvalue indexing, multiplicities, eigenfunction normalization, or completeness premise;
- whether zero modes are excluded, projected away, or avoided with a resolvent parameter;
- the Green-kernel sign and normalization convention or the precise summand;
- whether the asserted equality is pointwise off the diagonal, almost everywhere,
  distributional, weak/operator, or in a norm, and in what convergence order.

These choices produce inequivalent propositions. In particular, an unshifted inverse expansion can
be false or undefined in the presence of a zero eigenvalue. Selecting a bounded-domain elliptic
formula, a shifted resolvent identity, a continuous-spectrum integral, a finite-dimensional matrix
inverse, or only the spectral theorem would invent or substitute mathematics. Green-function
symmetry is separately assigned to `THM-M-1164` and cannot discharge this target.

The intake dependency already records this ambiguity with a null canonical claim and formal target,
open source/scope tasks, and provisional `[H5, M4, R4]`. Consequently this phase fails at canonical
human-claim identity, before minimal imports, an elaborated expression fingerprint, checked
transports, or meaningful removed-hypothesis, changed-domain, binder-scope, and boundary mutations
can be established. No Lean declaration, axiom, placeholder, weakened special case, or broadened
target was introduced. Machine state remains `M4`; statement acceptance and theorem completion are
false.

## Pinned environment and narrow validation

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai). The canonical pinned `.lake`
artifacts were read only; no update, build, dependency clone, or fetch was run.

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
| `python3 scripts/stage1_target.py show THM-M-1165` | 0 | rank 368, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | pinned Lean version and commit recorded above |
| `(cd Formalizations/Lean && lake --version)` | 0 | pinned Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository `rg` search for the Chinese title/wording and English eigenfunction-expansion aliases | 0 | found only the underspecified catalogue/Stage0 wording and neighboring scope references; no exact source-frozen proposition |
| pinned-mathlib `rg` search for Green-function/eigenfunction expansion combinations | 1 | no theorem-specific matching API (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` check: the prerequisite truth-valued target
does not exist. Elaborating a generic interface that assumes the desired identity would be fake
statement evidence, not the assigned deliverable.

## Retry condition

An accountable source reviewer must select an immutable primary-source edition and exact
theorem/page, dispose of errata, and freeze the operator, geometry, boundary conditions, spectral
basis and normalization, zero-mode policy, Green-kernel convention, formula, and convergence or
equality notion. A later statement run can then encode that claim without substitution, minimize
its pinned imports, serialize and hash the elaborated expression, add checked alternate transports,
and execute the four required mutation classes.

First failed gate: exact source-statement identity. The assigned phase is not genuinely self-tested
to its completion gate, so no `.stage1-worker-selftest.json` is emitted and no downstream-node or
theorem-completion credit is claimed.
