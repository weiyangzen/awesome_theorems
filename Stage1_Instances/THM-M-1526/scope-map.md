# Scope map

## Included claim

- Flat spacetime with one explicitly selected metric signature and dimension.
- A concrete spinor space and gamma matrices satisfying the corresponding Clifford anticommutation
  relations.
- The free massive Dirac equation and the algebraic factorization obtained by composing the two
  conjugate first-order operators.
- The consequence that a sufficiently regular Dirac spinor solves the componentwise free
  Klein-Gordon equation.

## Decisions required in the statement phase

The selected primary source must control the signs, units (`c` and `hbar` or natural units), index
raising, complex scalar convention, mass domain, gamma representation independence, and ordering of
the two first-order factors. The formal target must also select a domain on which mixed partials
commute and operator composition is meaningful. It must state behavior at zero mass and any boundary
or compact-support assumptions rather than silently relying on physics notation.

## Explicit exclusions

- The Dirac equation as an empirical law or a definition with no mathematical conclusion.
- Curved-spacetime, electromagnetic-coupling, spectral, self-adjointness, or existence theory as a
  substitute for the scoped free flat-spacetime factorization.
- Merely proving a finite gamma-matrix identity without connecting it to the selected derivative
  semantics and solution implication.
- An abstract package containing the desired conclusion as a field.

The historical `S1_M_194.lean` is a discovery map only. Its candidate choices must be re-audited,
not inherited as the canonical target or proof evidence.
