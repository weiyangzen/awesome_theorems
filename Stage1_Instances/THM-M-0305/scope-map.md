# Scope map

## Received scope

The catalogue fixes only the title `庞加莱不等式`, the gloss `Sobolev函数的L^p估计`, the
attribution Henri Poincare, the year 1890, and an untrusted `已验证` label. In the catalogue this
record lies in real analysis. Stage0 repeats it while leaving the precise definitions and premises,
proof, dependencies, equivalent forms, axioms, and machine artifact open.

Those words constrain the target to an analytic Poincare-type estimate involving Sobolev
regularity and an `L^p` quantity. They do not determine the two sides of the inequality or a
truth-valued proposition. The following is therefore a decision boundary, not a guessed theorem.

## Decisions required at statement freeze

An immutable source and independent review must fix:

1. The scalar field, ambient dimension, domain, measure, and whether the domain is open, bounded,
   connected, Lipschitz, convex, or otherwise regular.
2. The Sobolev model and function class: `W^{1,p}`, `W_0^{1,p}`, locally Sobolev, smooth dense
   representatives, or compactly supported continuously differentiable functions are not
   interchangeable.
3. The exponent or exponents, their ranges and endpoints, and whether the same `p` occurs on both
   sides or a Sobolev-conjugate exponent appears.
4. The normalization removing constants: subtraction of a mean, zero mean, zero trace, compact
   support, a fixed value, or a quotient by constants.
5. The weak derivative or gradient, vector norm, `L^p` norm convention, inequality direction,
   constant, and every parameter on which that constant may depend.
6. Whether the result asserts one fixed constant, existence of a domain-dependent constant, a
   best constant, equality cases, or a spectral characterization.
7. Treatment of disconnected, unbounded, empty, singleton, zero-measure, and irregular domains;
   constant functions; zero trace; endpoint exponents; and infinite norms.
8. Ordered binders, universes, coercions, almost-everywhere equivalence, representative choices,
   and all typeclass assumptions in the eventual Lean encoding.

## Candidate branches not credited

- A mean-subtracted bound of the form `norm (u - average u) <= C * norm (gradient u)` on a
  bounded connected regular domain.
- A zero-trace or compact-support bound of the form `norm u <= C * norm (gradient u)`.
- A one-dimensional interval/Wirtinger specialization.
- A best-constant or first-eigenvalue formulation.
- A compact-support Gagliardo-Nirenberg-Sobolev estimate with different exponents.

No branch is selected, asserted, or credited at intake. Formula fragments above only distinguish
the choices that an exact source must settle.

## Duplicate and substitution boundaries

`THM-M-1239` repeats the same attribution, year, gloss, importance, and untrusted status under the
Latin-spelled title `Poincaré不等式` in the PDE category. It remains a separate rev-5.6 target.
No source identity, alias, distinct formulation, terminal-body ownership, or metric-credit decision
has been accepted, so its dossier and any future evidence cannot be inherited here.

`THM-M-0998` has the distinct probability gloss "variance upper bound". Its variance/Dirichlet
form model cannot substitute for this Sobolev/real-analysis target. Also excluded as unreviewed
substitutions are Friedrichs' inequality, a generic Sobolev embedding, an inequality obtained by
assuming the desired estimate, or a structure field that contains the conclusion.

## Lean boundary

Pinned mathlib contains `Mathlib.Analysis.FunctionalSpaces.SobolevInequality`. Its checked
declarations bound `eLpNorm` by an `eLpNorm` of the Frechet derivative for compactly supported or
bounded-support continuously differentiable functions on finite-dimensional normed spaces. These
are adjacent feasibility interfaces and could match one source-selected branch, but the catalogue
does not select that branch and the module calls its results Gagliardo-Nirenberg-Sobolev
inequalities. They provide `M3` statement/interface discovery only, not an exact target, transport,
proof of THM-M-0305, or downstream anchor audit.
