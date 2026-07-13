# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-0055`, the label `瑞利商定理`, John William Strutt
(Rayleigh), the year 1870, the gloss `Hermite矩阵特征值的变分刻画`, and an untrusted `已验证`
status. Intake preserves that finite-matrix eigenvalue variational theorem-family boundary. The
literal `Hermite` is not silently normalized to Hermitian, and the sparse record is not replaced by
a familiar maximum-eigenvalue, two-extrema, or indexed Courant-Fischer proposition.

## Proposition-changing decisions

An approved source decision must freeze all of the following before statement elaboration:

- whether `Hermite矩阵` means a complex Hermitian matrix, a real symmetric matrix, or another
  convention, and whether the Lean carrier is a square matrix or its self-adjoint endomorphism;
- complex scalars versus arbitrary `RCLike` scalars, the finite index type, nonemptiness,
  decidable equality, dimension and universe conventions;
- the Rayleigh quotient numerator: `xᴴ A x`, an inner product with a fixed argument order, or its
  real part; the squared-norm denominator; and exclusion or convention at the zero vector;
- whether competitors are nonzero vectors, unit vectors, one sphere, subspaces, or orthogonal
  complements, and the checked equivalences among any credited encodings;
- decreasing or increasing eigenvalue order, multiplicity, index origin, and the relationship
  between a matrix's eigenvalues and those of the associated linear map;
- whether the root asserts only maximum/largest equality, only minimum/smallest equality, both
  extrema, existence of extremizers, an iff description of extremizing eigenspaces, or all indexed
  min-max equalities;
- `max`/`min` with witnesses versus `iSup`/`iInf`, and the exact attainment and equality clauses;
  and
- every ordered binder, hypothesis, conclusion, typeclass argument, coercion, and degenerate case.

These choices yield materially different propositions. They are a resolution ledger, not a
canonical claim.

## Candidate families not credited

- For a nonempty finite complex Hermitian matrix, its largest and smallest eigenvalues are the
  maximum and minimum of `xᴴ A x / xᴴ x` over nonzero vectors.
- The same two-extrema result for an abstract finite-dimensional self-adjoint map over an `RCLike`
  scalar field.
- A one-sided result that the supremum or infimum of the Rayleigh quotient is an eigenvalue.
- An extremizer characterization saying maximizing and minimizing vectors are precisely vectors
  in the top and bottom eigenspaces.
- The full finite-dimensional Courant-Fischer indexed min-max theorem.
- A generalized Rayleigh quotient `xᴴ A x / xᴴ B x` with positive-definite `B`.

No family in this list is selected, conjoined, asserted, or credited at intake.

## Neighbor and substitution boundaries

- `THM-M-1390` separately names the Courant min-max principle. A full indexed subspace min-max
  theorem cannot be silently assigned here merely because a modern source presents the extreme
  cases and Courant-Fischer together; conversely, an extremal Rayleigh theorem cannot close that
  indexed target.
- `THM-M-0043` separately owns the spectral theorem. Existence of a sorted eigenvalue list or an
  eigenbasis is substrate, not a variational characterization.
- `THM-M-0053` Gershgorin, `THM-M-0054` Perron-Frobenius, `THM-M-0056` Weyl inequalities, and
  `THM-M-1450` power iteration are distinct spectral results and share no proof credit.
- A definition, homogeneity or boundedness property of the Rayleigh quotient alone is not the
  theorem.
- A result only saying an attained extremum is an eigenvector is not the value equality or complete
  extremizer characterization unless an approved source selects exactly that proposition.
- Normal or arbitrary nonsymmetric matrices, numerical eigenvalue solvers, Rayleigh iteration,
  floating-point samples, and unchecked optimization certificates cannot substitute for the root.
- A premise, structure field, or interface that assumes the desired extremal equality is not a
  proof, and the catalog label `已验证` supplies neither source nor kernel credit.

## Boundary cases

The statement phase must decide the empty (`0 x 0`) and singleton carriers; zero and scalar
matrices; repeated top or bottom eigenvalues; singular and indefinite Hermitian matrices; quotient
behavior at zero; whether the real-symmetric case is included by specialization; non-Hermitian and
merely normal matrices; maximum/minimum attainment; equality cases and full extremizing
eigenspaces; indexing at the first and last eigenvalues; and whether all intermediate eigenvalues
are explicitly out of scope or part of the selected root.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks the Rayleigh quotient,
nonzero-vector/sphere extrema transports, global-extremum eigenvectors, finite-dimensional
supremum/infimum eigenvalues, the Hermitian-to-symmetric map bridge, and decreasing finite
eigenvalues. These are unusually close formal candidates, so the machine status is provisionally
`M3`, but exact source selection, matrix transport, statement identity, minimal imports,
fingerprints, and mutations remain downstream work. The probe is discovery only, not the exhaustive
anchor audit and not proof of the target.
