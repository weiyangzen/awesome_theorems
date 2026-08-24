# Full study — even binomial tail versus Gaussian correction

## Statement and interpretation

For `0 < p < 1/2`, positive natural `k`, `m=2k`, and `σ=√(p(1-p))`, the theorem lower-bounds the central upper tail of `Binomial(m,p)` by a Gaussian tail plus half of the central-binomial mass scale. The event starts at `k=m/2`; its Lean encoding uses the measure of `Set.Ici` on `Fin (m+1)`.

## Integral model of the binomial tail

The finite PMF tail is first expanded as a sum of binomial terms. Differentiating that sum telescopes, leaving

`choose(n,k) · k · p^(k-1) · (1-p)^(n-k)`.

Both the PMF tail and its beta-integral candidate vanish at zero, so equality follows from the derivative identity. This step is fully finite on the probability side and uses interval integration only for the analytic representation. At `n=2k` and `p=1/2`, symmetry splits the two tails and central mass, producing the exact endpoint correction.

## Gaussian and correction derivatives

Write `s=p(1-p)` and `z=(1/2-p)√(2k)/√s`. Differentiation of the Gaussian CDF uses its standard density. Differentiation of the correction term is elementary after replacing `√s` to the even power by `s^k`. Algebraic normalization isolates positive factors and reduces the sign of the complete gap derivative to a logarithmic scalar comparison `ψₖ(p) ≷ Cₖ`.

The required analytic controls include positivity of `s`, the bound `s≤1/4`, the exact identity for `z²`, Gaussian endpoint limits, and central-binomial estimates obtained from the Wallis product. None of these introduces a new axiom or an unproved analytic oracle.

## Single-crossing geometry

The derivative of `ψₖ` factors as a positive term times a function that is strictly monotone on `(0,1/2)`. Its limiting behavior at zero, its value at one half, and the Wallis comparison show that `ψₖ-Cₖ` crosses at the required location. Consequently, the original gap derivative is nonnegative on the left portion and nonpositive on the right.

This is exactly the geometry needed for the unimodal-gap lemma: a continuous function that starts at zero, increases until a crossing, then decreases to zero cannot be negative in the interval.

## Endpoint and exceptional-case audit

At zero, the beta integral tends to zero; the Gaussian standardized argument tends to positive infinity, making the Gaussian upper tail tend to zero; and the correction term also tends to zero. At one half, the standardized argument is zero, `Φ(0)=1/2`, and the even-tail symmetry identity closes the gap.

The strict hypotheses exclude every denominator singularity. `k>0` makes the beta exponent and threshold valid. `p>0` and `p<1/2<1` give positivity of `p`, `1-p`, and `σ`. Natural-number side conditions for the `Fin` threshold are discharged arithmetically.

## Trust and provenance

The mathematical construction follows the pinned solved-proof citation `logical-intelligence/proofs@0dbb9215f472c532ca8af1376ed58a7ebca6dec2`, rematerialized against the canonical repository toolchain. The source Formal Conjectures theorem remains the semantic authority, not a proof dependency, because its frozen body is sorry-backed. The target root's Lean axiom report contains only `propext`, `Classical.choice`, and `Quot.sound`.

The readable reconstruction is total over eight proof nodes and points back to named formal declarations. Machine, human, and readability cut sets are empty; Master acceptance is still explicitly reserved for independent semantic-root recomputation and integrated-byte replay.
