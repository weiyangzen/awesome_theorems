# Scope map

## Included topic boundary

- A complex Hilbert space.
- A one-parameter group of unitary operators indexed by the additive real group.
- A source-specified continuity condition, expected to be strong (pointwise norm) continuity.
- A densely defined self-adjoint infinitesimal generator.
- The source-selected existence, uniqueness, exponential representation, converse, or full
  correspondence between these data.

## Decisions required at statement freeze

The repository gloss leaves materially different formulations compatible with its words:

1. **Group to generator:** every strongly continuous one-parameter unitary group has a unique
   self-adjoint generator `A`, with an equality such as `U(t) = exp(i t A)`.
2. **Generator to group:** a self-adjoint (generally unbounded) operator gives a strongly continuous
   unitary group through spectral/functional calculus.
3. **Full correspondence:** both directions, including uniqueness and inverse laws.
4. **Generator characterization:** the domain consists of vectors where the strong derivative at
   zero exists, with the operator recovered from that derivative.

The source must freeze whether continuity is stated for every vector or in an operator topology,
whether the group law is additive, whether the operator is self-adjoint or skew-adjoint, and
whether the convention is `exp(i t A)` or `exp(-i t A)`. It must also freeze equality of partial
operators, the derivative normalization, and all completeness/nontriviality assumptions.

## Explicit exclusions

- Stone-Weierstrass, Stone duality, Stone-Cech compactification, and Stone separation.
- The bounded self-adjoint exponential fact alone; Stone's generator may be unbounded.
- A theorem only about unitary matrices or finite-dimensional diagonalization.
- Hille-Yosida or Lumer-Phillips as a substitute for the unitary-group theorem.
- A definition of a generator followed by a tautological projection.
- The duplicate physics entry as a second theorem or as proof/source evidence.
- The inventory label `已验证` as human-proof or machine-proof evidence.

No canonical Lean target is frozen at intake because the inventory does not select one exact
formulation or supply a primary source passage.

