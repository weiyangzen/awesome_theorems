# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0821`, the title `Sperner定理`, Emanuel Sperner, 1928, and
the gloss `幂集反链的最大大小`. The primary paper fixes the intended mathematical family:
subsets of one finite ground set, ordered by inclusion, with no member contained in another. Its
printed page 544 states the sharp middle-binomial bound and the equality cases. Importance `高` and
status `已验证` remain inventory metadata, not source-review or Lean-kernel evidence.

## Proposition-changing decisions

The statement phase must freeze all of the following from an independently reviewed source
transcription:

1. Whether the root is the upper bound, an equality of the maximum over all antichains, existence
   of a maximum-sized middle layer, or the full classification of equality cases.
2. The finite ground-set encoding: an arbitrary finite set, a finite type `alpha`, or `Fin n`, and
   the checked transport between any credited variants.
3. The family encoding: `Finset (Finset alpha)`, a finite `Set (Set alpha)`, or another carrier,
   including all finiteness and decidable-equality instances.
4. The antichain relation and orientation. The source forbids a member from being a subset of a
   different member; the Lean candidate uses `IsAntichain (fun x y => x \u2286 y)`.
5. The exact result: cardinality at most `Nat.choose n (n / 2)`, together with the convention that
   natural-number division supplies the lower middle rank.
6. If equality is included, the even/odd split and whether complement-related middle layers are
   stated as the only extremizers up to literal equality, relabeling, or order isomorphism.
7. Boundary cases `n = 0` and `n = 1`, the empty family, singleton families, and the two adjacent
   middle ranks when `n` is odd.

## Candidate canonical family, not yet frozen

Pinned mathlib's upper-bound candidate has the elaborated interface shape

```text
{alpha : Type u} [Fintype alpha] {A : Finset (Finset alpha)} ->
IsAntichain (fun x y => x \u2286 y) (A : Set (Finset alpha)) ->
A.card \u2264 Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)
```

This is an excellent candidate for the source paper's inequality component. Intake does not call it
the canonical root because the repository phrase "maximum size" may require the lower-bound witness
or equality classification that the declaration omits.

## Explicit exclusions

- The LYM inequality alone, local shadow inequalities, or a middle-layer cardinality lemma used as
  a substitute for Sperner's theorem.
- A theorem about arbitrary finite posets unless a checked Boolean-lattice specialization preserves
  the exact source statement.
- Dilworth, Mirsky, Erdos-Ko-Rado, or another neighboring antichain/intersection theorem.
- Multiset, list, weighted, infinite, `k`-uniform-only, or cross-Sperner generalizations used in
  place of the finite Boolean-lattice theorem.
- A structure that assumes the cardinality bound, an extremizer, or the equality classification as
  stored data.
- Exhaustive enumeration, a numerical experiment, or an unchecked certificate.
- The catalog's `已验证` label or the intake API probe used as source or proof credit.

## Neighbor and dependency boundaries

- `THM-M-0819` (Dilworth) and `THM-M-0820` (Mirsky) concern chain/antichain decompositions in
  general finite posets; they do not close this Boolean-lattice extremal result.
- `THM-M-0822` (Erdos-Ko-Rado) concerns maximum intersecting uniform families and is separate.
- The LYM and shadow declarations in the same pinned module are candidate proof dependencies, not
  independently accepted obligations or root closure at intake.
