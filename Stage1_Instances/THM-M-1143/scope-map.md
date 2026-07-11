# Scope map

## Preserved source scope

- Object: a harmonic function.
- Hypothesis: the function is bounded.
- Conclusion: the function is constant.
- Context: differential equations / partial differential equations, distinct from the ODE theorem
  also named Liouville theorem (`THM-M-1375`).
- Attribution and date in the repository: Joseph Liouville, 1844.

## Decisions required before statement freeze

The statement phase must identify a primary source and freeze the ambient space and dimension,
scalar codomain, whether the domain is all of `R^n`, the analytic definition of harmonicity and its
regularity requirements, whether bounded means a two-sided global norm bound or a one-sided bound,
and the precise constant-function conclusion. It must explicitly handle dimension zero and other
degenerate cases admitted by the chosen formulation.

## Explicit exclusions

- Liouville's theorem for bounded entire holomorphic functions unless a checked equivalence and
  source crosswalk establish it as the intended statement.
- Liouville formulas for ODEs, number-theoretic approximation theorems, and the distinct target
  `THM-M-1375`.
- Positive-harmonic, subharmonic, manifold, exterior-domain, or growth-condition variants chosen
  merely because they are easier to formalize.
- Treating the repository status `已验证` as source or machine-proof evidence.
