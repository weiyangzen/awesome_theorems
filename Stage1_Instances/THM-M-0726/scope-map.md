# Scope map

## Included discovery boundary

- Languages over a source-selected finite alphabet and an exact input encoding and size measure.
- A source-selected randomized computation model, its random-bit distribution, and acceptance
  semantics.
- Polynomial running time under an explicit worst-case or expected-time convention.
- Bounded two-sided error (BPP), one-sided error (RP/coRP), and zero-error randomized polynomial
  time (ZPP), only after their exact thresholds and machine semantics are frozen.
- A definition, containment, equality, closure, amplification, or derandomization result only if an
  immutable source later states that exact proposition.

These are candidate surfaces for source disambiguation, not a frozen root theorem.

## Ambiguities blocking statement freeze

The repository record does not determine:

1. probabilistic Turing machines, deterministic machines with random tapes, probabilistic programs,
   circuits, or another randomized model;
2. uniform random bits, a general sampler, rational transition probabilities, or an oracle;
3. worst-case polynomial time on every random tape, expected polynomial time, or a halting-tail
   condition;
4. exact error thresholds, strictness at the threshold, amplification, and small-input exceptions;
5. whether the target is a definition, closure property, inclusion such as `ZPP subset RP`, an
   equality characterization, or another theorem;
6. the quantified languages, machines, polynomials, witnesses, and actual conclusion.

These choices change the domains, binder order, hypotheses, degenerate cases, and result. Packaging
chosen definitions and projecting an assumed inclusion would not identify the repository theorem.

## Explicit exclusions

- Adjacent targets concerning polynomial hierarchy, PSPACE, interactive proofs, IP=PSPACE, PCP, or
  derandomization as silent replacements.
- Open or conditional relations such as `P = BPP` unless an exact source explicitly selects a
  conditional proposition.
- A convenient finite probability example, identity-machine example, definition-only declaration,
  tautological wrapper, assumed class relation, or weakened special case as the root.
- The availability of deterministic polynomial-time or PMF APIs as evidence that randomized
  complexity classes are already formalized.
- The untrusted inventory label `verified` as evidence of human or kernel closure.

No domain, universe, quantifier, hypothesis, conclusion, alternate encoding, or boundary case is
frozen because the source metadata contains no proposition.
