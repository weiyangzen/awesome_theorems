# Scope map

## Preserved source scope

The repository fixes the title `法图定理`, Pierre Fatou, the year 1906, the complex-analysis
category, and the gloss `单位圆盘内全纯函数的径向极限` ("radial limits of holomorphic functions
in the unit disk"). It supplies no citation, definitions, ordered binders, hypotheses, conclusion,
exceptional set, proof boundary, or formal artifact. This intake preserves only the classical
Fatou boundary-limit family and does not silently complete the missing proposition.

## Proposition-changing decisions

An approved statement phase must admit an immutable pinpoint source and freeze:

- the open unit disk representation and whether the analytic function is modeled on `ℂ`, a
  subtype, or another source-specified carrier;
- the essential size hypothesis: bounded analytic, a specified `H^p` class and exponent range,
  a Poisson integral of boundary data, or another exact source condition;
- the boundary carrier and measure, including angle interval or quotient-circle representation,
  endpoint identification, ordinary versus normalized Lebesgue/Haar measure, and measurability;
- radial convergence versus nontangential or unrestricted approach, with the exact one-sided
  filter as the radius tends to `1` from below;
- whether the conclusion supplies a finite complex limit, an extended limit, a boundary function,
  membership of that function in an `L^p` class, or convergence in an additional norm;
- whether the result is only almost everywhere, the precise null exceptional set, and whether one
  exceptional set must work for several asserted properties; and
- all scalar, exponent, representative, equality-almost-everywhere, endpoint, zero-function, and
  other boundary conventions.

These choices are not interchangeable. This list is a resolution checklist, not a canonical
statement.

## Candidate families not credited

- A bounded holomorphic function on the unit disk has finite radial limits almost everywhere on
  the unit circle.
- A specified analytic Hardy-class function has radial or nontangential boundary values almost
  everywhere, possibly with an `L^p` boundary or convergence conclusion.
- A Poisson integral of integrable boundary data converges at almost every boundary point.
- A harmonic-function or real/imaginary-part formulation transported to a holomorphic statement.

No candidate above is selected, source-crosswalked, or credited at intake.

## Explicit exclusions

This target must not be replaced by measure-theoretic Fatou's lemma, the complex-dynamical Fatou
set (`THM-M-1429`), Abel's theorem at one boundary point, a Cauchy or Poisson reproduction formula,
or a generic limit statement. It must not become the false unrestricted claim that every
holomorphic function on the unit disk has the intended almost-everywhere finite radial limit. A
finite polynomial, constant function, or structure carrying its boundary limit as an assumption is
not a substitute for the theorem.

The adjacent pinned unit-disc, circle-map, analytic, filter, and measure APIs are encoding
ingredients only. Their existence does not select a source theorem, establish statement identity,
or supply a proof body.

## Downstream boundary

The next phase must obtain and independently review the exact source passage before fixing ordered
binders, hypotheses, conclusion, canonical Lean expression, minimal imports, transports, or the
four required mutation classes. Obligation construction and proof search remain downstream of
that statement gate.
