# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `紧算子谱定理`, attributes it to Frigyes Riesz,
dates it to 1918, and gives only `紧自伴算子的谱分解` ("spectral decomposition of compact
self-adjoint operators"). Stage0 repeats this metadata and explicitly leaves exact definitions,
assumptions, equivalent formulations, axioms, proof path, and formal artifacts open. The rev-5.6
manifest preserves `已验证` only as `source_status_untrusted`.

No primary-source title, edition, theorem number, page, exact proposition, proof passage, or errata
record is supplied. Attribution and year are therefore discovery metadata, not an accepted `H0`
source crosswalk.

## Candidate source work

The statement/source-audit phases must locate an immutable primary or authoritative passage that
states the intended decomposition theorem, record its exact assumptions and conclusion, and check
edition and errata before independent review. In particular, the audit must not infer a modern
orthonormal-basis formulation merely from the historical attribution.

## Crosswalk

| Repository phrase | Mathematical choice still required | Lean component | Intake status |
|---|---|---|---|
| "compact" | compactness of the bounded endomorphism | `IsCompactOperator T` | pinned API probed; candidate only |
| "self-adjoint" | real/complex field and symmetry convention | `LinearMap.IsSymmetric` on the underlying linear map | pinned API probed; source convention open |
| "spectral decomposition" | complete eigenspace span | `(⨆ mu, eigenspace T mu)ᗮ = bot` | direct mathlib candidate; not selected |
| "spectral decomposition" | eigenbasis or convergent diagonal expansion | basis, orthogonal sum, and convergence data | exact target absent |
| nonzero eigenspaces | finite multiplicity | `FiniteDimensional k (eigenspace T mu)` for `mu != 0` | direct mathlib candidate; possible child only |
| `已验证` | untrusted inventory label | no proposition or proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.InnerProductSpace.Spectrum` describes and exports
`ContinuousLinearMap.orthogonalComplement_iSup_eigenspaces_eq_bot` as a spectral theorem for
compact self-adjoint operators. It also exports
`ContinuousLinearMap.finite_dimensional_eigenspace`. The bounded intake probe checks the exact
types of these declarations and the compact-operator nonzero-spectrum result
`IsCompactOperator.hasEigenvalue_iff_mem_spectrum`.

These are strong formal candidates, but intake does not equate any one of them with the repository
root before exact source selection, normalized type comparison, provenance/trust audit, and checked
transports. No machine closure is credited here.
