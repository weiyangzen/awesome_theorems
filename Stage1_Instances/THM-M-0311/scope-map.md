# Scope map

## Included claim boundary

- A measure space with its almost-everywhere equality relation.
- Measurable scalar-valued functions whose squared norm is integrable.
- The resulting L^2 quotient equipped with its L^2 metric or norm.
- Completeness: every Cauchy sequence in that quotient converges to an element of the quotient.
- Real and complex scalar readings as candidates, subject to the selected source.

## Decisions required at statement freeze

The source statement must determine whether the theorem is formulated for real-valued functions,
complex-valued functions, or both; whether the measure is arbitrary, finite, or sigma-finite; and
whether L^2 is presented as equivalence classes, an abstract Hilbert space, or via convergence of
function representatives. Binder order, universes, measurability assumptions, and the convention
for the L^2 norm must follow that source.

The name "Riesz-Fischer theorem" is also used for the assertion that every square-summable sequence
is the Fourier-coefficient sequence of an L^2 function, with convergence in mean. The repository
gloss selects L^2 completeness, but the statement phase must decide whether this historical form is
the primary sourced theorem, an alternate encoding requiring checked implications, or out of scope.

Boundary cases to retain unless the source says otherwise include the zero measure, an empty
underlying type, infinite measure, and functions changed on null sets. No finiteness assumption may
be introduced merely to simplify formalization.

## Explicit exclusions

- Completeness of `ell2` or arbitrary Hilbert spaces as a substitute without a checked bridge to
  the source's function-space L^2.
- The Riesz representation theorem, Frechet-Riesz representation, Riesz lemma, or Riesz-Markov
  representation theorem.
- Completeness of raw pointwise functions without quotienting almost-everywhere equality.
- Only completeness of a finite-dimensional or finite-measure special case.
- A structure carrying a `CompleteSpace` field by assumption, or a tautological restatement of a
  pre-existing typeclass assumption.
- The metadata value `已验证` as human-source or kernel evidence.

No canonical Lean target or theorem-completion state is frozen by this intake.
