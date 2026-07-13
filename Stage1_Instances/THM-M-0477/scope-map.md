# Scope map

## Preserved catalog scope

The intake preserves the repository title `中国剩余定理` and its exact gloss
`同余方程组的解法`. This identifies the classical Chinese-remainder family concerning simultaneous
congruences. It does not itself assert one truth-valued proposition. The attribution, approximate
date, importance, and `已验证` field remain catalog metadata only.

A later statement may be selected only by an accountable source decision and independent review.
The source decision must first distinguish the historical Sunzi numerical residue problem or
method from a later general CRT proposition. Plausible mathematical components, none credited as
the canonical claim at intake, include:

- a source-selected collection of residues and moduli, finite or otherwise explicitly delimited;
- a compatibility or pairwise-coprimality premise on the moduli and residues;
- existence of a simultaneous solution;
- uniqueness modulo an lcm or product; and
- optionally, a distinguished representative in a bounded range or an explicit construction.

## Proposition-changing decisions

The statement phase must settle all of the following before elaborating a root target:

1. Select an immutable primary or authoritative source edition, exact result and definition
   locators, proof boundary, translation, correction and errata disposition, and independent
   source review.
2. Decide whether the root is a formal rendering of the historical Sunzi problem/algorithm, a
   modern elementary CRT, or another explicitly sourced result. Historical attribution does not
   make these propositionally identical.
3. Fix the carriers: natural-number congruence, integer congruence, `ZMod`, quotient rings, or
   another source-defined setting. For integers, fix modulus sign and normalization. These
   encodings have different binders and boundary behavior.
4. Fix whether the system contains exactly two congruences, a list or multiset, a finset, an
   arbitrary finite indexed family, or a potentially infinite/locally finite family, including
   duplicate-index semantics and ordering relevance.
5. Fix the modulus hypotheses: pairwise coprime, merely nonzero, strictly greater than one, or the
   general compatibility condition that residues agree modulo pairwise gcds.
6. Fix the conclusion: existence only, construction of a solution, uniqueness modulo an lcm or
   product, existence of a unique residue class, a bounded least representative, or a conjunction
   of these claims.
7. Fix the quantifier order and whether residues are reduced modulo their moduli or may be arbitrary
   representatives.
8. Freeze all universes, types, typeclasses, namespaces, implicit and explicit binders, minimal
   imports, foundation/TCB/computation profiles, and checked transports between credited forms.

The coprime finite-family existence theorem is familiar, but choosing it now would add assumptions
and a conclusion not present in the repository wording. The compatible two-modulus theorem is more
general in one direction and narrower in family size. Neither may silently become the root.

## Boundary and mutation cases

Statement review must explicitly resolve:

- an empty system, whose product convention and solution set may make the conclusion vacuous;
- a singleton system and repeated indices or repeated moduli;
- modulus zero, whose `Nat.ModEq` interpretation differs from ordinary positive-modulus prose;
- modulus one, negative integer moduli, modulus normalization, zero residues, residues outside a
  canonical interval, and negative integer residues;
- pairwise-coprime moduli containing zero, including the exceptional coprime pairs involving one;
- incompatible residues when moduli are not coprime;
- whether uniqueness is equality of representatives or congruence modulo a product or lcm; and
- whether the claimed solver is constructive data or only propositional existence.

Later statement mutations must cover a removed compatibility/coprimality premise, a changed
carrier, a changed binder or family scope, and relevant zero/unit/empty boundary cases. Intake does
not predeclare any of these mutations equivalent or exclude any case.

## Explicit non-substitutions

- Do not replace a system-of-congruences theorem with only the ring isomorphism
  `ZMod (m * n) ≃+* ZMod m × ZMod n` without a source-approved and checked transport.
- Do not replace the received elementary-number-theory family with the broader theorem for
  pairwise coprime ideals in an arbitrary commutative ring.
- Do not silently replace the historical Sunzi problem or constructive method with the strongest
  later arbitrary-family existence-and-uniqueness theorem, or conversely.
- Do not substitute only Bezout's identity, Euler's theorem, modular inversion, Garner's algorithm,
  an RSA recombination step, or a numerical example for the complete root claim.
- Do not weaken a finite-family claim to two moduli, strengthen a compatibility claim to coprime
  moduli, or add uniqueness/boundedness merely because a pinned API exposes that shape.
- Do not encode the desired conclusion as an axiom, opaque premise, structure field, certificate,
  or hypothesis.
- Do not treat the catalog label `已验证`, a theorem name, module documentation, or a successful
  API probe as human-source identity, statement identity, or proof completion.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Data.Nat.ModEq` exposes two-congruence compatible and coprime constructions plus
boundedness and uniqueness interfaces. `Mathlib.Data.Nat.ChineseRemainder` exposes list, multiset,
and finset constructions, while `Mathlib.Data.ZMod.Basic` exposes a ring-equivalence form.

These are direct exact-topic candidates, not a canonical source transport or an exhaustive anchor
audit. Minimal-import certification for a selected root, expression and environment fingerprints,
checked transports, mutations, terminal-body provenance, dependency and axiom closure, and trust
acceptance remain downstream.
