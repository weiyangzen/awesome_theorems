# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1601`, the title `同态加密`, the literal gloss `密文上的计算`
(`computation on ciphertexts`), the attribution to Craig Gentry, and the year 2009. The importance
and `已验证` fields are catalog metadata, not source-fidelity or Lean evidence. The gloss names a
cryptographic capability, not one truth-valued statement.

## Candidate result families not credited

Gentry's 2009 STOC paper makes the following distinct roots plausible. None is selected or credited
by this intake:

1. Define correctness of `Evaluate`: decrypting the evaluated ciphertext yields the circuit applied
   to the plaintext inputs for every permitted circuit and valid key/encryption execution.
2. Define a scheme as homomorphic for a circuit class, or fully homomorphic for all circuits, with
   compact ciphertext size and decryption time.
3. Prove the bootstrapping theorem: a scheme bootstrappable for a gate set yields a leveled fully
   homomorphic family for circuits over those gates.
4. Prove correctness of the paper's ideal-lattice encryption scheme for its permitted circuit set.
5. Prove that the modified scheme `E3` is bootstrappable under the stated parameter inequality and
   combine this with bootstrapping and security assumptions to construct FHE.
6. Formalize a modern existence, security-reduction, compactness, noise-growth, or concrete-scheme
   theorem rather than a claim from the 2009 paper.

These claims are not interchangeable. In particular, operation preservation is only vocabulary for
a correctness diagram, while full homomorphism also quantifies over a circuit class and carries
algorithmic and compactness conditions; it is often paired with, but does not itself entail, a
security condition.

## Proposition-changing decisions

An approved statement phase must freeze all of the following from one immutable source passage:

- the selected theorem, version, theorem/equation/page locator, incorporated definitions, proof
  boundary, errata decision, and independent review;
- public-key versus secret-key encryption; security parameter; key, message, randomness, ciphertext,
  and failure types; and the exact `KeyGen`, `Encrypt`, `Evaluate`, and `Decrypt` interfaces;
- deterministic versus randomized algorithms, the probability space over keys and coins, perfect
  versus negligible-error correctness, and quantifier order;
- circuit representation, gate basis, fan-in, input arity, size and depth measures, permitted
  circuit family, uniformity, and evaluation of malformed or out-of-class circuits;
- single-key versus multi-key evaluation, public evaluation data, evaluation keys, key-dependent
  messages, and whether fresh and evaluated ciphertexts share a distribution;
- full versus leveled homomorphism, the depth parameter and its encoding, and all fixed-versus-
  varying asymptotic parameters;
- compactness: which ciphertext-size and decryption-time bounds are independent of circuit size or
  depth and the exact computational cost model;
- security notion, adversary model, oracle access, advantage, hardness assumptions, reductions, and
  whether a result is conditional; and
- the precise relationship among correctness, homomorphism, semantic security, bootstrappability,
  squashed decryption, and the final construction.

## Boundary cases to resolve

- zero security parameter, empty key/message/ciphertext types, failed key generation, malformed
  ciphertexts, encryption failure, decryption failure, and invalid evaluation keys;
- zero-input circuits, identity and constant circuits, empty gate sets, unsupported gates, fan-in
  zero, depth zero, size zero, and ill-typed or cyclic circuits;
- no ciphertext inputs, mismatched keys or arities, randomized evaluation, evaluation failure, and
  equality versus distributional correctness;
- additive-only, multiplicative-only, bounded-degree, shallow, somewhat, leveled, and fully
  homomorphic circuit classes;
- strict versus non-strict noise/parameter inequalities, noise overflow, bootstrapping at the exact
  depth boundary, and circuit-depth encoding; and
- perfect versus negligible-error correctness, finite versus asymptotic claims, and uniform versus
  nonuniform adversaries or circuit families.

## Excluded substitutions

- Defining a homomorphic encryption interface whose correctness is assumed as a structure field.
- Proving only `map_add`, `map_mul`, a `RingHom`, or a commuting diagram with no encryption scheme.
- Proving a toy Caesar, RSA, ElGamal, additive-only, multiplicative-only, or fixed-circuit example as
  the general fully homomorphic result.
- Treating correctness for one permitted circuit class as full or compact homomorphism.
- Treating an executable test, random experiment, benchmark, oracle, or floating-point estimate as
  a universally quantified correctness or security proof.
- Selecting a later FHE construction or theorem merely because it is easier to formalize.
- Using the separate Stage0 computer-science item `THM-C-0210` to change this target's claim, formal
  system, status, or evidence.
- Using the catalog label `已验证` as a primary source or proof receipt.

## Lean and trust boundary

Pinned mathlib provides `RingHom`, `map_add`, `map_mul`, `Function.Semiconj`, and
`Function.Semiconj₂`. Those APIs can express operation preservation or a correctness diagram. They
do not define encryption algorithms, circuit semantics, compactness, security, bootstrapping, or an
exact source root. Exact imports, expression and environment fingerprints, checked transports,
mutation tests, foundation and axiom policies, obligation registry, discovery inventory, proof
architecture, and release evidence remain downstream work.
