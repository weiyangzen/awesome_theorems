# THM-M-0049 scope map

## Catalog claim held fixed

The repository title is `弗罗贝尼乌斯不等式` (Frobenius inequality), with the entire mathematical
gloss `矩阵秩的不等式` (an inequality of matrix ranks). Intake preserves both strings and the 1911
Frobenius attribution. It does not infer a formula, scalar domain, dimensions, rank convention, or
proof status from the untrusted `已验证` label.

## Candidate theorem family

The conventional Frobenius rank inequality to assess at the statement gate is:

> For composable matrices `A`, `B`, and `C` over a field,
> `rank (A * B) + rank (B * C) <= rank B + rank (A * B * C)`.

Equivalently, `rank (A * B * C) + rank B >= rank (A * B) + rank (B * C)`. A modern inspected
source states this formula for `A in M_(m,n)`, `B in M_(n,p)`, and `C in M_(p,q)` over a field.
This is a discovery candidate, not the accepted repository statement or an `H0` source packet.

Pinned Lean can express one shape with finite index types, `Field K`, `Matrix.rank`, and the
association `((A * B) * C)`. `IntakeProbe.lean` checks only that this function returns `Prop`. It
does not freeze an expression fingerprint, declare the theorem, or establish the inequality.

## Decisions required at statement freeze

1. Admit and independently review a pinpoint source proposition and every incorporated definition.
2. Confirm that the named target is the triple-product lower bound rather than the two-factor upper
   bound, Sylvester rank inequality, a Frobenius-norm inequality, or another namesake.
3. Fix the scalar domain: field, division ring, commutative ring with extra hypotheses, or a
   source-justified specialization such as real or complex matrices.
4. Fix the four finite index types or natural-number dimensions and every `Fintype`, `Finite`,
   decidable-equality, nontriviality, and universe assumption.
5. Fix the exact matrix orientations and multiplication association, including whether a checked
   associativity transport relates `((A * B) * C)` and `A * (B * C)` encodings.
6. Fix whether rank means column-space dimension, row-space dimension, or a transported linear-map
   rank, and check each credited equivalence.
7. Fix the inequality orientation and arithmetic presentation, avoiding truncated subtraction or
   an implicit rearrangement that changes the proposition over natural numbers.
8. Resolve empty index types, zero dimensions, the zero matrix, zero or subsingleton coefficient
   structures, identity factors, invertible factors, and equality cases.
9. Audit the historical Frobenius attribution and 1911 date against a stable primary edition,
   theorem/page locator, translation, correction history, and independent reviewer.

## Prospective proof-route boundary

The inspected modern proof considers the surjective map induced by left multiplication by `A`,
from `range B / range (B * C)` to `range (A * B) / range (A * B * C)`. Comparing the dimensions
of these quotients yields the candidate inequality. This identifies prospective range, quotient,
surjectivity, and dimension-subtraction nodes only. No obligation registry is frozen and no node
receives closure credit at intake.

Pinned alternatives may instead derive a future proof from rank-nullity and subspace inclusion.
Such a proof route would still need a source-to-node crosswalk and checked composition; the
availability of component lemmas does not select or close the root.

## Explicit exclusions

- `rank (A * B) <= min (rank A) (rank B)` used as the target rather than an adjacent upper bound.
- The Sylvester inequality `rank (A * B) >= rank A + rank B - n`, or its additive form, used as
  the triple-product root without a checked derivation and accepted identity decision.
- `rank A + rank B <= n` under `A * B = 0`, which is an adjacent zero-product theorem.
- Frobenius norm, Frobenius reciprocity, Frobenius endomorphism, Perron-Frobenius, or Frobenius
  number inequalities.
- Equality characterizations, generalized inverses, or the equation `B = B * C * X + Y * A * B`
  substituted for the base inequality.
- Real-only, complex-only, square-only, fixed-dimension, invertible-factor, or zero-product special
  cases unless an accepted source makes exactly that narrow claim canonical.
- A hypothesis or structure field storing the desired inequality, a numerical rank experiment,
  or an unchecked certificate.
- The catalog label, adjacent API probe, theorem name, or modern source lead treated as proof or
  exact-statement evidence.

## Boundary cases to resolve

No case is silently excluded at intake. The statement phase must decide zero-sized intermediate
spaces, empty outer index types, zero and identity matrices, rank-zero middle matrix, full-rank or
invertible factors, equality cases, the zero/subsingleton scalar structure, and whether the source
requires every dimension to be positive.

## Neighbor and namesake boundaries

- `THM-M-0048` is Cauchy-Binet, a determinant minor-sum identity rather than a rank inequality.
- `THM-M-0050` is Sylvester's law of inertia, not the Sylvester matrix-rank inequality and not this
  Frobenius inequality.
- `THM-M-0051` is the Grassmann identity, a dimension formula that may support a proof but cannot
  inherit or substitute for this root.
- `THM-M-0066` is Perron-Frobenius, a spectral theorem with no shared statement or proof credit.

