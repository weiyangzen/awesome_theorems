# Scope map

## Included discovery boundary

- The classical complexity-theoretic PCP theorem represented in the repository by
  `NP = PCP[O(log n), O(1)]`.
- Languages over a source-selected finite input alphabet and their exact encodings and size measure.
- Polynomial-time randomized verifiers with random access to a source-selected proof-oracle model.
- Completeness and soundness probabilities, randomness complexity, and query complexity under the
  exact conventions selected from an immutable source.
- Both class inclusions needed for equality, including the easy encoding direction, without
  counting notation or a definitional equality as proof of either inclusion.

These are the intended source-discovery surfaces, not a frozen Lean proposition.

## Ambiguities blocking statement freeze

The repository shorthand does not determine:

1. the Turing-machine, RAM, circuit, or other model used for polynomial-time verification;
2. proof alphabet, finite or infinite oracle representation, and random-access semantics;
3. adaptive or nonadaptive query access and whether repeated positions count again;
4. whether `O(log n)` counts random bits, random strings, or another resource and which size/cost
   convention witnesses the asymptotic bound;
5. whether `O(1)` is a uniform constant bound for all inputs or an eventual asymptotic bound;
6. perfect or bounded completeness and the exact soundness constant (often normalized by
   amplification, but not definitionally interchangeable);
7. behavior on small, empty, malformed, or verifier-nonterminating inputs;
8. the exact ordered quantifiers over languages, verifiers, proofs, randomness, constants, and
   sufficiently large input sizes.

These choices change the target. They must come from the selected source and be reflected in Lean
before statement closure or mutation testing is possible.

## Explicit exclusions

- The quantum PCP conjecture, multiprover or interactive-PCP variants, MIP results, and Dinur's
  later combinatorial proof as substitutes for this target.
- Consequences for MAX-SNP, gap problems, hardness of approximation, or a particular CSP as the
  root theorem.
- The adjacent interactive-proofs and `IP = PSPACE` targets.
- A definition of `PCP` followed by a tautological restatement or an assumed class equality.
- A weakened one-language, fixed-size, finite-sample, or verifier-only example.
- The repository label `已验证` as human-proof or kernel-proof evidence.

No canonical domains, binders, hypotheses, alternate encodings, or degenerate cases are frozen at
intake because the repository sources do not supply the definitions needed to expand the shorthand.
