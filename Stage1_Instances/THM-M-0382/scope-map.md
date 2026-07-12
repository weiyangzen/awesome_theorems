# Scope map

## Included topic boundary

- An abstract operator family `U(t)` from an energy/Hilbert space into spatial functions.
- The energy and time-separated dispersive estimates required by the selected Keel-Tao theorem.
- The exact admissibility relation on time-space exponent pairs, including the endpoint.
- Precisely the homogeneous, dual, and/or retarded spacetime estimates selected from the source.
- All time domains, measures, scalar fields, operator adjoints, constants, and completions used by
  that statement.

## Decisions required at statement freeze

The label can denote several related but non-identical claims. The next phase must decide from an
immutable source whether the canonical root is the entire abstract estimate package or one of its
components. It must freeze:

1. The source theorem/part and whether its conclusion includes homogeneous, dual, retarded, or all
   estimates.
2. The decay parameter `sigma`, admissible exponent equality/inequality and endpoint exclusions.
3. The energy space, the `L^1` to `L^infinity` dispersive interface, and whether `U(t)` is unitary,
   merely energy-bounded, or supplied with a separate adjoint family.
4. Global real time versus a finite interval, strong/Bochner measurability, almost-everywhere
   equality, iterated/mixed norm order, and interpretation of infinite exponents.
5. Whether the theorem claims a qualitative constant, its dependence, or a sharp value.

The zero function is harmless, but zero time separation, `sigma = 0`, the exceptional endpoint,
null spatial measure, and nonmeasurable operator orbits cannot be assigned conventions ad hoc.

## Explicit exclusions

- A non-endpoint Strichartz estimate as a substitute for the endpoint result.
- A PDE-specific Schrödinger or wave corollary unless the selected source claim is that corollary.
- The Christ-Kiselev lemma, Hardy-Littlewood-Sobolev inequality, or a bilinear interpolation lemma
  alone as the target.
- An abstract structure that assumes each desired estimate as a field and then projects it.
- Merely defining admissible exponents or mixed norms.
- The repository label `已验证`, a citation, or an API probe as human-proof or kernel-proof evidence.

No canonical Lean proposition is frozen during intake because the repository gloss does not select
the source theorem clauses or their boundary conventions.
