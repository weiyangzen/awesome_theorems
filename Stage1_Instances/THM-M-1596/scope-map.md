# Scope map

## Preserved scope

The intake preserves target `THM-M-1596`, the title `密码学`, and the literal gloss `现代密码学`
(`modern cryptography`). The attribution, twentieth-century date, importance, and `已验证` fields
are catalog metadata. Together they identify a broad discipline and do not choose one theorem.

## Candidate result families not credited

The label is compatible with many inequivalent propositions. None is selected or credited here:

1. Correctness of a source-selected encryption, signature, commitment, key-exchange, secret-sharing,
   or authentication construction.
2. Security of a primitive or protocol in a specified game under an exact computational or
   information-theoretic assumption.
3. A reduction constructing pseudorandom generators, functions, or permutations from a selected
   primitive, or constructing another primitive from them.
4. A zero-knowledge, secure-computation, chosen-ciphertext, or composability theorem in an exact
   interaction and corruption model.
5. An impossibility, lower-bound, equivalence, amplification, or generic-composition theorem.
6. Correctness or security of the separately cataloged RSA, Diffie-Hellman, elliptic-curve,
   zero-knowledge, or homomorphic-encryption topics.

## Decisions required at statement freeze

1. Select one immutable, truth-valued source proposition with edition, theorem/definition/page
   locator, incorporated definitions, proof boundary, correction record, and independent review.
2. Fix the primitive or protocol syntax and every algorithm: setup, key generation, encryption,
   decryption, signing, verification, interaction, simulation, or other source-specific operation.
3. Fix all message, key, randomness, state, transcript, oracle, language, witness, group, field, and
   output spaces, including encodings, length conventions, universes, and typeclasses.
4. Fix whether algorithms and adversaries are deterministic, randomized, uniform, or nonuniform;
   interactive or oracle-aided; exact machines, circuits, or abstract cost-bounded functions.
5. Fix the resource model: security parameter, time/space/query/randomness bounds, polynomial-time
   definition, auxiliary advice, concurrency, corruption, setup, and computational foundation.
6. Fix the experiment/game and all probability spaces, randomness independence, transcripts,
   success events, distinguishing advantage, absolute-value and normalization conventions.
7. Fix perfect, statistical, or computational security; concrete versus asymptotic bounds;
   negligible/non-negligible definitions; every constant and polynomial dependency; and quantifier
   order over parameters, schemes, adversaries, distinguishers, simulators, messages, and coins.
8. Separate functional correctness, completeness, soundness, privacy, authenticity, secrecy,
   extraction, simulation, robustness, and efficiency. State exactly which conclusion is the root.
9. Fix all hardness assumptions and reductions, their direction, loss, black-box or non-black-box
   boundary, uniformity, failure probability, and whether an existence assumption is conditional.
10. Resolve empty message/key/randomness spaces, zero security parameter, invalid keys or ciphertexts,
    decryption failure, malformed transcripts, adversary ties, zero queries, deterministic coins,
    negligible-function endpoints, and exact versus implementation arithmetic.

## Explicit exclusions

- Do not choose a standard theorem merely because it is famous or representative of modern
  cryptography, and do not replace the unidentified root with a definition or trivial round trip.
- Do not substitute `THM-M-1597` RSA, `THM-M-1598` Diffie-Hellman, `THM-M-1599` elliptic-curve
  cryptography, `THM-M-1600` zero knowledge, or `THM-M-1601` homomorphic encryption.
- Do not merge unrelated entries from the repository's computer-science cryptography survey into
  an omnibus conjunction or use that survey's statuses as evidence.
- Do not treat modular arithmetic, finite probability, Turing-machine complexity, entropy, hashing,
  group theory, or number-theory infrastructure as a cryptographic security theorem by itself.
- Do not encode the conclusion as a structure field, hypothesis, oracle, axiom, opaque predicate,
  simulator assumption, benchmark, sampled experiment, or unchecked computational result.
- Do not credit the catalog's `已验证` label, the discovery probe, or a bounded no-match search as
  source, statement, or proof evidence.

## Lean and trust boundary

Pinned mathlib supplies finite probability mass functions and abstract Turing-machine computability
and polynomial-time predicates. Those interfaces could support parts of some future encoding. They
do not supply cryptographic schemes, security games, negligible advantage, adversarial interaction,
or the unidentified root. Exact imports, expression and environment fingerprints, checked
transports, statement mutations, foundation and computation policies, exhaustive candidate audit,
obligation registry, proof architecture, and release evidence remain downstream work.
