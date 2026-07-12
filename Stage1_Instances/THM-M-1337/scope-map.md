# Scope map

## Received scope

The repository fixes the name `Gronwall不等式`, attributes it to Thomas Gronwall in 1919, and
glosses it only as `微分不等式的积分形式` ("integral form of a differential inequality"). It does
not give a formula, source locator, definitions, assumptions, or conclusion. The `已验证` label is
explicitly untrusted under rev-5.6.

## Candidate mathematical boundary

An eventual exact target may be an integral Gronwall inequality only after a reviewed source fixes:

- the scalar ordered codomain or a norm-valued reduction, and whether the bounded function is
  pointwise nonnegative;
- the time domain, orientation, base point, closed or half-open endpoints, and quantifier order;
- continuity, measurability, local integrability, absolute continuity, or almost-everywhere
  hypotheses on every function;
- a constant or time-varying coefficient, its sign and integrability, and the integral convention;
- a constant initial bound, a nondecreasing inhomogeneous term, or additive forcing;
- whether the premise is pointwise, almost everywhere, derivative-based, right-Dini based, or an
  actual integral inequality; and
- the exact exponential conclusion, constant dependencies, exceptional sets, and endpoint cases.

The familiar scalar pattern

```text
u(t) <= A + integral(a, t, fun s => b(s) * u(s))
```

with a conclusion involving `A * exp(integral(a, t, b))` is a candidate family member, not the
canonical statement. Recording it here does not choose its domains, assumptions, or variants.

## Variant decisions required

1. Classical Gronwall versus the later Gronwall-Bellman integral formulation and their exact
   source genealogy.
2. Scalar inequality versus a normed-space theorem derived through the norm.
3. Constant coefficient `K` versus a variable coefficient `b(t)`.
4. Homogeneous bound versus constant additive forcing or a nondecreasing inhomogeneous function.
5. Integral premise versus differentiable, right-derivative, Dini-derivative, or liminf-slope
   premise, including the direction and hypotheses of any transport.
6. Pointwise regularity versus almost-everywhere inequalities and Bochner/Lebesgue integration.
7. The behavior when the interval is empty or reversed, `a = b`, `K = 0`, the initial bound is
   zero, or coefficients/functions change sign.

These choices change the proposition and cannot be resolved merely by selecting the easiest Lean
declaration.

## Explicit exclusions

- Bihari-LaSalle's nonlinear generalization, which is separately cataloged as `THM-M-1338`.
- A discrete sequence inequality or recurrence.
- Only an ODE uniqueness, continuous-dependence, comparison, trajectory-distance, or zero-solution
  corollary.
- Pinned mathlib's constant-coefficient derivative/right-slope results as the exact integral target
  without a source-approved, kernel-checked statement bridge.
- An abstract package containing the desired bound as a hypothesis or field.
- A numerical experiment, informal calculus derivation, theorem name, or catalog status as proof
  evidence.

## Formal boundary

No canonical Lean expression is frozen at intake. Pinned mathlib module
`Mathlib.Analysis.ODE.Gronwall` provides `gronwallBound`,
`le_gronwallBound_of_liminf_deriv_right_le`, and
`norm_le_gronwallBound_of_norm_deriv_right_le`. Those declarations establish relevant API
feasibility only. The module itself describes them as Gronwall-like derivative/right-slope bounds
and leaves a variable-coefficient extension as TODO work; a pinned-package search found no
integral-hypothesis theorem under the Gronwall name. Exact imports, expression fingerprint,
alternate transports, and statement mutations belong to the dependent statement phase.
