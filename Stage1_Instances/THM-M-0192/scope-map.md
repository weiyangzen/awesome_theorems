# Scope map

## Included claim

- Deligne's weight/Riemann-hypothesis theorem for a smooth projective variety over a finite field.
- Frobenius acting on degree-`i` l-adic etale cohomology, with the prime `l` different from the
  characteristic.
- Algebraicity and the source-faithful absolute-value/weight assertion for every relevant
  eigenvalue and embedding.
- The theorem's role as the remaining deep component completing the Weil conjectures. This
  historical consequence is not permission to claim a new proof of every antecedent component.

## Decisions required at the statement gate

The next phase must inspect an immutable scan of Deligne's numbered theorem and freeze whether the
source uses arithmetic or geometric Frobenius, the algebraic closure and coefficient field, the
meaning of variety/scheme, connectedness and dimension assumptions, the allowed cohomological
degrees, and the exact quantification over embeddings. It must also distinguish an eigenvalue from
its reciprocal root so that `q^(i/2)` is not accidentally inverted.

Ordered binders, universes, minimal imports, l-adic/etale-cohomology interfaces, the foundation and
choice profile, boundary cases, and checked transports to zeta-factor formulations belong to the
statement phase. An abstract structure carrying purity as a field cannot be used to make the
target true by definition.

## Explicit exclusions

- The whole four-part Weil-conjectures package as a duplicate of `THM-M-0191`.
- Dwork rationality, the Grothendieck trace formula, or the functional equation alone.
- Weil II's later general theory of weights for mixed sheaves as a broadened substitute.
- A result only for curves, projective space, abelian varieties, or one fixed variety.
- A generic linear-algebra eigenvalue statement with the etale-cohomological geometric content
  erased.
- A theorem assuming the desired purity/absolute-value conclusion under another name.

The first downstream blocker is source-faithful transcription and independent confirmation of the
numbered statement and conventions before a Lean proposition can be frozen.
