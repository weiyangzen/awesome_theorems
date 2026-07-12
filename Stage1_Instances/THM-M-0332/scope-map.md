# Scope map

## Included topic boundary

- A complex unital Banach algebra (or a source-explicit admissible variant), an element `a`, and its
  algebraic spectrum.
- A function holomorphic on an open neighborhood of `spectrum(a)`.
- The source-defined holomorphic functional calculus value `f(a)`.
- The equality `spectrum(f(a)) = f '' spectrum(a)`, with every binder, typeclass hypothesis, and
  side condition taken from one inspected source.

## Decisions required at statement freeze

The source phase must freeze the scalar field, unitality, completeness and commutativity
assumptions; whether `a` is an algebra element or bounded operator; the exact notion and domain of
holomorphicity; the definition of functional calculus; and equality versus one-sided inclusion.
It must also resolve the zero algebra, empty spectrum, constant functions, disconnected
neighborhoods, and any nonunital/unitization convention.

## Explicit exclusions

- The polynomial spectral mapping theorem alone.
- The continuous functional calculus for normal elements of C-star algebras alone.
- The spectral mapping theorem for operator exponentials, semigroups, resolvents, or bounded
  algebra homomorphisms as substitutes.
- A weakened inclusion where the source claim is equality.
- Defining an assumed operation with spectral mapping as a field and projecting that field.
- Treating the inventory label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake. The nearby checked APIs in `IntakeProbe.lean` are
scope landmarks and feasibility evidence only.
