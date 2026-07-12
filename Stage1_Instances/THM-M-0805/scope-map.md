# Scope map

## Included topic boundary

- Infinite two-player perfect-information games used in the intended formulation of AD.
- The exact ambient real space, payoff sets, strategies, and winning convention.
- A source-specified projective pointclass or level, including parameter conventions.
- One exact source-stated consequence, with every foundation and choice assumption explicit.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different claims such as:

1. AD itself, formulated as determinacy of every length-omega game on naturals.
2. Determinacy restricted to all projective sets or to a specified projective level.
3. Under AD, a regularity property for projective sets, such as measurability, the Baire property,
   or the perfect-set property.
4. Under AD or a stronger hypothesis, a uniformization, scale, prewellordering, or closure theorem
   for a specified projective pointclass.

The statement phase must locate an immutable source and freeze one proposition. It must specify the
base theory (for example ZF plus any dependent-choice fragment), the coding of reals and games,
boldface versus lightface and parameters, the projective level, all binders and hypotheses, and the
single conclusion. It must not silently import full choice into a claim whose content depends on
the failure of choice.

## Explicit exclusions

- Borel determinacy, analytic determinacy, or determinacy of finite games as substitutes for AD.
- A theorem merely about analytic sets, descriptive trees, or Polish spaces.
- The algebraic-geometric meaning of "projective".
- Treating a list of unrelated consequences as one conjunction without a source.
- Defining the desired property as assumed data and proving a tautological projection.
- The repository label `已验证` as evidence of a human or machine proof.

No canonical Lean target is frozen at intake because the source record does not identify one.
