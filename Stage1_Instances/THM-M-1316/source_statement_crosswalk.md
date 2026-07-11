# Source-Statement Crosswalk

## Repository Claim

The Stage0 source record names Richard Schoen and Shing-Tung Yau, dates the result to
1979, and gives only `ADM质量非负`. That is a discovery label, not an exact statement.

## Primary-Source Candidates

| Root component | Candidate source | Crosswalk | Intake status |
|---|---|---|---|
| Positive mass for asymptotically flat manifolds | Richard Schoen and Shing-Tung Yau, *On the proof of the positive mass conjecture in general relativity*, Communications in Mathematical Physics **65** (1979), 45-76, DOI `10.1007/BF01940959` | Original minimal-surface proof; candidate source for dimension, asymptotic hypotheses, positivity, and rigidity | Primary bibliographic identity located; exact theorem number/page wording, conventions, and errata are not yet audited, so not `H0` |
| General relativity interpretation | Same paper, introductory formulation and constraint-equation discussion | Relates energy condition to the Riemannian scalar-curvature condition in the time-symmetric case | Transport must be formalized; it is not credited at intake |
| Spinorial alternative | Edward Witten, *A new proof of the positive energy theorem*, Communications in Mathematical Physics **80** (1981), 381-402, DOI `10.1007/BF01208277` | Alternative proof route and broader positive-energy context | Route evidence only; it cannot replace the Schoen-Yau root or the separate `THM-M-1317` task |

## Statement Nodes

| Node | Human phrase | Frozen target interpretation | Unresolved source check |
|---|---|---|---|
| `PM-S1` | asymptotically flat | A selected end with a chart, metric decay, derivative decay, and integrability sufficient for ADM mass | Exact falloff order, differentiability, number of ends, and coordinate-invariance assumptions |
| `PM-S2` | nonnegative scalar curvature | Pointwise nonnegative scalar curvature of the Riemannian metric | Exact smoothness and whether integrability is separately assumed |
| `PM-S3` | ADM mass | The conventionally normalized flux limit at the selected end | Normalization constants, orientation, existence, and end dependence |
| `PM-S4` | mass is nonnegative | `0 <= m_ADM(E)` | Whether the primary theorem states strict positivity first and handles equality separately |
| `PM-S5` | rigidity | Zero selected-end mass forces the complete manifold to be Euclidean 3-space up to Riemannian isometry | Exact connectedness, end, and regularity hypotheses for equality |

## Exclusions And Non-Substitutions

- The full positive energy theorem for initial data `(M,g,K)` is broader than this root.
- The inequality alone is a proper subclaim because the frozen root includes rigidity.
- Positivity for Schwarzschild metrics or a finite-dimensional toy mass functional is
  not the geometric theorem.
- Higher-dimensional, spin, charged, boundary/horizon, and asymptotically hyperbolic
  formulations need separate assumptions and cannot be substituted.

## Fidelity Boundary

The candidates above support `H1` discovery only. Acceptance requires inspection of an
immutable edition, exact theorem/page and assumptions, errata search, and independent
review. The Lean statement phase must either match that result exactly or record any
narrowing as a distinct subtheorem without renaming it as the full root.
