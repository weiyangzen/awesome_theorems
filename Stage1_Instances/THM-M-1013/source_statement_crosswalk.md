# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Multivariate weak convergence follows from convergence of every scalar linear projection | H. Cramer and H. Wold, "Some Theorems on Distribution Functions", *Journal of the London Mathematical Society* s1-11 (1936), no. 4, 290-294, DOI `10.1112/jlms/s1-11.4.290` | probability measures on `Fin d -> Real`, `Measure.map` by `x -> sum i, t i * x i`, and mathlib weak-convergence APIs | Original primary paper identified, but scan/hash, exact theorem/page wording, assumptions, and errata are not yet audited: `H1` |
| Weak convergence implies convergence of each projection | Continuous mapping principle applied to a scalar linear map | future forward-direction obligation | Mathematically part of the biconditional; exact API and assumptions are unverified |
| Projection convergence implies multivariate weak convergence | Cramer-Wold convergence device, normally proved through characteristic functions and a continuity theorem | future reverse-direction obligation | Root-specific hard direction; neither a Lean anchor nor terminal proof provenance is credited |
| Random vectors versus laws | Standard formulation: `X_n` converges in distribution to `X` iff every `t dot X_n` converges in distribution to `t dot X` | laws as pushforwards of ambient probability measures | Candidate transport only; measurability and law equality must be checked |
| Dimension and coordinate model | Classical theorem is finite-dimensional over the reals | `Fin d -> Real` or `EuclideanSpace Real (Fin d)` | Representation choice remains open, including `d = 0`; no finite-dimensional generalization is substituted for the coordinate-space claim |

The blueprint gloss "multidimensional distribution convergence" is interpreted as the convergence
device, not merely the related uniqueness result saying that all one-dimensional projections
determine a distribution. The statement phase must confirm this interpretation against the primary
paper, select the exact mathlib weak-convergence predicate, elaborate the ordered binders, and
mutation-test probability assumptions, the universal coefficient vector, dimension zero, and both
directions of the equivalence.

Discovery link (not immutable evidence):

- Original paper DOI: <https://doi.org/10.1112/jlms/s1-11.4.290>

No `H0` or machine-closure claim is made. Required follow-up includes an immutable source copy and
hash, exact theorem/page and assumption mapping, errata search, mathlib/external Lean candidate
inventory at pinned revisions, and independent review.
