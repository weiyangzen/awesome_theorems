# Scope map

## Identified theorem family

The intake scope is the scalar nonlinear integral-inequality family commonly associated with
Bihari's generalization of Bellman's/Gronwall's inequality. A later statement phase may select a
root only after an immutable primary edition is inspected and its exact numbered result is mapped.
The expected mathematical components, not yet credited as the theorem, are:

- a real interval with an initial point and an orientation;
- a nonnegative unknown or majorized scalar function;
- a nonnegative time weight and a nonlinear response function;
- an integral inequality coupling the unknown to the response;
- an auxiliary transform built by integrating the reciprocal response;
- a domain/range condition permitting an inverse transform;
- a pointwise upper-bound conclusion on a source-specified interval.

## Decisions required at statement freeze

The statement phase must freeze all of the following from the accepted source rather than from a
textbook convention:

1. The exact primary edition, result number, pages, wording, definitions, and errata disposition.
2. Whether the root is Bihari's generalized Bellman lemma, a later LaSalle form, a differential
   inequality, a uniqueness corollary, or another named variant.
3. The time domain, endpoints, interval orientation, and whether the result is local or global.
4. The codomain and regularity of `u`, the time weight, and the nonlinear response `omega`.
5. Every nonnegativity, positivity, continuity, and monotonicity hypothesis, including behavior at
   zero and whether `omega` may vanish.
6. The exact integral convention and whether the hypothesis holds pointwise or almost everywhere.
7. The base point and normalization in the reciprocal-response transform.
8. Ordinary inverse versus generalized inverse, its domain, and the range/blow-up cutoff.
9. Strict versus non-strict inequalities and every endpoint or zero-initial-value case.
10. The exact conclusion and its quantifier order, including any maximal interval on which it holds.

## Degenerate and boundary cases

The source review must explicitly dispose of an empty or reversed interval; `u0 = 0`; identically
zero time weight; constant, zero, or non-strictly increasing response; a divergent reciprocal
integral at zero; a finite upper endpoint of the transform range; equality cases; discontinuities;
and functions for which the relevant integrals do not exist. These choices can change the truth and
strength of the result.

## Explicit exclusions

- The pinned linear theorem `norm_le_gronwallBound_of_norm_deriv_right_le` is not a substitute.
- The ordinary Gronwall inequality scheduled as `THM-M-1337` remains a separate target.
- Osgood's uniqueness criterion, ODE uniqueness, continuous dependence, comparison principles, and
  LaSalle's invariance principle are not silently substituted for the requested inequality.
- A special case with `omega(r) = r`, a discrete inequality, vector-valued norm estimate, or finite
  numerical experiment cannot stand in for the source-selected root.
- A structure or theorem hypothesis that assumes the desired inverse-transform bound is prohibited.
- The repository label `verified` supplies no human-source or kernel-proof credit.

No canonical Lean target, expression fingerprint, checked alternate encoding, obligation registry,
or proof state is frozen at intake.
