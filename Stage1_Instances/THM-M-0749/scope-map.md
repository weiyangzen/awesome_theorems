# Scope map

## Preserved theorem family

The target is the Friedberg-Muchnik existence theorem from computability theory. The family has
these material components:

- two sets or predicates on the natural numbers;
- computable enumerability of both sets;
- Turing reducibility, not merely many-one or one-one reducibility;
- failure of reduction in both directions; and
- an existential conclusion producing the incomparable pair.

This incomparability implies that both degrees are noncomputable and below the complete c.e.
degree, yielding an affirmative solution of Post's problem. That consequence does not by itself
fix which statement is canonical or which transport to an intermediate-degree formulation is
credited.

## Decisions required at statement freeze

1. Pin and independently review immutable copies of the incorporated primary proof sources,
   including definitions, exact result locators, assumptions, proof boundaries, translations,
   corrections, and errata.
2. Decide whether the canonical witnesses are predicates, sets, characteristic partial functions,
   enumeration domains, or degrees, and compile all credited transports.
3. Fix the c.e. model and its relationship to mathlib `REPred`, including extensional equality and
   any decidability or coding instances.
4. Fix how a set is represented as an oracle partial function for mathlib `TuringReducible`; this
   bridge is proposition-critical and cannot be inferred from matching names.
5. Freeze ordered binders and the exact two nonreducibility conjuncts. Determine whether distinct
   witnesses, noncomputability, proper bounds below the complete c.e. degree, or degree notation
   are conclusions or derived consequences.
6. Resolve boundary cases: empty, finite, computable, equal, complementary, and complete c.e. sets;
   total versus partial characteristic encodings; and natural numbers versus positive integers.
7. Select the foundation, choice, quotient, extensionality, coding, and computation policies.

## Explicit exclusions

- Only the assertion that an intermediate c.e. Turing degree exists, without an approved checked
  relationship to the two-incomparable-witness theorem.
- The Kleene-Post theorem about incomparable unrestricted Turing degrees; c.e. witnesses are
  essential here.
- Incomparability under many-one, one-one, truth-table, weak, Medvedev, or another reducibility.
- Existence of noncomputable c.e. sets, simple sets, creative sets, or immune sets alone.
- Generic order-theoretic existence of incomparable elements in `TuringDegree` without proving
  that the representatives are c.e.
- A finite-injury or priority-method interface whose hypotheses already contain the desired sets,
  requirements, or nonreducibility conclusion.
- `TuringDegree.instPartialOrder`, `REPred`, or the untrusted `已验证` label presented as root proof
  evidence.

No canonical Lean target, checked alternate encoding, statement fingerprint, obligation registry,
discovery protocol, proof state, or completion claim is frozen at intake.
