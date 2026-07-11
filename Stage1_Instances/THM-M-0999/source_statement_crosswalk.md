# Source-statement crosswalk

| Claim component | Human source anchor | Future Lean surface | Intake assessment |
|---|---|---|---|
| Logarithmic Sobolev inequality / entropy upper bound | Leonard Gross, "Logarithmic Sobolev Inequalities", *American Journal of Mathematics* 97(4) (1975), 1061-1083, DOI `10.2307/2373688` | No declaration selected | The author and year agree with Stage0 metadata, but theorem/page, edition hash, assumptions, and errata are not yet audited: `H2` |
| Entropy functional | Gross's integral expression involving a function squared and its logarithm | A definition using mathlib measure/integral APIs | The repository's phrase "entropy upper bound" omits the measure, normalization, zero convention, and integrability premises |
| Gaussian measure | Historically central finite-dimensional Gaussian specialization of the Gross inequality | A probability measure on Euclidean space | Covariance and density normalization must be transcribed before the constant can be frozen |
| Dirichlet energy and factor 2 | Candidate standard-normal Gaussian form `Ent_gamma(f^2) <= 2 integral ||grad f||^2 d gamma` | Differentiability/Sobolev-space expression not yet chosen | Provisional target shape only; no exact-constant or equivalence credit |
| Function class | Source-specific admissibility/closure conditions | Smooth, Sobolev, or form-domain predicate | Unresolved; choosing a convenient smaller class without a source crosswalk would substitute the theorem |

Repository genealogy:

- `Docs/Stage0_Blueprint.md` names Leonard Gross, dates the proposal to 1975, and describes only
  "an upper bound for entropy"; it explicitly leaves exact definitions and assumptions unfinished.
- `Docs/Stage1_Blueprint.md` carries that wording into the Lean 4 queue and labels the old source
  status as verified, but rev-5.6 declares that label untrusted and grants no proof credit.
- `Docs/Stage1_Targets_rev-5.6.json` fixes membership, rank 279, `L0 / rework_required`, and the
  `hard_mathlib_anchor_and_wrapper` lane; it does not supply a mathematical statement.

Discovery locator (not an immutable evidence receipt):

- Gross paper: <https://doi.org/10.2307/2373688>

The next phase must obtain a stable primary-source copy, hash it, identify the exact theorem and
pages, transcribe every domain and premise, settle Gaussian/energy normalization, and only then
elaborate the canonical Lean expression. It must also search corrections or errata and independently
review the crosswalk. Until that happens, neither the sharp finite-dimensional form nor a weaker
smooth-function version may be presented as the exact repository theorem.
