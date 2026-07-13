# Scope map

## Received scope

The catalogue fixes only the title `弗里德里希斯不等式`, the gloss
`紧支集Sobolev函数的估计`, the attribution Kurt Friedrichs, the year 1929, and an untrusted
`已验证` label. In the catalogue this record lies in real analysis. Stage0 repeats it while leaving
the precise definitions and premises, proof, dependencies, equivalent forms, logical principles,
and machine artifact open.

Those words constrain the target to a Friedrichs-type analytic estimate involving compact support
and Sobolev regularity. They do not determine either side of an inequality or a truth-valued
proposition. The following is therefore a decision boundary, not a guessed theorem.

## Decisions required at statement freeze

An immutable source and independent review must fix:

1. The scalar field, ambient dimension and space, domain, measure, and whether the domain is open,
   bounded, connected, Lipschitz, convex, or otherwise regular.
2. The function model: `C_c^1`, `C_c^2`, `W^{1,p}`, `W_0^{1,p}`, smooth functions with bounded
   support, and weakly differentiable representatives are not interchangeable.
3. Whether support is compact in the ambient space, compactly contained in the domain, merely
   bounded, or replaced by a zero-trace condition, together with the exact transport if two forms
   are related.
4. The exponent or exponents and endpoints, including whether the same `p` occurs on both sides or
   a Sobolev-conjugate exponent occurs.
5. The weak derivative, gradient or Frechet derivative, vector norm, `L^p` norm and measure
   conventions, inequality direction, and every parameter on which the constant depends.
6. Whether the theorem asserts existence of a finite positive constant, supplies an explicit or
   optimal constant, includes a boundary term, or states norm equivalence.
7. Treatment of empty, singleton, disconnected, unbounded, zero-measure, and irregular domains;
   constant functions; support touching the boundary; endpoint exponents; and infinite norms.
8. Ordered binders, universes, coercions, almost-everywhere equivalence, representative choices,
   and all typeclass assumptions in the eventual Lean encoding.

## Candidate branches not credited

- A bounded-support estimate `norm u <= C * norm (gradient u)` with the same exponent on both
  sides.
- A compact-support Sobolev-conjugate estimate with different exponents.
- A zero-trace `W_0^{1,p}` inequality on a bounded domain.
- A boundary-term inequality or norm-equivalence result on a Lipschitz domain.
- The historical two-dimensional smooth-function formulation identified by a secondary source.

No branch is selected, asserted, or credited at intake. Formula fragments above only distinguish
the proposition-changing choices that an exact source must settle.

## Duplicate and substitution boundaries

`THM-M-1240` repeats the same attribution, year, gloss, importance, and untrusted status under the
Latin-spelled title `Friedrichs不等式` in the PDE category. It remains a separate rev-5.6 target.
No source identity, alias, distinct formulation, terminal-body ownership, or metric-credit decision
has been accepted, so its dossier and any future evidence cannot be inherited here.

`THM-M-0305` is the separately catalogued real-analysis Poincare inequality. Also excluded as
unreviewed substitutions are a mean-zero Poincare inequality, a general Sobolev embedding, a
Hilbert-space coercivity estimate, a trace theorem, an inequality obtained by assuming the desired
estimate, or a structure field containing the conclusion.

## Lean boundary

Pinned mathlib contains `Mathlib.Analysis.FunctionalSpaces.SobolevInequality`. Its checked
declarations bound `eLpNorm` by an `eLpNorm` of the Frechet derivative for compactly supported or
bounded-support continuously differentiable functions on finite-dimensional real normed spaces.
One same-exponent result is close to the catalogue gloss, while other results use conjugate
exponents. Mathlib calls the family Gagliardo-Nirenberg-Sobolev and does not resolve the catalogue's
domain, support/trace, exponent, or historical-source choices. These declarations provide `M3`
statement/interface discovery only, not an exact target, checked transport, proof of THM-M-0306,
or downstream anchor audit.
