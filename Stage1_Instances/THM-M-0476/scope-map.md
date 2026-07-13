# Scope map

## Preserved theorem family

The catalog formula `(p-1)! congruent to -1 (mod p)` preserves the forward direction of Wilson's
theorem. Its conventional completion is:

> For every natural prime `p`, `(p - 1)!` is congruent to `-1` modulo `p`.

A canonical Lean target now represents the congruence as equality in `ZMod p`:

```text
forall p : Nat, p.Prime -> ((p - 1)! : ZMod p) = -1
```

This is the exact statement-phase expression. It is the conventional completion selected from the
catalog formula, not a claim that the catalog literally supplied the natural domain or prime
premise. Primary-source selection, premise mapping, correction or errata review, and independent
source approval remain open, so the human-source level remains `H1`.

## Frozen statement decisions

1. The modulus binder is `p : Nat`, followed by the explicit hypothesis `hp : p.Prime`.
2. Factorial is `Nat.factorial (p - 1)` and is cast into `ZMod p`.
3. Congruence is equality of residue classes, and `-1` is the additive inverse of one in `ZMod p`.
4. The root is only the displayed forward implication, not the converse or primality iff.
5. `p = 2` remains in scope. Zero, one, and composite moduli are outside the root only because they
   fail `p.Prime`; no odd-prime side condition is added.
6. The only credited alternate form uses `[Fact p.Prime]`; the checked witness is
   `Stage1Instances.THM_M_0476.wilsonTheoremTarget_iff_factTarget`.
7. Removed-prime, changed-domain, existential-binder, and composite-`p = 4` boundary mutations all
   elaborate distinctly. The boundary mutation is additionally kernel-refuted at `p = 4`.

## Related forms, not substitutes

- `ZMod.wilsons_lemma` has a typeclass premise `[Fact p.Prime]`; the statement module checks the
  exact `Iff` between that binder contract and the explicit `hp : p.Prime` target. It does not
  invoke or credit the proof-bearing declaration.
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

The canonical expression, its explicit serialization hash, primitive import set, environment
fingerprint, one checked binder transport, and mutation boundary are frozen in `statement.json`.
No primary-source acceptance, proof body, formal-anchor credit, obligation registry, audit
completion, or theorem completion is supplied by this statement phase.
