# Proof outline

## RO-root

Let

\[
a_n=\frac{(2/3+(1/3)\sin n)^n}{n},\qquad n\ge 1.
\]

The target says that the positive answer is equivalent to summability of
`a`.  Since the positive Boolean answer elaborates to truth, the substantive
direction is exactly convergence of this nonnegative series.

## RO-rewrite

Using `1 - cos x = 2 sin²(x/2)`, rewrite

\[
2/3+(1/3)\sin n=1-\frac{1-\sin n}{3}.
\]

For `0 ≤ x ≤ 1`, `(1-x)^n ≤ exp(-nx)`.  Thus the term is controlled by
the distance of `n` from a maximum of sine, equivalently the distance of
`2n-π` from a multiple of `4π`.

## RO-arithmetic

Partition positive integers into dyadic blocks and then into level sets for
the distance to `π/2 + 2πℤ`.  A quantitative irrationality measure for `π`
separates exceptionally close returns.  Counting the remaining returns at
each level gives a summable bound per dyadic block; summing the blocks proves
`Summable a`.

## RO-composition

The Lean root composes the analytic convergence fact with the tautological
reverse implication from summability to truth.  The provider's sorry-backed
body is not referenced.  The two crosswalk theorems express both directions
of the identity transport between the frozen surface and the claim-owned root.

## RO-exception

`n : ℕ+` excludes zero, so division by `n` is harmless.  The coefficient lies
in `[1/3,1]`; it reaches one only if `sin n = 1`, impossible for an integer by
irrationality of `π`.  Near-maximal returns are precisely the exceptional case
handled by the irrationality-measure level sets.

## RO-trust

The provider supplies statement bytes, never a proof.  The worker preflight
does not establish kernel closure.  Trust-zero compilation, exact dependency
and axiom collection, cold replay, and mutation replay are reserved for the
canonical Master.
