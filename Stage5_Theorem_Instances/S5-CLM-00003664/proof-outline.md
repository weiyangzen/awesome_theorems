# Proof outline — Lenz lower bound

Put `p = d / 2`. The hypothesis `4 ≤ d` gives `2 ≤ p`, and the first `2p`
coordinates of `ℝ^d` split into `p` mutually orthogonal coordinate planes.
In each plane choose finitely many distinct points on the circle of radius
`1 / √2`. Points on different circles have squared distance
`1/2 + 1/2 = 1`, so every cross-class pair contributes a unit distance.

Distribute the `n` points as evenly as possible among the `p` circles. If the
class sizes are `a_i`, the number of cross-class pairs is

`Σ_{i<j} a_i a_j = (n² - Σ_i a_i²) / 2`.

Balanced sizes have `Σ_i a_i² ≤ n²/p + O_p(1)`. Thus the displayed count is
at least `(p-1)/(2p) n² - C_p`. The constructed set occurs among the finite
sets in the supremum defining `f d n`; consequently its unit-distance count
is at most `f d n`. Taking a single rounding constant `C = C_p` proves the
claim for every natural `n`.
