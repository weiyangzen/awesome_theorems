# Scope map

## Preserved catalog boundary

The intake preserves target `THM-M-1598`, title `Diffie-Hellman密钥交换`, attribution to Diffie
and Hellman, year 1976, and gloss `公钥密码学的开创`. Importance `high` and status `已验证` are
catalog metadata, not source or kernel evidence. The gloss identifies historical subject matter but
does not determine a theorem.

## Candidate interpretations not credited

1. **Algebraic agreement:** for a selected commutative/cyclic group and exponents `a,b`, both
   exponentiation orders yield the same group element.
2. **Protocol correctness:** after validating parameters/public keys and running a specified
   finite-field or elliptic-curve DH primitive, both honest parties output the same non-error shared
   secret or derived keying material.
3. **Passive security:** an eavesdropper cannot recover or distinguish the established key under a
   precisely stated discrete-log, computational Diffie-Hellman, or decisional Diffie-Hellman
   assumption.
4. **Authenticated key agreement:** a named authenticated protocol satisfies a specified security
   game against active attackers, including impersonation and man-in-the-middle behavior.
5. **Implementation correctness:** a concrete modular-exponentiation, validation, encoding, and
   key-derivation implementation refines one selected protocol specification.

None is selected or credited at intake. Agreement is not secrecy; passive secrecy is not active
authentication; an implementation trace is not a general security theorem.

## Proposition-changing decisions

A statement phase may proceed only after an immutable source and independent review fix:

- the exact paper/standard, edition, section/result, incorporated definitions, proof or argument
  boundary, corrections, and whether the canonical target is historical or modern;
- finite-field multiplicative groups, an abstract cyclic group, elliptic curves, or another domain;
- public domain parameters, generator/subgroup order, prime and safe-prime conditions, cofactor,
  public-key validation, and representation/encoding conventions;
- secret-exponent domain and distribution, ephemeral/static keys, randomness, reuse, erasure, and
  compromise model;
- the exact transcript, roles, public values, shared-secret computation, error behavior, key-
  derivation function, context binding, and key confirmation;
- correctness alone versus a security experiment, and for security: adversary interface, oracle
  queries, authentication, freshness, corruption, advantage, security parameter, asymptotics, and
  the precise hardness assumption;
- whether equality is mathematical equality of group elements or equality after serialization and
  key derivation; and
- ordered binders, universes, typeclasses, all hypotheses, conclusion, alternate encodings, and
  transport directions.

## Degenerate and adversarial cases to resolve

- trivial or singleton groups, generator `1`, subgroup order zero/one, invalid/non-prime modulus,
  and malformed or nonmember public keys;
- exponents zero, one, out of range, reused, biased, exposed, or adversarially chosen;
- shared value `0`, `1`, or `p - 1`, small-subgroup and invalid-curve inputs, cofactor behavior, and
  rejection versus continuation;
- equal parties/keys, reflection, replay, unknown-key-share, key-compromise impersonation, and
  unauthenticated active man-in-the-middle attacks;
- empty or colliding encodings, key-derivation failure, missing context/identity binding, and random-
  oracle versus standard-model choices; and
- exact arithmetic versus bounded machine integers, side channels, fault behavior, and secret
  erasure.

No degenerate case is excluded before a proposition is selected.

## Explicit non-substitutions

- The identity `(g^a)^b = g^(a*b) = g^(b*a) = (g^b)^a` alone as the entire key-agreement target.
- A record or hypothesis that already stores equal shared keys, followed by projection of equality.
- Discrete-log, CDH, or DDH hardness assumed in a form that directly assumes the desired security
  conclusion.
- Security against an active man-in-the-middle attacker for unauthenticated basic DH.
- RSA, elliptic-curve cryptography generally, zero-knowledge proofs, or generic cryptography as a
  substitute for this target.
- A fixed numerical test vector, probabilistic simulation, benchmark, executable output, or
  unchecked solver/certificate.
- Generic group/cyclic APIs, the catalog's `已验证` label, or this intake probe as theorem evidence.
