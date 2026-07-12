# Scope map

## Included topic boundary

- Recursively enumerable subsets of finite powers of the natural numbers.
- Diophantine subsets represented by existentially quantified natural-number witnesses and an
  integer-coefficient polynomial equation.
- A checked transport between the source definitions and the selected Lean encodings.
- The forward MRDP implication from recursive enumerability to Diophantine definability.

## Decisions required at statement freeze

1. Select the exact recursive-enumerability predicate: domain of a partial recursive function,
   range of a total computable enumeration, or an equivalent accepted formulation.
2. Select the finite-tuple representation and state whether the theorem is uniform in arity.
3. Decide whether "Diophantine" means one polynomial equation or a finite system, and whether
   variables range over `Nat` or `Int`.
4. Freeze the coefficient ring, witness index type, ordered binders, and all checked transports.
5. Treat arity zero, empty/full sets, and no-witness representations explicitly rather than
   silently imposing positivity assumptions.

## Explicit exclusions

- `Dioph.pow_dioph` alone: it supplies the historically decisive exponentiation ingredient, not
  the general recursively-enumerable-set theorem.
- Matiyasevich's Pell-equation characterization alone.
- The undecidability of Hilbert's tenth problem or nonexistence of a decision algorithm as a
  substitute; these require additional computability and reduction statements.
- The converse, that Diophantine sets are recursively enumerable, unless used as an explicitly
  separate equivalence transport.
- Diophantine approximation, algebraic geometry over arbitrary rings, or integer-solution variants
  without a checked equivalence to the selected natural-number formulation.
- An assumed MRDP hypothesis followed by a projection, or the repository label `已验证`, as proof.

No canonical Lean target is frozen at intake because the source record does not specify the exact
computability and Diophantine encodings.
