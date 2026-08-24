# Proof outline

1. From `p ∈ (0, 1/2)`, obtain both nonnegativity for the `ℝ≥0` binomial parameter and the bound `p ≤ 1` required by `PMF.binomial`.
2. Preserve `k > 0` and the defining identity `σ = sqrt (p(1-p))`; no exceptional zero-variance case is silently introduced.
3. Use the checked analytic certificate for the sum of the normal-tail contribution and half the central atom.
4. Compose that certificate through `central_binomial_tail_bound`; the result is the exact probability lower bound for the event `{j | k ≤ j}` under `Binomial(2k,p)`.
5. Transport definitionally in both directions between the provider surface (whose local `Φ` denotes the standard-normal CDF) and the claim-owned explicit-CDF surface.

The exceptional cases `p = 0`, `p = 1/2`, and `k = 0` remain excluded exactly as in the frozen statement. The provider's proof body is outside the trust boundary; only the claim-owned proof term and the canonical Master replay can supply closure.
