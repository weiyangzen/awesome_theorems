# Scope map

## Preserved theorem family

The catalog formula `(p-1)! congruent to -1 (mod p)` preserves the forward direction of Wilson's
theorem. Its conventional completion is:

> For every natural prime `p`, `(p - 1)!` is congruent to `-1` modulo `p`.

A natural Lean candidate represents the congruence as equality in `ZMod p`:

```text
forall p : Nat, p.Prime -> ((p - 1)! : ZMod p) = -1
```

This is a candidate family boundary, not a frozen canonical expression. The catalog supplies no
primary source or explicit domain and hypothesis, so source review and the dependent statement gate
must approve those choices before statement credit.

## Decisions required at statement freeze

1. Admit and independently review an immutable primary or authoritative source passage, including
   its exact direction, definitions, assumptions, historical attribution, corrections, and errata.
2. Freeze `p : Nat` or another source-supported domain, the explicit premise `p.Prime`, ordered
   binders, and the conclusion's congruence representation.
3. Fix whether `-1` means the additive inverse of one in `ZMod p`, the natural residue `p - 1`, an
   integer congruence, or a divisibility statement, and check every credited transport.
4. Fix factorial as `Nat.factorial (p - 1)`, including the cast into the modular ring and the role
   of natural truncated subtraction.
5. Keep `p = 2` in scope and verify it. Record that `p = 0`, `p = 1`, and composite moduli lie
   outside the forward root only because they fail the prime premise.
6. Distinguish the catalog's forward implication from the converse and full primality
   characterization, especially the exceptional `n = 1` behavior.
7. Freeze foundation, TCB, computation, freshness, and ownership profiles, then perform the four
   required statement mutations before inspecting proof closure.

## Related forms, not substitutes

- `ZMod.wilsons_lemma` has a typeclass premise `[Fact p.Prime]`; a canonical root with an explicit
  `hp : p.Prime` needs a checked wrapper installing that fact.
- `Nat.ModEq p (p - 1)! (p - 1)` is a plausible natural congruence form. Its relationship to the
  `ZMod` equality requires a checked `Iff`; raw negative one is not a natural-number term.
- `Nat.prime_iff_fac_equiv_neg_one (h : n != 1)` is a stronger characterization with an explicit
  exceptional case. It cannot replace the displayed forward formula.
- `ZMod.prod_Ico_one_prime` is a finite-product form. Factorial-to-product normalization must be
  represented explicitly if it is credited.
- Divisibility of `(p - 1)! + 1` by `p`, integer `Int.ModEq`, remainder equality, and unit-product
  forms need checked transports and source mapping.

## Boundary and non-substitution rules

- `p = 2` is included; both sides are one in `ZMod 2`.
- The equality also happens to hold in the subsingleton ring `ZMod 1`, which is why the converse
  theorem needs `n != 1`. This accidental boundary truth does not remove the prime premise from
  the forward target.
- A composite example such as `p = 4` refutes an unrestricted-modulus reading.
- Fermat's little theorem, Euler's theorem, the Chinese remainder theorem, and other neighboring
  elementary-number-theory targets are not Wilson's theorem.
- A prime-only special case, a converse-only statement, or the stronger iff cannot be substituted
  for the exact selected direction.
- A structure, hypothesis, custom axiom, oracle, computation, or unchecked certificate containing
  the desired equality is circular and receives no proof credit.
- The catalog's `已验证` label, a theorem-name match, API output, and this discovery probe are not
  human-source or kernel-completion evidence.

No canonical expression, fingerprint, checked alternate transport, or proof body is frozen by this
intake. Those belong to dependency-ordered downstream phases.
