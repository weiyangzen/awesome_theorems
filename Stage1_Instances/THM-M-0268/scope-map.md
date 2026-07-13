# Scope map

## Preserved catalog scope

The intake preserves the named Lebesgue dominated-convergence family and the catalog's literal
claim that some conditions permit exchange of a limit and an integral. A conventional modern
sequence form, recorded only as a candidate, has:

- a measure space `(alpha, m, mu)`;
- a sequence of measurable or almost-everywhere strongly measurable functions `F n`;
- almost-everywhere pointwise convergence of `F n` to `f`;
- one integrable function dominating the norms or absolute values of every `F n` almost everywhere;
- convergence of the integrals of `F n` to the integral of `f`; and often
- integrability of `f` and convergence in `L1` as companion conclusions or consequences.

The catalog does not contain these binders or assumptions. They delimit the recognizable family;
they are not yet the canonical statement.

## Proposition-changing decisions

The statement phase must freeze all of the following from an admitted source rather than from the
theorem name or a convenient library declaration:

1. The exact source edition, proposition and definition locators, proof boundary, translation,
   correction or errata record, and independent review.
2. The measurable carrier, measure, scalar field, and codomain: real-valued, complex-valued,
   arbitrary real normed-space-valued, or nonnegative extended-real-valued functions.
3. Whether the integral is the Bochner integral or `lintegral`, and whether the expected root is a
   convergence theorem alone or also asserts integrability and `L1` convergence.
4. Whether the index is `Nat` with `atTop` or a general countably generated filter.
5. Whether convergence, measurability, and domination hold everywhere or almost everywhere, and
   whether measurability is ordinary, almost-everywhere, or strong measurability.
6. Whether domination is `norm (F n x) <= g x`, `abs (F n x) <= g x`, or an `ENNReal` order
   bound, plus the exact nonnegativity, measurability, and integrability requirements on `g`.
7. Ordered binders, implicit typeclass assumptions, equality orientation, topology on integral
   values, universe levels, foundation profile, and minimal imports.

Every alternate form requires a checked transport after source selection; a general library form
cannot silently broaden a source-selected scalar or sequence theorem.

## Boundary and mutation cases

The selected statement must explicitly handle null or infinite measures, zero or negative-looking
real bounds, functions changed on null sets, an almost-everywhere rather than everywhere limit,
nonmeasurable representatives with measurable modifications, a limit not separately assumed
integrable, incomplete codomains, and constant or eventually constant sequences. Required statement
mutations must reject removal of integrable domination, replacement of one uniform dominator by
per-term bounds, pointwise convergence outside the selected almost-everywhere scope, a non-equivalent
codomain change, and a conclusion about only a subsequence or only limsup inequalities.

## Explicit exclusions

- Monotone convergence, Fatou's lemma, bounded convergence, uniform convergence, Vitali
  convergence, or convergence in measure substituted for dominated convergence.
- The nonnegative `lintegral` theorem substituted for a source-selected signed or Bochner theorem,
  or conversely.
- A filter generalization substituted for a sequence root without a checked specialization.
- Series, interval-integral, conditional-expectation, or parametric-continuity corollaries used as
  the root target.
- A hypothesis that already assumes convergence of the integrals or integrability of the limit.
- The catalog's untrusted `已验证` label, a theorem name, a successful `#check`, or an axiom report
  used as source or proof evidence.

## Formal boundary

Pinned mathlib directly exposes Bochner-integral and nonnegative-`lintegral` dominated convergence
families. Their interfaces are unusually close to the catalog title, so the provisional machine
status is `M3`, not `M4`. Nevertheless, source selection, exact target elaboration, normalized
expression matching, proof-body provenance, dependency and trust closure, and accepted wrapper
evidence belong to later phases. The bounded intake search is not an exhaustive anchor audit.
