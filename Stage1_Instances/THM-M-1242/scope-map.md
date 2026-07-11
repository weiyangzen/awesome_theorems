# Scope map

## Included claim

- The supercritical regime `1 <= n < p < infinity` for first-order scalar Sobolev functions.
- A bounded Euclidean domain with the precise Lipschitz or extension-domain hypothesis selected
  from the primary source.
- Existence of an almost-everywhere equal representative with Holder exponent
  `alpha = 1 - n/p`.
- A quantitative Holder/seminorm estimate with every constant dependency exposed.

## Statement-phase decisions

The next phase must freeze whether the canonical root is the Euclidean compact-support inequality
or its bounded-domain Sobolev consequence; the domain regularity; homogeneous versus inhomogeneous
Sobolev norm; scalar field; representative agreement; Holder norm convention; closure/boundary
behavior; and the exact dependence of the constant. It must also decide how the real exponent and
the natural dimension are represented and mutation-test `p > n` and `n >= 1`.

## Explicit exclusions

- The critical and subcritical cases `p <= n`, which have different conclusions.
- Mere continuity without the Holder exponent, or a qualitative statement without the required
  quantitative estimate.
- Arbitrary unbounded or irregular domains without the hypotheses needed for extension/restriction.
- Vector-valued, higher-order, metric-measure, Campanato, or Morrey-space generalizations.
- A package that assumes the desired representative or estimate as an unconstrained field.

The similarly scoped `THM-M-1237` dossier and historical `S1_M_175.lean` are discovery inputs only.
They do not identify this target's exact statement and provide no inherited acceptance or proof
credit.

