# Scope map

## Included claim

- Domain: an arbitrary number field `K`, meaning a finite extension of the rational numbers.
- Object: its ring of integers `O_K`, and the ideal class group `Cl(O_K)`, equivalently nonzero
  fractional ideals modulo principal fractional ideals.
- Conclusion: the underlying set of `Cl(O_K)` is finite.
- Quantification: the claim is uniform in `K`; it does not fix a degree, signature, discriminant,
  or chosen embedding.

The intended Lean normalization to investigate in the statement phase is
`Finite (ClassGroup (NumberField.RingOfIntegers K))`, with `[Field K] [NumberField K]` and the
universe made explicit. `Fintype` is a stronger data-bearing presentation and may be used only
through a checked transport to the source-level `Finite` claim.

## Boundary cases

- `K = Q` is included; its trivial class group is not the whole theorem.
- Class number one is included but is not assumed.
- All finite degrees and all archimedean signatures are included.
- No effectiveness, explicit class-number bound, class-number formula, or ideal representative
  enumeration is asserted.

## Explicit exclusions

- Finiteness of class groups of arbitrary Dedekind domains.
- Finiteness of ray, narrow, divisor, function-field, or scheme class groups.
- Positivity or computation of the class number, principality criteria, and unique factorization.
- Treating the legacy wrapper or an inferred typeclass as accepted rev-5.6 proof evidence.

The next phase must freeze ordered Lean binders, exact imports, declaration/expression,
environment fingerprint, transports between `Finite` and `Fintype`, and mutations of the
number-field and ring-of-integers hypotheses.
