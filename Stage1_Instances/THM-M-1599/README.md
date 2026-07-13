# THM-M-1599 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label
`椭圆曲线密码学` (elliptic-curve cryptography). The repository supplies only the gloss
`基于椭圆曲线的密码` (cryptography based on elliptic curves), an attribution to Victor Miller
and Neal Koblitz, the year 1985, and an untrusted `已验证` label. These fields name a
cryptographic subject and construction family, not a truth-valued proposition with ordered
binders, hypotheses, and a conclusion.

## Intake result

Miller's original paper *Use of Elliptic Curves in Cryptography* and the bibliographic record for
Koblitz's *Elliptic curve cryptosystems* were inspected as primary source-family leads. They discuss
elliptic analogues of public-key systems, key exchange, discrete logarithms, efficiency, parameter
selection, implementation, and security heuristics or assumptions. The catalog cites no passage
and does not select protocol correctness, a security reduction, an algorithmic result, or a group-
theoretic lemma as its root.

This intake therefore does not silently replace the label by ECDH agreement, EC ElGamal
correctness, ECDSA correctness, ECIES correctness/security, hardness of the elliptic-curve discrete
logarithm problem, or the elliptic-curve group law. These are different claims with materially
different definitions and assumptions.

## Formal boundary

Pinned mathlib supplies Weierstrass curves, ellipticity, projective points, and an additive
commutative group instance. `IntakeProbe.lean` authenticates only those generic APIs and reports the
instance's axioms. A bounded search found no elliptic-curve cryptosystem, ECDH, ECDSA, encryption,
or discrete-logarithm API in pinned mathlib. These are discovery observations, not an exhaustive
anchor audit, and the probe grants no target proof credit.

The provisional vector is `[H5, M4, R4]`. `H5` classifies the received catalog label as not yet a
stable proposition; it does not say that correctly stated elliptic-curve cryptography results are
false or open. No usable exact formal artifact or proof reconstruction can be credited before a
root exists. All six downstream phases remain open. No canonical statement, H0, M0, R0, accepted
proof state, audit completion, theorem completion, accepted receipt, or master acceptance is
claimed.
