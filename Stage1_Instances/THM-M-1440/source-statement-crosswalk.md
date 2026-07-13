# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10518-10523` supplies exactly the title `牛顿迭代法`, attribution
to Isaac Newton, the year 1669, the gloss `方程求根的二次收敛方法`, importance "high," and status
`已验证`. All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, source edition,
theorem/page locator, formula, quantified statement, assumptions, proof, errata, reviewer, or
formal artifact. The attribution and date are therefore unverified catalog metadata, not a
historical theorem locator.

`Docs/Stage0_Blueprint.md:39163-39189` is a generated projection. It repeats the gloss and metadata
while explicitly leaving the exact definitions and premises, proof route, dependencies, alternate
forms, axioms, machine status, and artifact links open. Its generic closed-result and theorem-tree
language is workflow metadata, not independent source evidence. Rev-5.6 retains `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Material interpretations | Required Lean component | Intake result |
|---|---|---|---|
| `方程求根` (finding roots) | solve `f(a) = 0` over reals, complexes, or a normed space | carrier, function, root, equality and derivative notions | all unspecified |
| `牛顿迭代法` | `x_(n+1) = x_n - f(x_n) / f'(x_n)` or a Fréchet-derivative analogue | update map, initial point, recurrence, nonzero/invertible derivative and invariant domain | formula and well-definedness absent |
| `二次收敛` | one-step error bound, eventual Q-order two, positive finite asymptotic ratio, or big-O | exact sequence/error predicate, norm, constants, quantifier order | meaning not selected |
| `方法` | mathematical iteration or finite-precision algorithm | one truth-valued convergence/correctness theorem | no exact conclusion supplied |
| `已验证` | untrusted screening label | accepted source and kernel receipts | no credit |

The ambiguity is substantive. For `f(x) = x^2` at the multiple root zero, nonzero Newton iterates
satisfy `x_(n+1) = x_n / 2`, which is linear rather than quadratic. The update is also undefined in
the classical field formula wherever `f'(x_n) = 0`. Thus a root-multiplicity/nondegeneracy premise
and an iteration well-definedness argument cannot be silently omitted.

## Pinned Lean boundary

Pinned mathlib module `Mathlib.Dynamics.Newton` defines `Polynomial.newtonMap` over commutative
rings using a junk-value convention at nonunits. It proves the Newton formula under a unit
derivative, root-to-fixed-point results, nilpotent divisibility growth, and a nilpotent-root
existence/uniqueness result. Those are useful neighboring interfaces but not a local analytic
quadratic-convergence theorem for exact Newton root iteration.

A bounded search of repo-local Lean and pinned mathlib found no declaration whose statement matches
the catalog's missing quadratic-convergence claim. This is intake discovery only, not the later
immutable anchor audit and not a proof of global absence. The API probe states no target theorem
and gives no statement or proof credit.

## Neighbor boundaries

The catalog separately owns secant method (`THM-M-1441`), bisection (`THM-M-1442`), generic fixed-
point iteration (`THM-M-1443`), Banach fixed-point theorem (`THM-M-1444`), and Hessian-based Newton
optimization (`THM-M-1500`). Their statements and artifacts cannot be substituted for or credited
to this root-finding convergence target.

## Source gate and retry condition

An accountable correction must cite an immutable approved edition and exact theorem/page, select
one truth-valued Newton convergence theorem, map every definition, binder, premise, conclusion and
boundary case, audit corrections and historical attribution, and receive independent source
review. Only then may the statement phase freeze a Lean expression, checked transports, and the
required removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations.
