# Full study — Erdős problem 1014

## Node N0: frozen statement

For an arbitrary natural `k` with `3 ≤ k`, the frozen target asks for convergence at infinity of the real quotient `R(k,l+1)/R(k,l)` to one. Here `R` has exactly the provider's Ramsey-number convention. This node takes the frozen record and hypothesis as inputs, outputs the exact target proposition, anchors at `A0:frozen-statement`, feeds N1 and N2, excludes `k<3`, and trusts only the pinned statement bytes—not either sorry-backed provider proof.

## Node N1: lower bound

On the eventual tail where `R(k,l)>0`, monotonicity in the second Ramsey parameter yields `R(k,l) ≤ R(k,l+1)`. Casting to the reals and dividing by the positive denominator gives `1 ≤ R(k,l+1)/R(k,l)`. The output is anchored at `A1:monotonic-lower-bound` and is used by N4. The only exceptional case is the finite initial range, which disappears under `atTop`; the trust boundary is the audited order, cast, positivity, and Ramsey-monotonicity library facts.

## Node N2: upper bound

The claim-owned quantitative argument, reconstructed independently of the FormalConjectures proof bodies, gives constants `c>0` and `C≥0` and an eventual threshold such that

`R(k,l+1) ≤ (1 + C*(l:ℝ)^(-c/(k:ℝ)^2))*R(k,l)`.

The argument's inputs are `3≤k` and the fixed Ramsey convention; its output is the displayed estimate at `A2:quantitative-one-step-bound`, used by N3 and N4. The threshold is enlarged so all casts and denominators used later are positive. The trust boundary excludes both `Erdos1014.erdos_1014` and its sorry-backed upper-bound variant; only the local reconstruction and audited foundation are admitted.

## Node N3: error decay

Because `c>0` and `k≥3`, the exponent `-c/k²` is strictly negative. Thus `l^(-c/k²)` tends to zero along the positive natural tail. Multiplication by the fixed nonnegative `C` and addition of one show that the upper factor tends to one. This conclusion is anchored at `A3:error-decay` and feeds N4. The value at `l=0` is exceptional but irrelevant to an eventual statement. The trust boundary is Mathlib's audited real-power and filter-limit layer.

## Node N4: squeeze

Conjoin the eventual predicates from N1–N3. Divide N2 by the positive `R(k,l)` to obtain

`R(k,l+1)/R(k,l) ≤ 1 + C*l^(-c/k²)`.

Together with N1, the quotient is squeezed between a constant sequence tending to one and the N3 sequence tending to one. The squeeze theorem outputs the required fixed-`k` convergence at `A4:squeeze`; N5 consumes it. Finite threshold differences are the sole exceptional case and are merged by eventual conjunction. The machine trust boundary is recorded, rather than duplicated, in `machine-closure.json`.

## Node N5: root

The parameter `k` was arbitrary subject only to `3≤k`, so universal introduction produces the exact frozen proposition. This output is anchored at `A5:universal-closure` and is used by the audit and release surfaces. It asserts nothing for `k<3`. Canonical-Master re-elaboration, trust-zero compilation, environment hashing, mutation testing, and release acceptance remain outside the worker trust boundary.
