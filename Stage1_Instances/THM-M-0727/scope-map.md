# Scope map

## Included discovery boundary

- Languages over a source-selected alphabet, with an exact input encoding and size measure.
- An interactive protocol with explicitly modeled prover, verifier, messages, transcript, private or
  public coins, acceptance event, and adversarial prover quantification.
- Source-selected verifier time, prover power, round/message bounds, uniformity, and oracle policy.
- Explicit completeness and soundness probabilities, including strictness, amplification, and
  perfect-completeness conventions.
- A definition, protocol theorem, closure result, characterization, or complexity-class equality
  only if an immutable source later states that exact proposition.

These are candidate surfaces for source disambiguation, not a frozen root theorem.

## Ambiguities blocking statement freeze

The repository record does not determine:

1. whether the target is a definition of an interactive proof, the class `IP`, a protocol result,
   a closure theorem, or some other proposition;
2. public-coin versus private-coin protocols, number of provers, message schedule, or adaptivity;
3. probabilistic Turing machines, circuits, oracle machines, or another party model;
4. polynomial-time and uniformity restrictions on the verifier, and computational restrictions (if
   any) on the prover;
5. completeness and soundness thresholds, perfect completeness, amplification, or small-input rules;
6. the quantified languages, inputs, protocols, provers, random tapes, bounds, and conclusion.

These choices change the domains, binder order, hypotheses, boundary cases, and result. Merely
defining a protocol structure and proving a projection from its fields would not identify the
repository theorem.

## Explicit exclusions

- The adjacent `THM-M-0728` claim `IP = PSPACE` as a silent replacement.
- Zero-knowledge interactive proofs, multi-prover systems, PCP, Fiat-Shamir, or cryptographic
  proof/argument systems unless the selected immutable statement explicitly requires them.
- A convenient finite protocol example, identity interaction, definition-only declaration,
  tautological wrapper, assumed completeness/soundness, or weakened special case as the root.
- Generic language, deterministic time, or probability APIs as evidence that interactive proofs
  are already formalized.
- The untrusted inventory label `verified` as evidence of human or kernel closure.

No domain, universe, quantifier, hypothesis, conclusion, alternate encoding, or boundary case is
frozen because the source metadata contains no proposition.
