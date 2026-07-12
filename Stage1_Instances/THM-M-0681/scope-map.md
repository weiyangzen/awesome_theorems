# Scope map

## Included theorem family

- Ordinary differential fields of characteristic zero with one derivation.
- Existential closedness with respect to differential-field extensions, expressed directly or by a
  source-checked first-order equivalent.
- An explicit first-order axiom scheme stated using finite differential-polynomial conditions.
- Both directions: the axioms imply existential closedness and every existentially closed
  differential field satisfies the axioms.
- All side conditions used by the selected source, including nonzero inequations, differential
  order, initials/separants, or characteristic assumptions.

## Decisions required at statement freeze

The repository phrase does not identify an exact theorem. The statement phase must inspect the
primary text and determine whether the root is Robinson's original scheme or a later simplified
criterion. It must then freeze the language of differential rings, the definition of differential
field extension and existential closedness, the differential-polynomial representation, the number
of indeterminates, coefficient and parameter conventions, rankings/orders, side conditions, and
both implication directions. Any use of a modern Blum-style criterion needs a source crosswalk and
a checked bridge rather than an unsupported historical identification.

The intended field characteristic is zero and the derivation is ordinary (one derivation). These
boundaries follow the standard `DCF_0` setting but remain subject to confirmation against the
pinpointed source. The statement must expose rather than hide behavior for the zero derivation,
constant equations, empty or inconsistent systems, and vacuous side conditions.

## Explicit exclusions

- Defining a class `DifferentiallyClosed` by the desired axiom scheme and proving only `P ↔ P`.
- Algebraic closedness of the underlying field as a substitute for differential closedness.
- Existence of a differential closure, uniqueness of differential closures, model completeness,
  decidability, or quantifier elimination as a substitute root.
- Partial differential fields with several commuting derivations, difference fields, or positive
  characteristic unless the reviewed source explicitly selects them and the target is re-frozen.
- A finite collection of illustrative differential equations in place of the universal scheme.
- The repository label `已验证`, API availability, or successful `#check` output as proof evidence.

## Lean boundary at intake

Pinned mathlib represents a differential ring through `Differential` and its derivation, supports
`DifferentialAlgebra`, and has ordinary differential-field results. The scoped search did not find
a differential-polynomial type, an existentially-closed differential-field predicate, a `DCF_0`
theory, or a terminal axiomatization theorem. Consequently the exact Lean domain and proposition
remain open rather than being invented from ordinary polynomial APIs.
