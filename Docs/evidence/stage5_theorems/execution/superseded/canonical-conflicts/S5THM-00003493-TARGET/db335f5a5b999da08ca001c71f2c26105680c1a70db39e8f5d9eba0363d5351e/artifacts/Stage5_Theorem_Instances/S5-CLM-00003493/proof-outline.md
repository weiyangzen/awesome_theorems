# Proof outline: S5-CLM-00003493

Let `F(n)` be the largest length of a list of triples from `[1,n]` such that
every earlier triple is smaller than every later triple in at least two
coordinates. Let `L(n)` be the iterated logarithm from the source.

1. Assume an admissible list has more than `n²` entries. Map each position to
   the pair consisting of its first two coordinates. All pairs lie in a set of
   cardinality `n²`, so two different positions have the same pair.
2. Order those two positions. Pairwise increasingness says the earlier triple
   is strictly smaller than the later one in two distinct coordinates. At
   least one of those coordinates must be the first or second, contradicting
   equality there. Hence every admissible list has length at most `n²`, and
   therefore `F(n) ≤ n²`.
3. Choose `Ω(n) = -L(n)`. Big-O uses norms, so `L = O(-L)` follows from
   `|L| = |-L|` (implemented by reflexive Big-O followed by right negation).
4. The iterated logarithm is a natural number, hence nonnegative. Thus
   `exp(Ω(n)) = exp(-L(n)) ≤ 1`, while it remains positive.
5. Therefore `n² ≤ n² / exp(Ω(n))`. Compose this with the quadratic bound to
   obtain the required inequality for every `n`.

The construction also covers `n = 0` and `n = 1`; the pigeonhole argument does
not need a separate small-`n` case.
