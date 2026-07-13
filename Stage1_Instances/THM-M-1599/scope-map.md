# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1599`, the title `椭圆曲线密码学`, the literal gloss
`基于椭圆曲线的密码`, the attribution Victor Miller/Neal Koblitz, and the year 1985. It does not
turn this subject label into a conjunction of everything commonly called elliptic-curve
cryptography. The importance and `已验证` fields are catalog metadata, not source-fidelity or Lean
evidence.

## Candidate result families not credited

1. Honest-output agreement for an elliptic-curve Diffie-Hellman protocol.
2. Encrypt/decrypt correctness for EC ElGamal or ECIES, including encoding and failure behavior.
3. Sign/verify correctness for ECDSA or another elliptic-curve signature scheme.
4. A reduction from a specified security experiment to ECDLP, CDH, DDH, or another assumption.
5. A mathematical theorem about point counts, subgroup order, primitive points, or resistance to a
   specified attack family used in parameter selection.
6. Correctness and complexity of point addition, doubling, scalar multiplication, point encoding,
   or subgroup validation.

These claims are not interchangeable. In particular, scalar multiplication commutes in an
additive group, but that generic identity is neither a full protocol specification nor a security
theorem.

## Proposition-changing decisions

An approved statement phase must freeze all of the following from one immutable source passage:

- the selected scheme or algorithm, exact theorem locator, incorporated definitions, proof
  boundary, corrections or errata, translation decisions, and independent review;
- correctness, security, hardness, complexity, construction, or parameter theorem as the root;
- finite field representation and characteristic, Weierstrass model and nonsingularity, point
  coordinate system, equality, point at infinity, and cofactor/subgroup conventions;
- base point, subgroup and its order, admissible scalar range and reduction, key generation, public-
  key validation, and exceptional or invalid points;
- message, plaintext, ciphertext, signature, nonce and randomness spaces, encoding/decoding,
  hash-to-field or hash-to-curve policy, serialization, rejection, and failure semantics;
- for correctness, the exact algorithms, preconditions, output relation, determinism/probability,
  and whether equality is literal, decoded, or distributional;
- for security, security parameter, adversary and oracle interfaces, experiment, advantage,
  resource/cost model, assumption, reduction loss, asymptotic quantifier order, and conclusion;
- mathematical versus executable specification, exact versus machine-integer or floating-point
  arithmetic, certificate policy, trusted computation, and side-channel scope; and
- every ordered binder, hypothesis, conclusion, universe, typeclass, alternate encoding, and logic
  or choice dependency.

## Boundary and degenerate cases

Source selection must explicitly resolve singular curves; characteristic two or three; empty or
trivial groups; identity or low-order base points; nonprime subgroup order; nontrivial cofactor;
zero, negative, oversized, or unreduced scalars; invalid public keys; the point at infinity;
malformed encodings; messages outside the encoding image; zero or repeated nonces; noninvertible
denominators; signature range failures; hash collisions or random-oracle idealization; and
probability spaces with empty support. None is excluded at intake.

## Neighbor and substitution exclusions

- `THM-M-1598` separately owns the general Diffie-Hellman key-exchange topic. An ECDH root cannot
  silently duplicate or borrow that target's future scope or evidence.
- `THM-M-1597` separately owns RSA encryption. RSA correctness or security supplies no target
  statement here.
- Stage0 computer-science item `THM-C-0203` separately names DSA/ECDSA correctness and is outside
  the 1546-target Stage1 set. It cannot select this target's root or donate status.
- EC group-law associativity, commutativity, point-counting, or scalar-action identities alone are
  mathematical substrate, not the unspecified cryptographic root.
- A concrete standard curve, toy curve, one fixed key exchange, test vector, or finite computation
  cannot replace a general source claim without source authority.
- A structure field, hypothesis, adversary oracle, unchecked certificate, simulation, benchmark,
  or empirical attack result that assumes or samples the conclusion is not a proof.
- The catalog label `已验证`, the discovery probe, and a bounded no-match search provide no source,
  statement, or proof credit.

## Lean and trust boundary

Pinned mathlib provides a generic Weierstrass-curve object model and an additive commutative group
on nonsingular projective points. It does not thereby select a finite field, cryptographic subgroup,
protocol, implementation, security experiment, adversary, complexity model, or theorem. Exact
imports, canonical expression and environment fingerprints, checked transports, mutation tests,
foundation/axiom/computation policy, discovery protocol, obligation registry, typed graphs, proof
architecture, and release evidence remain downstream work.
