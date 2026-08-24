# Proof outline

Let `n = 2k`, let `F(p)` be the upper-tail probability of a binomial random variable with parameters `(n,p)`, and let

`G(p) = 1 - Φ((1/2-p)√(2k)/√(p(1-p))) + ½·choose(2k,k)·(√(p(1-p)))^(2k)`.

1. Express `F(p)` as the beta integral `choose(n,k)·k·∫₀ᵖ t^(k-1)(1-t)^(n-k) dt`. This representation is proved directly from the finite binomial PMF tail.
2. Differentiate `F-G`. After positive factors are removed, its sign is equivalent to comparing a scalar function `ψₖ(p)` with a constant assembled from the central binomial coefficient.
3. Prove the comparison has one crossing. The derivative of `ψₖ` factors through `p(1-p)`; Wallis bounds and Gaussian calculus establish the necessary endpoint and monotonicity estimates.
4. Extend the gap continuously to `p=0`. Both the binomial integral and the Gaussian/correction terms tend to zero there. At `p=1/2`, symmetry of the even binomial law and `Φ(0)=1/2` give gap zero.
5. The derivative is nonnegative up to the crossing and nonpositive after it. Thus the continuous gap rises from zero and returns to zero, so it is nonnegative on `[0,1/2]`.
6. Rewrite the beta integral back to the PMF tail and substitute the supplied equality `σ = √(p(1-p))`. This is exactly the frozen Conjecture 6.3 inequality.

Exceptional cases are discharged by `0 < k` and `p ∈ (0,1/2)`, which keep every denominator positive and make the finite-tail index well formed.
