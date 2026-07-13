# Scope map

## Frozen catalog boundary

The repository fixes only the numerical-analysis label `奇异值分解`, the gloss `矩阵的SVD分解`,
the Beltrami/Jordan attribution, the year 1873, importance "high," and an untrusted `已验证` status.
This identifies the singular value decomposition family but supplies no source citation, formula,
definition chain, binders, premises, conclusion, proof boundary, correction record, or reviewer.

Consequently this intake freezes a theorem family and its non-substitution boundary, not a completed
proposition. No canonical statement, formal expression, alternate encoding, or excluded case is
selected.

## Proposition-changing choices

An approved statement must decide all of the following together:

- real matrices, complex matrices, a conjunction of both, or a more general scalar abstraction;
- arbitrary finite rectangular dimensions, square matrices only, or another source-selected shape;
- `Fin m` and `Fin n` versus arbitrary finite index types and all required order structures;
- full square left/right factors versus thin or compact factors indexed by `min m n` or rank;
- orthogonal/unitary predicates and whether the right factor is starred in `A = U * Sigma * V*`
  or a conventionally equivalent orientation;
- the rectangular diagonal encoding, singular-value indexing, nonnegativity, decreasing order,
  multiplicity, and zero-padding rules;
- existence alone versus any uniqueness claim for values, subspaces, or factors;
- exact ordered binders, universes, typeclasses, foundation profile, and checked transports; and
- empty row/column dimensions and every other degenerate case.

These choices produce inequivalent Lean propositions. They are a resolution checklist, not a
canonical target supplied by this intake.

## Candidate family, not credited

The conventional full finite-dimensional reading says that each finite rectangular real or complex
matrix has square orthogonal or unitary matrices `U` and `V` and a conforming rectangular diagonal
matrix `Sigma`, with nonnegative real diagonal entries, such that `A = U * Sigma * V*`. Thin and
compact SVDs instead use smaller factors and need explicit rank or dimension conventions. Axler's
inspected source states an orthonormal-list linear-map form and derives a rectangular matrix form.
None of these is selected as the canonical claim before source and duplicate review.

## Excluded substitutions

- A theorem only for square, normal, Hermitian, positive, invertible, full-rank, fixed-size,
  real-only, or complex-only matrices cannot silently replace an unspecified general matrix SVD.
- The existence, nonnegativity, order, support, or eigenvalue relation of singular values alone does
  not construct the two factor matrices and final equality.
- The spectral theorem for `A* A` alone omits the left singular vectors, basis extension,
  rectangular zero tail, and final factorization.
- Polar, QR, Schur, eigenvalue, or ordinary diagonalization theorems are distinct.
- Thin or compact SVD cannot replace full SVD, or conversely, without a source-selected target and
  checked equivalence.
- An approximate numerical algorithm, floating-point residual, experiment, oracle, or unchecked
  certificate is not an exact decomposition theorem.
- A structure or hypothesis already storing the desired factors supplies no existence proof.
- `THM-M-0044` artifacts or status cannot be inherited without an accepted identity and ownership
  decision.
- A theorem name, passing API probe, or the catalog's `已验证` label supplies no H or M credit.

## Neighbor and collision boundaries

`THM-M-0044` is a likely duplicate SVD theorem-family entry with a sharper catalog gloss; its root
and evidence remain separate pending integration review. `THM-M-0043` owns the spectral theorem,
`THM-M-0046` and `THM-M-1448` own QR decomposition families, and `THM-M-1451` owns the numerical QR
algorithm. These may eventually provide explicit dependencies, but none grants status by proximity.

## Cases still open

The statement phase must resolve `m = 0`, `n = 0`, `m = 1`, `n = 1`, the zero matrix, rank zero,
full row or column rank, repeated and zero singular values, `m < n`, `m = n`, `m > n`, square normal
and nonnormal matrices, factor nonuniqueness, phase/sign changes, repeated-value subspace rotations,
ordering ties, and rectangular zero padding. No case is silently excluded now.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, singular-value, spectral-basis, Hermitian-matrix,
diagonal-matrix, conjugate-transpose, and unitary-group interfaces are available. The discovery probe
checks representative declarations but states no SVD target. The sibling `THM-M-0044` path contains
a full rectangular Real-and-Complex target and provisional kernel-checked proof bodies; they are a
material formal candidate but cannot identify this target's missing source proposition or transfer
credit before duplicate review and a checked statement transport. These are discovery boundaries,
not the statement gate, anchor audit, or accepted proof.
