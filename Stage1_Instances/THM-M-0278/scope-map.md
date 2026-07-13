# Scope map

## Received theorem family

The repository fixes only the title "Riesz representation theorem," the attribution Frigyes Riesz,
the year 1909, and the gloss "representation of linear functionals on Hilbert spaces." This
recognizably points to the Fréchet-Riesz theorem: a continuous linear functional on a Hilbert space
is represented by inner product with a vector. That sentence is a family description, not the
frozen canonical proposition.

## Decisions required at statement freeze

An exact, source-reviewed statement must decide all of the following:

1. Whether the scalar field is `Real`, `Complex`, or a source-authorized common abstraction such as
   mathlib's `RCLike`.
2. Whether the carrier is called a Hilbert space directly or is represented by a normed additive
   commutative group with `InnerProductSpace` and `CompleteSpace` instances.
3. Whether "linear functional" means an everywhere-defined bounded/continuous functional and how
   it is bundled; an arbitrary algebraic functional would be a different and generally false claim.
4. The inner-product convention: whether the representative occurs in the first or second
   argument, including conjugation for complex scalars.
5. Whether the conclusion asserts existence only, existence and uniqueness, surjectivity of a
   canonical map, a linear/conjugate-linear equivalence, or also the norm identity.
6. The exact universe levels, ordered binders, typeclass assumptions, foundation profile, and every
   alternate encoding with a checked transport.
7. Whether the historical attribution and 1909 date refer to the same source proposition as the
   modern Fréchet-Riesz formulation selected for formalization.

These choices can change the proposition or its proof boundary. Intake does not choose among them.

## Boundary and degenerate cases

Source review must explicitly settle the zero Hilbert space, the zero functional, one-dimensional
spaces, real versus complex spaces, and nonseparable or infinite-dimensional spaces. It must also
state whether uniqueness follows from positive-definiteness and whether the norm equality is part
of the root or a corollary. No boundary case is excluded before the proposition is selected.

## Pinned formal candidate

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the direct import
`Mathlib.Analysis.InnerProductSpace.Dual` supplies:

- `InnerProductSpace.toDualMap`, the conjugate-linear isometric embedding
  `E -> StrongDual K E` induced by `x |-> (y |-> inner K x y)`;
- `InnerProductSpace.toDual`, the corresponding isometric equivalence when `E` is complete;
- `InnerProductSpace.toDual_apply_apply` and `InnerProductSpace.toDual_symm_apply`, the forward and
  inverse pointwise equations.

The module's own prose calls this the Fréchet-Riesz representation theorem. This is a strong M3
statement/interface candidate, not proof credit for an as-yet-unfrozen canonical source claim.

## Excluded substitutions

- The Riesz-Markov-Kakutani theorem representing positive functionals on continuous functions by
  measures.
- The Riesz-Fischer theorem or completeness of `L^2`.
- Riesz's lemma about proper closed subspaces of normed spaces.
- Riesz-Thorin interpolation, Riesz transforms, compact-operator spectral theorems, or the
  Fredholm alternative.
- A finite-dimensional coordinate-duality theorem used in place of the Hilbert-space theorem.
- A result only for real spaces or only for complex spaces unless the accepted source selects that
  scope and any broader/narrower relationship is checked.
- A structure or hypothesis that stores the representing vector or surjectivity as assumed data.
- The catalogue's untrusted verified label, the mathlib theorem name, or this intake probe used as
  source identity or proof credit.
