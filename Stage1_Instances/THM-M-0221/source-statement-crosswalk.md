# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1598-1603` supplies exactly the title `柯西积分定理`, Augustin
Cauchy, 1825, the gloss `全纯函数沿闭曲线的积分为零` ("the integral of a holomorphic function along
a closed curve is zero"), high importance, and status `已验证`. All six uncited lines originate in
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, theorem locator,
formula, definitions, premises, proof, corrections, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:6140-6165` repeats the gloss while explicitly leaving the formal system,
foundation, precise definitions and premises, proof route, dependencies, equivalent formulations,
axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Truth and ambiguity check

The gloss cannot be accepted literally as a universal statement. Let `U = Complex \ {0}` and
`f z = 1 / z`. The function is holomorphic on `U`, but the pinned theorem
`circleIntegral.integral_sub_center_inv` computes its integral around the positively oriented unit
circle as `2 * pi * I`. Therefore a domain, interior, homotopy, winding, or primitive hypothesis is
missing. Which repair represents the catalog target is a source question and cannot be decided by
choosing whichever Lean declaration is easiest.

## Inspected modern source lead

Elias M. Stein and Rami Shakarchi, *Complex Analysis*, Princeton Lectures in Analysis II,
Princeton University Press, 2003, ISBN 978-0-691-11385-2, was inspected through the publisher-hosted
Chapter 2 PDF on 2026-07-13. The observed PDF SHA-256 was
`f2b4abefa97631084ee40ef77e18523d6599441e3726aa9a94cbf4595596d25b`.

At printed pages 32-33, Chapter 2 states Cauchy's theorem loosely for a function holomorphic on an
open set and a closed curve whose interior also lies in the set, immediately warning that a precise
general formulation requires defining the curve's interior. Theorem 1.1 on printed page 34 gives
the triangle form. Theorem 2.2 and Corollary 2.3 on printed page 39 give the disk and circle forms;
the text then treats toy contours and defers general piecewise-smooth curves.

This is a strong authoritative modern source lead and supports provisional H1. It is not catalog-
cited or the historical 1825 source, and its loose overview does not choose one root for this
dossier. The publisher-hosted bytes are mutable and not repository-preserved; a complete pinpoint
definition, assumption, proof-node, correction/errata and independent-review packet is absent. It
therefore supplies no H0 receipt.

## Clause crosswalk

| Catalog phrase | Missing mathematical decision | Prospective Lean surface | Intake status |
|---|---|---|---|
| "holomorphic function" | scalar or Banach-valued; domain and boundary regularity | `DifferentiableOn Complex f U`, `DiffContOnCl`, or source-selected equivalent | codomain and exact predicate open |
| "closed curve" | path type, regularity, endpoints, self-intersections, orientation | `Path a a`, circle parametrization, rectangle boundary, or a cycle | object and regularity open |
| "along" | curve image only or a filled-region/neighborhood condition | `Set.range gamma subset U`, disk/rectangle containment, or homotopy image containment | essential missing premise |
| "integral" | scalar contour integral or one-form curve integral | interval expression, `circleIntegral`, or `curveIntegral` | transport and integrability open |
| "equals zero" | which family of curves/cycles and under which topology | equality in `Complex` or a complex Banach space | exact quantifier scope open |
| `已验证` | untrusted inventory label | source review and kernel receipts would be required | no H or M credit |

## Pinned Lean candidates

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides:

- `Mathlib.Analysis.Complex.CauchyIntegral`:
  `Complex.integral_boundary_rect_eq_zero_of_differentiable_on_off_countable`,
  `Complex.integral_boundary_rect_eq_zero_of_continuousOn_of_differentiableOn`, and
  `Complex.integral_boundary_rect_eq_zero_of_differentiableOn` prove restricted rectangle-boundary
  Cauchy-Goursat statements. `Complex.circleIntegral_eq_zero_of_differentiable_on_off_countable`
  and `DiffContOnCl.circleIntegral_eq_zero` prove restricted circle forms.
- `Mathlib.Analysis.Complex.HasPrimitives`: `Complex.IsExactOn` encodes existence of a primitive;
  `DifferentiableOn.isExactOn_ball` and `Differentiable.isExactOn_univ` provide disk and entire
  primitive results. The module explicitly marks the simply-connected-domain extension as TODO.
- `Mathlib.MeasureTheory.Integral.CurveIntegral.Basic` defines `curveIntegral` for `Path`s.
  `Mathlib.MeasureTheory.Integral.CurveIntegral.Poincare` proves equality of curve integrals across
  a suitably smooth homotopy for a closed one-form and exactness on convex sets. Applying it to a
  holomorphic integrand would require an explicit one-form adapter and all homotopy/regularity
  obligations.
- `circleIntegral.integral_sub_center_inv` formalizes the punctured-plane counterexample integral.

These exact declarations justify provisional M3 because usable pinned theorem and interface
candidates exist. None receives root proof credit: the source root is not selected, normalized
statement identity and transports are absent, and the later immutable anchor, terminal-body,
provenance, trust, and dependency audits have not run.

The repo-local legacy `AwesomeTheorems.Stage1.S1_M_178.cauchy_integral_formula_anchor` is an
adjacent Cauchy integral formula wrapper, not the zero-integral theorem, and belongs to another
target surface. No status or proof credit transfers.

## Source and statement gate

Before leaving H1, reviewers must preserve and approve one exact source assertion and all
incorporated definitions, binders, assumptions, proof nodes, corrections, and errata, reconcile it
with the catalog's false literal reading and historical attribution, and independently approve the
mapping. Only then may the statement phase select minimal imports, elaborate and hash that same
claim, compile transports, and mutation-test removed hypotheses, changed domains, binder scope,
and boundary cases.
