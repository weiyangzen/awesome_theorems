# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1600`, the title `零知识证明`, the literal gloss
`不泄露信息的证明` (a proof that leaks no information), the Goldwasser/Micali/Rackoff
attribution, and the year 1985. Importance and `已验证` are untrusted catalog metadata. The gloss
does not say which zero-knowledge definition or theorem is the root.

## Candidate roots not credited

The inspected GMR source makes at least these distinct roots plausible:

1. The Section 3.3 definition of perfect, statistical, or computational zero knowledge for a
   protocol, or the derived definition of a zero-knowledge proof system.
2. Section 5, Theorem 1: the displayed protocol is a perfectly zero-knowledge proof system for the
   quadratic-residuosity language `QR`.
3. Section 6, Theorem 2: the displayed protocol is a statistically zero-knowledge proof system for
   the quadratic-nonresiduosity language `QNR`.
4. A later existence result, such as the GMW all-NP result in the assumption-dependent form
   reported by GMR; its exact source statement and cryptographic assumptions require a separate
   audit.

A definition is not an existence theorem. `QR` and `QNR` are different languages with different
protocols and zero-knowledge strengths. The later GMW candidate is a distinct catalog item and
cannot be inferred from the GMR attribution and slogan.

## Decisions required at statement freeze

An approved source decision must fix all of the following:

- the exact definition or theorem, immutable edition, section/theorem/page locator, incorporated
  definitions, proof boundary, correction/errata disposition, and independent review;
- language over bit strings versus a witness relation, instance and auxiliary-input encoding,
  security parameter, and all ordered quantifiers;
- interactive protocol semantics, prover/verifier machine models, private randomness, message and
  transcript representation, termination, round bounds, and resource measure;
- proof versus argument, honest-verifier versus arbitrary malicious verifier, uniform versus
  nonuniform adversaries/simulators, and standalone versus auxiliary-input/composable setting;
- perfect equality, statistical distance, or computational indistinguishability, including the
  exact negligible bound and distinguisher model;
- expected versus strict polynomial time for the simulator, success/failure behavior, and the
  simulated view, including verifier coins, messages, state, and auxiliary input;
- completeness and soundness errors, amplification policy, knowledge-soundness or proof-of-
  knowledge clauses if any, and whether only the zero-knowledge property or the full proof-system
  conjunction is asserted; and
- if `QR` or `QNR` is selected, the integer encoding, unit/Jacobi-symbol predicates, number-theory
  conventions, protocol repetitions, modular-arithmetic witnesses, and exact conclusion.

## Boundary cases to resolve

- empty language, empty input, zero-length security parameter, malformed encodings, and empty
  auxiliary input;
- zero-round protocols, deterministic prover or verifier, zero random bits, nontermination, aborts,
  malformed messages, and transcript length outside the selected bound;
- completeness or soundness thresholds at `0` or `1`, sufficiently-large-input conventions, and
  strict versus non-strict negligible bounds;
- simulator failure or unbounded expected runtime, distinguishers that ignore or hard-wire input,
  and identical versus merely close distributions;
- honest-verifier versus malicious-verifier behavior, sequential/concurrent composition, and
  auxiliary information derived from prior interactions; and
- for number-theory roots, invalid moduli, nonunits, `x = 0` or `x = 1`, Jacobi-symbol boundaries,
  and repetition count zero.

## Excluded substitutions

- The slogan, GMR definition, or a structure containing the desired simulator presented as a
  proved zero-knowledge existence theorem.
- Completeness or soundness alone, simulator existence alone, or indistinguishability alone used
  as the full zero-knowledge proof-system conclusion.
- Honest-verifier zero knowledge substituted for malicious-verifier auxiliary-input zero knowledge.
- Perfect, statistical, and computational zero knowledge interchanged without checked implications
  in the selected direction.
- A fixed toy transcript, Schnorr/Sigma protocol, 3-color protocol, Fiat-Shamir transform,
  zk-SNARK/STARK, noninteractive, concurrent, or composable result substituted without source
  authority.
- The separate `THM-C-0181` GMR definition, `THM-C-0182` GMW theorem, or `THM-C-0183` 3-color target
  used to broaden this mathematical target or import their status.
- An oracle, random-oracle heuristic, experiment, simulation trace, unverified sampler, unchecked
  probabilistic computation, `sorry`, axiom, or the untrusted `已验证` label used as proof credit.

## Lean and trust boundary

Pinned mathlib provides generic languages, deterministic polynomial-time Turing-machine
computability, probability mass functions, and a superpolynomial-decay predicate whose module
documentation notes the cryptographic notion of negligible functions. The probe confirms only
those interfaces. It does not supply interactive probabilistic machines, verifier views,
computational indistinguishability, simulators, a zero-knowledge predicate, or either GMR theorem.
Exact imports, formal expression and environment fingerprints, transports, mutations, obligation
registry, discovery inventory, proof architecture, and trust/release evidence remain downstream.
