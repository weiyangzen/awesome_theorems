# Source-statement crosswalk

| Claim component | Available source anchor | Required formal decision | Intake assessment |
|---|---|---|---|
| Item identity | `Docs/researches/math_theorems.md` names `特征函数展开` | Preserve the catalogue identity | Repository metadata only |
| Human statement | The entry says `Green函数的特征函数表示` | Select one quantified kernel identity | Descriptive phrase, not an exact proposition |
| Attribution/date | “众多数学家”, “20世纪” | Record a primary work, edition, theorem/page, assumptions, and errata | Too broad for H evidence |
| Operator/domain | Not stated | Freeze the operator realization, geometry, coefficients, boundary conditions, and measure | Open |
| Spectral premises | Not stated | Freeze self-adjointness, compact resolvent/discreteness, completeness, normalization, and zero-mode policy | Open |
| Conclusion | “representation” only | Freeze the summand, index set, spectral parameter, and convergence/equality mode | Open |
| Lean representation | No formal artifact is cited | Elaborate an exact expression with minimal pinned imports | `M4`; no candidate receives credit |

The catalogue label `已验证` is untrusted under rev-5.6. It is neither a primary proof citation nor
kernel evidence. Repository search found only this wording and generated projections.

## Non-equivalent readings

The phrase may mean a bounded-domain elliptic Green kernel, a resolvent kernel at a spectral
parameter, a generalized eigenfunction integral for continuous spectrum, or merely a
finite-dimensional inverse formula. Even in the discrete case, pointwise equality away from the
diagonal, distributional equality, and operator convergence are different claims. Zero modes can
make the unshifted Green operator nonexistent. These readings cannot be credited as alternate
encodings until a primary statement fixes the scope and checked transports exist.

## Required source audit

1. Identify the intended primary theorem and record edition, theorem/page, assumptions, and errata.
2. Crosswalk the operator, domain, boundary realization, spectral basis, zero modes, and convergence
   statement without importing assumptions absent from the source.
3. Map every source binder and conclusion to Lean before selecting imports or an anchor.
4. Obtain independent review before assigning H0 or running the statement gate.

Current human status is `H5`: the exact theorem has not been identified. This is a source-selection
blocker, not a claim that eigenfunction expansions are unknown mathematics.
