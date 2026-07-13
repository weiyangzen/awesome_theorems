# Scope map

## Received claim

The repository names Burnside's theorem and gives the gloss `p^a q^b阶群可解`, meaning that a
group of order `p^a q^b` is solvable. This distinguishes the intended finite-group theorem from
Burnside's orbit-counting lemma, but it is not a fully bound proposition.

## Candidate family boundary

A usual modern reading has all of the following clauses, each still requiring a pinpoint source
and an independently reviewed formal choice:

- a group `G` whose finite order is represented by `Nat.card G`;
- primes `p` and `q`, usually distinct;
- natural-number exponents `a` and `b`;
- an equality `Nat.card G = p ^ a * q ^ b`;
- the conclusion that the derived series of `G` eventually reaches the trivial subgroup.

In pinned mathlib the last clause is `IsSolvable G`, defined by `isSolvable_def`. The preceding
clauses have plausible encodings, but the repository has not selected their binder order,
typeclass form, or boundary policy. This intake does not freeze the candidate as the root.

## Decisions required at statement freeze

1. Admit and independently review an immutable primary or authoritative source passage, including
   its definitions, assumptions, proof boundary, edition history, corrections, and errata.
2. State finiteness explicitly and choose `[Finite G]`, `[Fintype G]`, or a consequence of a
   positive `Nat.card` equality without making the premise circular.
3. Fix whether `p` and `q` must be distinct, whether their order is significant, and how one-prime
   cases are represented.
4. Fix the exponent domain and decide whether `a = 0`, `b = 0`, or both zero are included.
5. Choose equality of cardinality with `p ^ a * q ^ b` versus a prime-support formulation, and
   supply checked transports for every credited alternate encoding.
6. Fix the exact solvability convention and its relationship to mathlib's derived-series
   predicate `IsSolvable`.
7. Freeze ordered binders, universes, typeclass context, multiplication orientation, and the
   behavior of the trivial group, prime-order groups, prime-power groups, and `p = q`.

## Related but nonidentical results

- `MonoidHom.ker_transferSylow_isComplement'` is Burnside's normal p-complement theorem. It has
  extra Sylow-centralizer hypotheses and is a possible proof ingredient, not this root theorem.
- The finite Z-group `IsSolvable` instance assumes all Sylow subgroups are cyclic. A group of order
  `p^a q^b` need not satisfy that stronger premise.
- `IsPGroup.of_card` handles a single prime power and does not establish the two-prime theorem.
- The Sylow theorems provide subgroup existence and counting ingredients, not the solvability
  conclusion by themselves.
- Burnside's lemma counts orbits of a group action and is a separate target (`THM-M-0929`).

## Explicit exclusions

- Burnside's orbit-counting lemma, Burnside's normal p-complement theorem, or the Burnside basis
  theorem substituted for the received theorem.
- Solvability only for squarefree-order groups, Z-groups, odd-order groups, abelian groups, or
  fixed primes or fixed exponents.
- A one-prime p-group result silently substituted for the two-prime family.
- A hypothesis, structure, or typeclass that already contains `IsSolvable G`.
- A proof for groups whose order divides `p ^ a * q ^ b` substituted without a checked source
  relationship to an equality formulation, or conversely.
- The catalog's `已验证` label, a theorem name, `#check` output, or a successful interface probe
  treated as proof credit.

No canonical Lean expression, ordered binders, hypotheses, conclusion encoding, alternate
transport, or degenerate-case exclusion is frozen during intake.
