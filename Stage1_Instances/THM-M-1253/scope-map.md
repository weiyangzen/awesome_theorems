# Scope map

## Included mathematical scope

- Schwartz distributions, understood as continuous linear functionals on compactly supported smooth
  test functions over a finite-dimensional real vector space (normally `R^n`).
- The standard convolution construction when at least one factor has compact support.
- The defining pairing suggested by
  `⟨S * T, φ⟩ = ⟨S_x, ⟨T_y, φ(x + y)⟩⟩`, with all continuity and support conditions made explicit.
- Closure as a distribution and the algebraic or differentiation laws that are actually part of
  the ultimately selected source statement.

## Decisions deferred to statement freeze

The repository source phrase does not determine whether the target is merely existence and
well-definedness, commutativity/associativity, a support bound, compatibility with derivatives, or
the larger convolution theory. The next phase must select an exact primary-source theorem and fix
the ambient space, real or complex scalars, topology on test functions, support hypothesis, binder
order, universes, normalization, and all degenerate cases. It must also decide whether mathlib has
a sufficiently concrete distribution API or whether prerequisite infrastructure is the blocker.

## Explicit exclusions

- Convolution of functions, measures, probability laws, or Schwartz functions as a substitute.
- An unrestricted claim that every pair of distributions can be convolved.
- Taking convolution or its desired laws as fields of an assumed structure.
- Using the manifest's untrusted `已验证` label as mathematical or machine-proof evidence.

