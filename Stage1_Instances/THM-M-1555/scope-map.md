# Scope map

## Included theorem family

- A one-dimensional scalar second-order Schrodinger-type spectral equation on a real interval.
- A sufficiently regular seed solution at a distinguished factorization energy, nonzero on the
  domain where logarithmic derivative or division by the seed is used.
- A first-order Darboux transformation built from differentiation and the seed's logarithmic
  derivative.
- An intertwining identity between the original and transformed differential expressions, with
  the consequent map from an original solution to a transformed solution.
- A transformed potential determined by the seed, with its exact formula fixed only after source
  and sign conventions are selected.

## Decisions required at statement freeze

The statement phase must select and inspect one exact primary result and freeze: the interval or
local domain; real versus complex functions; classical, weak, or operator-theoretic solutions;
differentiability of the potential, seed, and input solution; the sign and normalization of the
second derivative; whether the equation is written as `H psi = lambda psi` or in another normal
form; factorization energy and input spectral parameter; whether they may coincide; the exact
first-order operator and transformed-potential formula; and whether the conclusion is an
intertwining identity, a solution transformation, a factorization, or all three.

Zeros of the seed, disconnected domains, endpoint conditions, identically zero inputs, singular
potentials, spectral multiplicity, self-adjoint operator domains, and invertibility/deletion or
creation of an eigenstate must be handled exactly as the selected source does. Binder order and
universes must follow those choices.

## Explicit exclusions

- Darboux's intermediate-value theorem for derivatives and Darboux's theorem in symplectic
  geometry; these share a name but are different scheduled mathematics.
- A Baecklund transformation, Crum's iterated transformation, supersymmetric quantum mechanics,
  or a multidimensional/matrix Darboux transformation as a substitute for the selected result.
- Merely defining the transformed potential or checking a single polynomial/example solution.
- Assuming the intertwining identity or transformed differential equation as a structure field.
- Treating the repository metadata value `已验证` as human-source or kernel evidence.

No canonical Lean expression is frozen at intake. A later statement must expose concrete
differentiation, potential multiplication, seed nonvanishing, spectral equations, and transformed
operator rather than encode the desired conclusion as a premise.
