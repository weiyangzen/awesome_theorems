# Scope map

## Included claim

- A real-valued i.i.d. sequence with mean zero, variance one, and a moment generating function
  finite on an open interval containing zero.
- Existence, on one probability space, of variables with the prescribed i.i.d. law and an i.i.d.
  standard Gaussian sequence. Partial sums of the Gaussian sequence may equivalently be represented
  by a standard Brownian motion sampled at the nonnegative integers.
- A nonasymptotic exponential tail estimate, with constants depending only on the input law, for
  the running maximum of the partial-sum discrepancy above a threshold of the form
  `C * log n + x`, uniformly in positive integers `n` and real `x >= 0`.
- Consequently, an almost-sure `O(log n)` strong approximation, derived rather than substituted for
  the tail estimate.

The variance-one form is the normalization target. A checked scaling transport may later support a
strictly positive finite variance. The normal and other degenerate-at-the-boundary cases must be
handled by the exact quantifiers rather than silently excluded.

## Statement-phase decisions

Primary-source inspection must settle the exact neighborhood/moment hypothesis, whether constants
are named or existential, the threshold's additive constants and logarithm convention, strict
versus weak inequalities, and the ranges of `n` and `x`. It must also decide whether the canonical
coupling is stated using Gaussian increments or a Brownian motion, and whether the almost-sure
corollary belongs to the root or is a child.

The Lean phase must select encodings for distributions, identical distribution, independence,
partial sums, moment generating functions, maxima over `Finset.range`, and probability tail bounds.
It must freeze binder order, all typeclass assumptions, the common probability space, the exact
expression fingerprint, foundation/TCB/computation profiles, and boundary cases such as `n = 1`.

## Explicit exclusions

- The empirical distribution function, empirical process, or Brownian-bridge KMT construction;
  those are related KMT results but not this entry's partial-sum root.
- Donsker's invariance principle or a Skorokhod representation with only `o(sqrt n)` discrepancy.
- An approximation only in distribution, in probability, or at the single terminal sum rather than
  a common-space running-maximum coupling.
- Assuming the desired coupling or tail inequality as a hypothesis, or replacing the input law by
  Gaussian variables so that the conclusion becomes tautological.
- A finite-moment approximation with a polynomial error rate in place of the exponential-moment
  logarithmic approximation.

These boundaries distinguish this target from the neighboring manifest entry `THM-M-1066` (named
only "KMT theorem" there); no proof or scope state is borrowed from that separately owned target.
