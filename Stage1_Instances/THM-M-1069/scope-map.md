# Scope map

## Repository boundary

The title names the Skorokhod problem, while the only repository gloss says "reflected stochastic
differential equation." These do not fix the state space, reflecting domain, reflection direction,
driving signal, coefficient hypotheses, or whether the desired result is the deterministic
reflection map or existence and uniqueness for a reflected SDE. The intake preserves this
ambiguity as the first statement-phase blocker.

## Leading claim candidate

- A continuous real input path `x` on a fixed compact interval, initially in `[0, infinity)`.
- A constrained path `z` and regulator `k` satisfying `z = x + k`.
- Nonnegativity of `z`, with `k(0) = 0` and `k` nondecreasing.
- The complementarity/minimality condition that the regulator changes only on the zero set of
  `z`, expressed by a source-backed support or Stieltjes-integral condition.
- Existence, uniqueness, and the explicit half-line formula
  `k(t) = sup_{0 <= s <= t} max(-x(s), 0)`.

This is the standard one-dimensional deterministic reflection problem and is only the leading
candidate. It is not yet asserted to be the exact source theorem behind the repository entry.

## Reflected-SDE candidate

If primary-source inspection confirms the gloss as the root, the exact theorem must instead expose
a filtered probability space, Brownian driver, initial value, drift and diffusion coefficients,
a reflecting domain and inward normal/reflection field, an adapted continuous solution, and a
finite-variation regulator supported on the boundary. It must state the selected weak/strong
existence and pathwise/in-law uniqueness conclusion with its actual regularity hypotheses.

## Required statement decisions

The statement phase must select one pinpointed theorem and freeze: interval and endpoint
conventions; continuous versus cadlag inputs; half-line, interval, orthant, or smooth domain;
normal versus oblique reflection; regulator codomain and bounded-variation convention;
complementarity encoding; initial-boundary behavior; and any SDE coefficient, filtration,
adaptedness, and uniqueness assumptions. It must probe paths starting on the boundary, paths never
crossing zero, constant negative excursions after time zero where allowed, zero-length intervals,
and multidimensional corner behavior where relevant.

## Explicit exclusions

- Assuming the desired reflected path or reflected-SDE solution as structure data.
- Replacing existence and uniqueness by nonnegativity alone or by an unconstrained SDE theorem.
- Substituting absolute value of Brownian motion, a discrete random walk, or a penalized
  approximation for the exact reflection theorem.
- Presenting the half-line explicit formula as closure of a multidimensional or reflected-SDE root
  without checked source-backed reduction and composition.
- Inferring any proof credit from the manifest label `已验证`.
