# Scope map

## Preserved theorem family

The intake preserves the catalog's quadratic-reciprocity family: for odd primes, the quadratic
residue status of one prime modulo the other is reciprocal, with a sign change precisely in the
both-congruent-to-3-modulo-4 case. This sentence is a scope description, not a frozen canonical
proposition.

A conventional distinct-prime product form is

```text
(q / p) * (p / q) = (-1)^(((p - 1) / 2) * ((q - 1) / 2)),
```

where `(a / p)` is the Legendre symbol. An equality form, the mod-4 case split, and a
residue/nonresidue formulation can encode closely related mathematics, but they require an
approved source mapping and checked transports before any receives target credit.

## Decisions required at statement freeze

1. Choose an immutable source proposition and incorporated definitions rather than relying on the
   uncited catalog gloss.
2. Fix the domains of both primes: natural positive primes, integer primes, or another encoding.
3. State primality and oddness explicitly, including how the prime 2 is excluded.
4. Define the Legendre-symbol numerator/denominator convention and the values 0, 1, and -1.
5. Select the ordered binders and orientation of `p` and `q`.
6. Select the product law, signed equality, congruence-mod-4 split, or residue-predicate root.
7. Decide whether `p != q` is a premise. The product theorem requires distinct primes; the
   mathlib equality variant permits `p = q` because both relevant symbols are zero.
8. Fix the sign exponent and prove the transport between natural division
   `p / 2 * (q / 2)` and `((p - 1) / 2) * ((q - 1) / 2)` under oddness.
9. Decide whether the theorem asserts only reciprocity or also includes supplementary laws.
10. Freeze universes, typeclass context, minimal imports, foundation/TCB/computation profiles,
    alternate encodings, and every required mutation boundary.

## Boundary and degenerate cases

The statement phase must explicitly handle `p = 2`, `q = 2`, `p = q`, the order of the two
prime binders, and all four pairs of residues modulo 4. It must also distinguish a symbol value of
zero (divisibility) from quadratic nonresidue value -1. Nothing at intake excludes a case before
one exact proposition is source-approved.

## Excluded substitutions

- The supplementary laws for -1, 2, or -2 alone are not the two-prime reciprocity theorem.
- Euler's criterion and evaluations of one Legendre symbol are ingredients, not the root.
- A theorem only for primes congruent to 1 modulo 4 or only for both primes congruent to 3 modulo 4
  is one branch, not the complete law.
- Jacobi-symbol reciprocity and composite odd moduli are generalizations, not silent replacements.
- A statement about arbitrary finite fields, quadratic characters, or Gauss sums is supporting
  infrastructure unless a checked composition proves the selected root.
- A product statement that drops distinctness without addressing the zero-symbol case, or an
  equality statement that silently changes the source's domain, is not accepted.
- The catalog's untrusted verified label, a theorem name, or the discovery probe supplies no source
  fidelity or proof credit.

## Neighbor boundaries

`THM-M-0476` (Wilson's theorem), `THM-M-0477` (Chinese remainder theorem), and
`THM-M-0479` (Dirichlet's theorem) are separate targets. The reciprocity law may use general
congruence and prime infrastructure, but none of those targets can substitute for its signed
two-prime conclusion.
