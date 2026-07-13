# Scope map

## Received claim

The repository gives only the name `冯·诺依曼迹不等式`, the attribution John von Neumann, the year
1937, and the gloss `矩阵迹的最大值不等式`. The name points to the von Neumann trace-inequality
family; the gloss says only that a trace has an extremal bound. Neither supplies a formal
proposition.

## Source-guided candidate family not credited

A familiar modern formulation concerns two matrices and bounds the magnitude or real part of a
trace pairing by a correspondingly ordered sum of products of their singular values. Related
statements express that sum as a maximum over unitary or orthogonal changes of basis, or specialize
to real matrices and transpose. This description is only a theorem-family locator. It is not the
canonical claim until an admitted source fixes every convention and checked transports relate any
credited variants.

## Proposition-changing decisions

The statement phase must freeze all of the following:

1. Real or complex scalars, or a more abstract RCLike setting.
2. Square matrices of one order versus rectangular matrices with compatible dimensions.
3. The exact trace expression: `trace (Aᴴ * B)`, `trace (A * Bᴴ)`, `trace (Aᵀ * B)`, or another
   pairing, including multiplication order and conjugation convention.
4. Whether the left side is an absolute value, complex norm, real part, or an ordered real trace.
5. The number, indexing, multiplicity, zero-padding, and descending order of singular values.
6. The exact right-hand finite sum and all index-range or rank/min-dimension conventions.
7. Whether only an upper bound is asserted or whether an equality/maximization characterization,
   equality conditions, or both belong to the root.
8. Ordered binders, dimension nonemptiness, finite-dimensionality, decidable-equality and basis
   assumptions, and all casts from finite sums to the scalar/order codomain.
9. Boundary behavior at dimension zero, zero/rank-deficient matrices, rectangular zero dimensions,
   repeated singular values, and the real-versus-complex specialization.

Each choice changes the proposition or its formal representation. A prose assertion of equivalence
cannot replace a kernel-checked transport.

## Explicit exclusions

- A generic trace identity such as cyclicity, conjugate-transpose compatibility, or a sum of
  diagonal entries used as the requested inequality.
- Cauchy-Schwarz, Holder/Schatten, Ky Fan, Golden-Thompson, Klein, or rearrangement inequalities
  substituted merely because they can imply or resemble a trace bound.
- A positive-semidefinite, Hermitian, normal, diagonal, real-only, square-only, rank-one, or fixed
  numerical special case selected without source authorization.
- A maximization formula, equality condition, or lower companion bound silently added to or removed
  from the root.
- A proposition whose assumptions store a singular-value decomposition or already assume the
  desired trace inequality.
- The untrusted `已验证` label, theorem-name match, historical citation lead, API probe, or bounded
  no-match search treated as source or proof credit.
- `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_058.lean`: that legacy slot is explicitly
  `THM-M-0430` (Langlands reciprocity), not this target.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the following adjacent
interfaces elaborate:

- `Matrix.trace`, `Matrix.trace_conjTranspose`, and `Matrix.trace_mul_comm`;
- `LinearMap.trace_eq_sum_inner` and `LinearMap.IsSymmetric.trace_eq_sum_eigenvalues`;
- `LinearMap.singularValues`, nonnegativity, monotonicity, and finite-rank support results.

These are statement substrate only. The bounded search over pinned mathlib and repo-local Lean found
no trace/singular-value bridge or von-Neumann-trace declaration. Complete formal candidate discovery
belongs to the later anchor-audit phase.

No canonical expression, environment fingerprint, alternate encoding, mutation suite, discovery
protocol, obligation registry, or proof state is frozen at intake.
