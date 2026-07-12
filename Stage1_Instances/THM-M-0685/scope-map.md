# Scope map

## Intended root

The repository phrase `PA的一致性证明` identifies the historical Gentzen consistency theorem but
not an exact formal proposition. The intended root is syntactic consistency of first-order Peano
arithmetic: contradiction is not derivable in a fixed, faithful calculus for PA. A source-approved
formulation must state both the object theory and the metatheory used to justify proof reduction.

## Included mathematical layers

- A recursive language and axiom presentation for first-order arithmetic.
- A concrete proof calculus and inductive/coded predicate for finite PA derivations.
- A contradiction formula or empty-sequent convention and the resulting consistency predicate.
- Transformation to the infinitary or otherwise normalized derivations used by the selected
  Gentzen presentation, including cut reduction.
- An ordinal assignment into a primitive-recursive notation system for ordinals below epsilon-zero.
- Strict descent of the assigned notation under reduction.
- The precise transfinite-induction or well-foundedness principle that rules out an infinite
  reduction sequence and yields consistency.
- A checked mapping from these syntactic definitions to the canonical human claim.

These are provisional scope nodes, not frozen obligations or accepted proof credit.

## Decisions required at statement freeze

1. Pin an inspected source edition and exact theorem/passage, plus a modern explicit reconstruction
   if needed to expose suppressed metatheoretic assumptions.
2. Choose PA's language, induction schema, logical axioms/rules, coding of proofs, and contradiction.
3. Decide whether consistency is expressed as `not Provable false`, absence of an empty-sequent
   derivation, or another checked-equivalent syntactic formulation.
4. Define the ordinal notation system and its comparison relation. Relate it explicitly, rather
   than by name, to mathlib's set-theoretic `Ordinal.epsilon 0` if that API is used.
5. Freeze the exact induction schema and base metatheory. Do not package well-foundedness as an
   unexplained assumption that already contains the hard part of Gentzen's theorem.
6. Fix every binder, universe, coding invariant, degenerate case, foundation principle, and import,
   then elaborate and mutation-test the exact Lean proposition.

## Explicit exclusions

- Semantic satisfiability of an arbitrary first-order theory as a substitute for syntactic PA
  consistency.
- Consistency inferred merely from Lean's built-in natural numbers modeling an informal list of PA
  axioms, unless a checked soundness bridge covers the selected object calculus and full schema.
- Simple consistency, omega-consistency, 1-consistency, reflection principles, and conservativity
  claims unless the source crosswalk proves the required relationship.
- Consistency of PRA, fragments `I Sigma_n`, second-order arithmetic, set theory, or Lean itself.
- The bare fact that epsilon-zero is an ordinal fixed point, without the notation system, reduction,
  descent, and induction argument.
- A theorem made tautological by assuming `Consistent PA`, `WellFounded reduction`, or the desired
  normalization conclusion as input.
- The untrusted manifest label `已验证` as either source or kernel evidence.

## Boundary cases

The statement phase must test deletion or weakening of the induction schema, changes of proof
calculus, alternate contradiction formulas, malformed derivation codes, zero-step reductions, and
notations at versus strictly below epsilon-zero. It must distinguish external well-foundedness in
Lean from the exact arithmetically expressible transfinite-induction strength claimed by the source.
