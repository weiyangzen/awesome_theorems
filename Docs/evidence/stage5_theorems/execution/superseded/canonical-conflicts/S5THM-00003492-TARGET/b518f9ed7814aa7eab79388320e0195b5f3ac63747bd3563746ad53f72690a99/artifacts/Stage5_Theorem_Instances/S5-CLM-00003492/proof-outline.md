# Proof outline — the maximal length is at most `n²`

## Claim

Let `s` be a list of triples of natural numbers. Every coordinate of every
triple lies in the interval `[1,n]`, and each earlier triple is strictly
smaller than each later triple in at least two distinct coordinates. Then the
length of `s` is at most `n²`. Taking the supremum over all such lengths gives
the claimed bound.

## Argument

1. Send position `k` to the ordered pair consisting of coordinates zero and
   one of the triple at `k`.
2. The coordinate-range hypothesis puts every image in
   `Finset.Icc 1 n ×ˢ Finset.Icc 1 n`, whose cardinality is `n²`.
3. If the list had more than `n²` entries, finite pigeonhole gives distinct
   positions with the same first two coordinates.
4. Put the earlier of those positions first. Pairwise increase says its two
   strictly increasing coordinates exist. Two distinct coordinates among
   `0,1,2` must include coordinate zero or one; equality in that coordinate
   contradicts strict increase.
5. Thus every admissible length is at most `n²`. The empty list witnesses that
   the set of lengths is nonempty, so `csSup_le` gives the supremum bound.

The proof is uniform in `n`. For `n=0`, the bounded-coordinate condition makes
every nonempty candidate impossible; for `n=1`, a list of length greater than
one would collide in its first two coordinates. These cases are therefore
covered by the same pigeonhole contradiction rather than discarded.
