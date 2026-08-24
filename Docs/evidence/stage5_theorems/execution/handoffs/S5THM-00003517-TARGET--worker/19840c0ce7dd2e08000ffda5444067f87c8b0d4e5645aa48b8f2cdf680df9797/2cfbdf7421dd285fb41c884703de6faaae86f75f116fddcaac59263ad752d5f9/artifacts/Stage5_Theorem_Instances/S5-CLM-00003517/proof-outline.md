# Proof outline

1. Normalize the frozen proposition and choose `c = 1/256`.
2. If the finite vertex type is empty, use the empty set and the zero matrix.
3. If `1 ≤ n < 4`, use a singleton; its induced Laplacian has no internal edge
   and the size inequality follows from `ε ≤ 1`.
4. For `n ≥ 4`, take a Hermitian square root and pseudoinverse of the graph
   Laplacian.  The dynamic BSS barrier colors `k = floor(n/4)` vertices with
   `r = ceil(16/ε)` colors while keeping every normalized monochromatic sum
   below the ε barrier.
5. Pigeonhole gives a color class of cardinality at least `k/r`.  The integer
   and real inequalities `n ≤ 8k` and `εr ≤ 32` imply `k/r ≥ εn/256`.
6. Transport the resulting exact proposition in both directions to the frozen
   provider declaration.
