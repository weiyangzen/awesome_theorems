# Scope map

## Included claim

- A discrete-time filtered probability space and a real-valued martingale `f` with finite time
  horizon and terminal value in `L^p`, where `1 < p < infinity`.
- A real predictable multiplier sequence `v`: the multiplier used on the increment from time
  `k - 1` to `k` is measurable with respect to the information available at time `k - 1`.
- The pointwise bound `|v_k| <= 1` and the transform
  `g_n = sum_{k=1}^n v_k * (f_k - f_{k-1})`.
- A terminal `L^p` estimate `||g_n||_p <= C_p ||f_n||_p`, with one finite constant depending only
  on `p`, uniformly in the space, filtration, martingale, multipliers, and finite horizon.

This qualitative formulation is deliberately insensitive to a non-sharp choice of `C_p`. A sharp
constant is not part of the frozen claim until a primary-source audit shows that it belongs to the
repository record rather than to a later strengthening.

## Statement-phase decisions

The next phase must select and inspect a pinpoint primary statement before fixing the Lean target.
It must settle whether the source starts the transform at zero or includes `v_0 f_0`, whether
predictability is expressed by shifted adaptedness, whether martingales are indexed by `Nat` or
`Fin (n+1)`, and whether the conclusion uses the terminal variable, a supremum over times, or a
bounded-martingale norm. It must also choose mathlib's filtration, conditional expectation,
strong-measurability, `MemLp`, and `snorm` conventions and freeze binder order and universes.

Boundary cases to record include horizon zero, zero increments, multipliers `0`, `1`, and `-1`,
null sets in the multiplier bound, and `p` at the excluded endpoints. The statement gate must not
turn an almost-everywhere bound into a pointwise assumption, or conversely, without a checked
transport.

## Explicit exclusions

- The Burkholder-Davis-Gundy comparison between a martingale maximum and quadratic variation.
- A continuous-time stochastic integral or semimartingale transform as a replacement for the
  discrete transform.
- Weak-type `p = 1`, endpoint, differential-subordination, UMD Banach-space, or Hilbert-transform
  extensions.
- A theorem assuming the desired `L^p` bound, a definition-only declaration, or a result for one
  fixed martingale or one fixed multiplier sequence.
- Claiming the later sharp factor `p* - 1` unless its exact applicable theorem and historical
  source are separately verified.

The formal statement may use an equivalent martingale-difference formulation only after a checked
two-way transport preserves filtration measurability, integrability, indexing, and the norm bound.
