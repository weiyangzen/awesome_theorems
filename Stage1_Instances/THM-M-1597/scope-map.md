# Scope map

## Preserved repository scope

The intake preserves target `THM-M-1597`, the title `RSA加密`, the literal gloss `公钥加密系统`,
the Rivest/Shamir/Adleman attribution, and the year 1977. The importance and `已验证` fields are
catalog metadata, not source-fidelity or Lean evidence. The record names a cryptosystem rather than
one exact proposition.

The primary paper makes the following result families plausible, but none is selected or credited:

- construct exponentiation-based encryption and decryption keys from two primes;
- prove that encryption followed by decryption, and decryption followed by encryption, recover
  every allowed message;
- prove correctness or authenticity properties of the paper's signature protocol;
- prove exact or asymptotic cost bounds for modular exponentiation, prime search, or key generation;
- relate recovery of a private key to factoring or another computational problem; and
- assert a modern security notion for a precisely padded, randomized RSA scheme.

## Decisions required at statement freeze

1. Admit and independently review an immutable source edition, and select an exact theorem passage
   rather than the catalog's system label.
2. Decide whether the root concerns construction, round-trip correctness, signatures, efficiency,
   one-wayness, a reduction, or security; do not combine these without source authority.
3. If selecting the Section VI correctness route, fix the carrier and ordered binders for primes
   `p`, `q`, exponents `e`, `d`, and message `M`; require the truth-critical distinctness or
   coprimality condition on `p` and `q`.
4. Fix the key equation and its orientation: the paper uses `e * d` congruent to `1` modulo
   `(p - 1) * (q - 1)`. Decide whether a Carmichael-function variant is an alternate encoding or a
   different target.
5. Fix message and ciphertext domains, whether exponentiation is explicitly reduced after each
   operation, and whether the result is equality in `Fin (p*q)`, `ZMod (p*q)`, or natural modular
   equality.
6. Map both inverse directions separately and decide whether the canonical conclusion is one
   direction, both directions, or that the maps form a permutation/equivalence.
7. If security or complexity is selected, fix the padding/randomization scheme, adversary model,
   experiment, security parameter, advantage, reduction, cost model, and exact or asymptotic bound.
8. Freeze minimal imports, expression and environment fingerprints, checked transports, foundation,
   TCB and computation profiles, all boundary cases, and the four required statement mutations.

## Truth-critical and boundary cases

- `p = q` is not harmless. The paper's totient product and CRT argument require distinct primes.
  For example, `p = q = 3`, `e*d = 5`, and `M = 2` satisfy the naive exponent congruence modulo
  `(p-1)(q-1) = 4`, but `2^5` is not congruent to `2` modulo `9`.
- The all-message correctness proof must include `M = 0`, `M = 1`, and messages divisible by `p` or
  `q`; a coprime-message Euler theorem is strictly weaker.
- The statement must settle `p`/`q` order, primes equal to `2`, zero or one exponents, modulus and
  message-range endpoints, representatives outside `[0,p*q)`, and encryption/decryption reductions.
- Modular inverse existence must not be smuggled in as a structure field or as the conclusion
  itself. The exact hypotheses on chosen keys must be source-mapped.
- An inverse-permutation correctness theorem does not imply confidentiality, chosen-ciphertext
  security, signature unforgeability, or implementation security.

## Excluded substitutions

- the separate Stage0 computer-science record `THM-C-0201 RSA正确性`;
- Euler/Fermat for bases coprime to the modulus, without the paper's non-coprime cases and CRT step;
- only one fixed numerical RSA example or a finite computation;
- a definition of RSA keys or encryption used as the requested theorem;
- OAEP, PKCS#1, PSS, randomized RSA, Rabin encryption, or another modern scheme;
- a factoring-hardness assumption, private-key recovery reduction, IND-CPA/IND-CCA result, or
  signature-unforgeability theorem used in place of correctness;
- benchmark, implementation, side-channel, or probabilistic-primality evidence used as mathematical
  correctness; and
- the catalog's `已验证` label or the discovery probe used as source or proof credit.

## Scope boundary

Intake freezes the unresolved choices and non-substitution rules only. It intentionally leaves the
canonical mathematical statement and Lean target null. Tree construction, proof search, debt
promotion, and theorem completion are outside this phase.
