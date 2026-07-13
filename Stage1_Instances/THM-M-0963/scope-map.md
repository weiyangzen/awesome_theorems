# Scope map

## Preserved theorem family

The intake preserves the classical uniform Ray-Chaudhuri-Wilson intersection-bound family.
For a finite ground set of size `n`, let `L` contain `s` permitted nonnegative intersection
sizes and let `F` be a family of `k`-subsets such that distinct members meet in a cardinality
belonging to `L`. The familiar candidate conclusion is `|F| <= choose n s` when
`0 < s <= k <= n`. This description fixes the theorem family, not an accepted canonical
proposition.

## Candidate source proposition

Theorem 1.6 of arXiv:`1512.05531v2` states the candidate explicitly: positive integers
`0 < s <= k <= n`, a set `L` of `s` nonnegative integers, and an L-intersecting,
`k`-uniform family `F = {F_1, ..., F_m}` of subsets of `[n]` imply
`m <= choose n s`. Theorem 7 of arXiv:`0905.2423v2` independently records the same bound
using the phrase "w-uniform s-intersecting family." These are immutable secondary
restatements of the primary 1975 result, not substitutes for inspecting and admitting the
primary passage.

## Decisions required at statement freeze

1. Authenticate and inspect one immutable complete edition of the 1975 paper, select the
   exact theorem/corollary and incorporated definitions, audit corrections, and obtain an
   independent premise-by-premise review.
2. Fix whether `L` is a finite set of natural numbers with `card L = s`, an indexed list of
   `s` distinct values, or an arbitrary permitted set of size at most `s`. Replacing equality
   by `card L <= s` changes parameter monotonicity and boundary behavior.
3. Fix the family as a finset of distinct `k`-subsets, an indexed family with a no-duplicate
   premise, or a finite set. The conclusion counts distinct members, not list multiplicity.
4. Fix the ground set as `Fin n` or an abstract finite type and compile any cardinality
   transport rather than identifying the encodings informally.
5. Fix uniformity as `card A = k` for every member and preserve the ordered dependency of
   `s`, `k`, `n`, `L`, and the family.
6. Fix L-intersection over distinct family members. Applying the condition to a member
   against itself additionally requires `k in L` and is not equivalent.
7. Fix the exact parameter range. The secondary statement uses `0 < s <= k <= n`; the
   intake does not silently drop positivity or infer alternate endpoints from the formula.
8. Fix the conclusion as the upper bound only. A tightness construction, equality
   classification, nonuniform strengthening, modular variant, or vector-space analogue is
   additional mathematics unless the selected source explicitly makes it part of the root.

## Degenerate and boundary cases

Source and statement review must dispose of `s = 0`, `k = 0`, `n = 0`, `s = k`, `k = n`,
an empty `L`, repeated listed values, values in `L` greater than `k`, the empty or singleton
family, `L` containing or excluding zero, and the distinction between exact size `s` and at
most `s`. It must also test a family containing duplicate indexed blocks, intersection of a
block with itself, and natural-number binomial conventions when parameters are out of range.
No case is excluded at intake.

## Neighbor and substitution exclusions

- `THM-M-0962` Frankl-Wilson concerns a modular intersection method and cannot replace the
  ordinary exact-cardinality L-intersection bound.
- `THM-M-0822` Erdős-Ko-Rado and `THM-M-0964` Hilton-Milner impose nonempty intersection
  and optimize different uniform-family classes; they are not this finite-list bound.
- `THM-M-0965` Ahlswede-Khachatrian is a complete t-intersection theorem, and
  `THM-M-0966` Kruskal-Katona is a shadow theorem. Neither shares root credit.
- Nonuniform Ray-Chaudhuri-Wilson inequalities, Fisher-type inequalities, modular forms,
  vector-space q-analogues, few-distance results, equality classifications, and numerical
  examples are differently typed or stronger/weaker targets.
- A proof of `card F <= 2^n`, an assumed linear-independence certificate, an API probe, or
  the catalog's `已验证` label supplies no requested proof credit.

No canonical Lean expression, statement fingerprint, checked alternate encoding, obligation
registry, discovery protocol, accepted proof state, or completion claim is frozen at intake.
