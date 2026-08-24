# Proof outline — Erdős–Szekeres bounds

For `n ≥ 3`, write `f(n)` for the least cardinality forcing `n` points in convex position among planar finite sets with no three collinear.

1. **Lower construction.** The standard separated-block induction builds `2^(n-2)` points in general position with no convex `n`-subset. Every smaller cardinality is obtained by taking a subset. Consequently no integer at most `2^(n-2)` belongs to `cardSet n`, so `2^(n-2)+1 ≤ sInf (cardSet n)`.
2. **Upper cup–cap theorem.** After choosing a generic horizontal direction, order the points by first coordinate. The cup–cap induction says that more than `choose(r+s-4,r-2)` points contain an `r`-cup or an `s`-cap. With `r=s=n`, either chain consists of `n` vertices in convex position. Hence `choose(2*n-4,n-2)+1 ∈ cardSet n`, and the defining infimum is at most that value.
3. **Composition.** Apply both estimates for the same `n` and pair them. The statement/audit roundtrip verifies that this is exactly the curried conjunction of the frozen provider declaration.

Degenerate cases are explicit: `n < 3` is outside the theorem, and the generic-direction step uses the finite general-position hypothesis rather than assuming distinct original x-coordinates.
