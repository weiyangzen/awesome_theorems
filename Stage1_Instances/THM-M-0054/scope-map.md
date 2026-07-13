# Scope map

## Preserved theorem family

The intake preserves the catalog's Perron-Frobenius family for finite square nonnegative matrices.
An exact root may be selected only from an immutable, independently reviewed source passage.
Candidate clause bundles, none yet credited as the theorem, include:

- an arbitrary entrywise-nonnegative matrix has its spectral radius as an eigenvalue with a
  nonzero nonnegative eigenvector;
- an irreducible nonnegative matrix has a positive Perron eigenvector and a positive simple Perron
  root dominating the moduli of all eigenvalues, while other peripheral eigenvalues may remain;
- a primitive nonnegative or entrywise-positive matrix has strict peripheral dominance; and
- a classification of peripheral eigenvalues and their cyclic structure for irreducible matrices.

These are not interchangeable. The zero matrix shows that an arbitrary nonnegative matrix need
not have a positive Perron root. An identity matrix in dimension greater than one shows that its
positive spectral radius need not be simple. An irreducible periodic matrix can have other
eigenvalues of equal modulus, so strict dominance requires stronger conditions.

## Decisions required at statement freeze

1. Preserve one lawful complete source edition, select a precisely delimited result and proof
   boundary, map every incorporated definition, audit translations/corrections, and obtain
   independent source approval.
2. Reconcile the catalog's 1907 date and combined Perron/Frobenius attribution with Perron's
   positive-matrix result and Frobenius's later nonnegative-matrix extensions. Do not merge their
   hypotheses or conclusions.
3. Fix the scalar field, finite square index type, dimension/nonemptiness assumptions, and whether
   entries are real, nonnegative real, or embedded into complex matrices for spectrum claims.
4. Define entrywise positivity/nonnegativity and choose the exact structural hypothesis: none,
   irreducible, primitive, or strictly positive.
5. Fix the spectral-radius representation and its bridge to real or complex eigenvalues,
   characteristic roots, and algebraic multiplicity.
6. State the conclusion clause by clause: eigenvalue existence, sign of the root, nonnegative or
   positive eigenvector, algebraic/geometric simplicity, modulus dominance, strict dominance,
   uniqueness up to scaling, and peripheral cyclicity.
7. Fix eigenvector orientation and normalization, including whether both left and right vectors
   are included.
8. Freeze ordered binders, quantifier dependencies, degenerate cases, foundation policy, and
   checked transports for every credited alternate encoding.

## Degenerate and boundary cases

Source review must explicitly dispose of the empty and singleton index types; zero dimension; the
zero and identity matrices; diagonal, reducible, block-triangular, permutation, stochastic,
nilpotent, irreducible periodic, and primitive matrices; spectral radius zero; repeated Perron
roots; left versus right eigenvectors; normalization when the coordinate sum vanishes; and real
versus complex spectrum encodings.

No case is excluded at intake. A statement that assumes a Perron eigenvalue/eigenvector, a simple
dominant eigenvalue, or the desired spectral conclusion as structure data is circular rather than
a Perron-Frobenius theorem.

## Neighbor and substitution exclusions

- The out-of-scope physics record `THM-P-0887` states the narrower positive-matrix slogan "the
  largest eigenvalue is positive and simple." It exposes a scope distinction but cannot select or
  replace the nonnegative-matrix target.
- `THM-M-0043` concerns the spectral theorem for normal/self-adjoint operators, not entrywise order.
- `THM-M-0041` (Cayley-Hamilton), `THM-M-0042` (Jordan form), and `THM-M-0045` (Schur
  decomposition) may supply linear-algebra ingredients but do not prove the order-theoretic
  Perron conclusion.
- Gershgorin bounds, generic eigenvalue existence, generic spectral-radius attainment, stochastic
  matrix facts, and irreducibility/primitivity definitions alone are not substitutes.
- A theorem restricted to a fixed dimension, symmetric matrices, stochastic matrices, or a
  caller-provided positive eigenvector cannot replace the source-selected root.
- The repository's `verified` label and this intake probe supply no source or proof credit.

## Formal boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` defines
`Matrix.IsIrreducible` and `Matrix.IsPrimitive` and proves graph/power characterizations. It also
provides matrix-to-linear-map spectrum bridges, eigenvalue existence over algebraically closed
fields, and generic Banach-algebra spectral radius. The probe authenticates only these adjacent
interfaces. It does not define or prove a Perron eigenvector, positivity/simplicity at the spectral
radius, modulus dominance, or peripheral-spectrum classification. No canonical Lean target,
expression fingerprint, checked transport, mutation suite, or proof body is claimed at intake.
