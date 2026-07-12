# THM-M-0048 scope map

## Catalog claim held fixed

The repository title is `柯西-比内公式` (Cauchy-Binet formula), with the gloss `矩阵乘积的行列式公式`
(determinant formula for a matrix product). Intake preserves both strings. It does not infer a
field, dimensions, or a particular minor encoding from the untrusted `已验证` label.

## Candidate theorem family

The conventional full family to assess at the statement gate is:

> For an `m`-by-`n` matrix `A` and an `n`-by-`m` matrix `B`, the determinant of `A * B` is the sum,
> over the `m`-element subsets `S` of the intermediate indices, of
> `det(A[:, S]) * det(B[S, :])`.

This paragraph is a discovery candidate, not the accepted canonical claim. In particular, intake
does not decide whether the source requires `m <= n` or makes an empty-sum convention cover
`m > n`, nor whether the intended coefficient domain is a field or a commutative ring.

Pinned Lean can express one candidate using `Fin m`, `Fin n`, `CommRing R`,
`Set.powersetCard (Fin n) m`, and `Set.powersetCard.ofFinEmbEquiv.symm` to order each subset.
`IntakeProbe.lean` checks that expression only as a `Prop`-valued function. It is not frozen as the
target, given a declaration, or used for proof credit.

## Decisions required at statement

- Admit and independently review a pinpoint theorem/proof source and its incorporated definitions.
- Decide full rectangular minor-sum Cauchy-Binet versus square determinant multiplicativity.
- Fix the coefficient domain and all algebraic typeclass assumptions.
- Fix dimensions, row/column orientation, index types, and the order of `A` and `B`.
- Define the summation carrier, subset ordering, minors, and determinant sign convention.
- Decide whether `m <= n` is a hypothesis or whether the formula includes `m > n` by convention.
- Fix whether arbitrary finite ordered types or only `Fin` indices constitute the canonical root.
- Elaborate and fingerprint one exact expression, then check all credited transports.
- Mutation-test the domain, dimension relation, binder scope, product order, and boundary cases.

## Boundary cases to resolve

- `m = 0`, including the determinant of the empty square matrix and the unique empty subset;
- `n = 0` with `m > 0`, and the zero product versus an empty subset sum;
- `m > n`, when no `m`-element intermediate subset exists;
- `m = n`, where the formula should reconcile with square `Matrix.det_mul`;
- zero matrices and matrices with repeated or dependent rows/columns;
- singleton and other low-dimensional cases;
- characteristic two, where signs collapse but the identity should remain meaningful;
- nontriviality assumptions, if any, versus the zero commutative ring.

## Excluded substitutions

- `Matrix.det_mul` presented as the full rectangular minor-sum theorem without a checked scope
  decision and transport;
- a field-only, real-only, complex-only, fixed-dimension, or full-rank theorem silently replacing a
  more general accepted source claim;
- the Weinstein-Aronszajn/Sylvester identity `det(1 + A * B) = det(1 + B * A)`;
- Laplace expansion, determinant multilinearity, or a single minor identity without the final sum;
- a Cauchy-Binet inequality, rank inequality, Gram determinant consequence, or compound-matrix
  identity without checked equivalence to the root;
- numerical determinant experiments, floating-point residuals, or unchecked certificates;
- a hypothesis or structure that directly stores the desired formula;
- the catalog label, a theorem-name match, or the intake probe used as proof evidence.

## Neighbor boundaries

- `THM-M-0041` (Cayley-Hamilton) concerns annihilation by the characteristic polynomial, not
  determinant expansion of a rectangular product.
- `THM-M-0044` (singular value decomposition) may use Gram determinants but is a factorization
  theorem, not this identity.
- `THM-M-0047` (LU decomposition) is a triangular factorization theorem; determinant
  multiplicativity may be an ingredient, but it does not supply the Cauchy-Binet sum.
- `THM-M-0050` (Sylvester's law of inertia) concerns congruence invariance of a real symmetric
  form, not the Sylvester determinant identity and not Cauchy-Binet.

## Profiles held open

Lean 4 dependent type theory and pinned mathlib are the intended formal environment. Exact uses of
classical decidability, finite choice, quotients, extensionality, and any source-level foundation
assumptions remain downstream. No oracle, native shortcut, experiment, or numerical computation is
eligible for proof credit.
