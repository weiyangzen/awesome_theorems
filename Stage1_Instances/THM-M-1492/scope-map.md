# Scope map

## Preserved scope

The repository supports only the topic family "linear programming" together with the phrase
"optimization of a linear objective function." A conventional finite-dimensional program might
optimize `c^T x` subject to linear equalities or inequalities and sign restrictions. That template
is useful for exposing omitted choices, but it is not an accepted theorem statement.

## Decisions required at statement freeze

1. The truth-valued root: existence or attainment of an optimum, an infeasible/unbounded/optimal
   trichotomy, optimality at a basic feasible solution or extreme point, weak or strong duality,
   complementary slackness, a certificate theorem, or correctness or complexity of an algorithm.
2. Whether the objective is minimized or maximized and whether data are presented in standard,
   canonical, inequality, equality, geometric, or conic form.
3. The finite- or infinite-dimensional decision carrier, scalar field or ordered coefficient type,
   index types, universes, matrix/linear-map representation, and required order/topology instances.
4. The objective coefficients and value codomain, including whether extended values represent
   infeasibility or unboundedness.
5. Equality and inequality constraints, comparison direction, right-hand sides, nonnegativity or
   free-variable convention, and the exact feasible-set definition.
6. Every ordered binder and hypothesis, including finiteness, nonemptiness, feasibility,
   boundedness, compactness, closedness, nondegeneracy, rationality, or constraint qualification.
7. The exact conclusion and witness data: optimum value only, an optimizer, an extreme/basic
   feasible optimizer, dual variables, a separating certificate, or an algorithm output.
8. Boundary behavior for no variables or constraints, empty feasible sets, redundant or
   inconsistent constraints, zero objective, unbounded objective, unattained infimum/supremum,
   multiple optima, rank deficiency, and infinite values.
9. An immutable primary source edition with theorem/page locator, incorporated definitions,
   assumptions, proof boundary, corrections or errata, translation policy, and independent review.

## Explicit exclusions

- Do not choose LP strong duality, the fundamental theorem of linear programming, an attainment
  theorem, Farkas' lemma, or an infeasible/unbounded/optimal alternative merely because it is
  familiar.
- Do not substitute `THM-M-1491` (convex optimization), `THM-M-1493` (simplex method),
  `THM-M-1494` (interior-point method), `THM-M-1495` (ellipsoid method), or `THM-M-1507`
  (Lagrangian duality), and do not inherit evidence from those targets.
- Do not turn a general optimization or conic theorem into the root without an approved
  source-identity bridge, and do not replace the family with a one-dimensional or unconstrained
  special case.
- Do not encode the missing result as an assumption, opaque predicate, certificate field, axiom,
  or existential witness projected directly from a hypothesis.
- Do not treat generic convexity/separation infrastructure, the meta simplex oracle, the catalog
  label `已验证`, or a successful API probe as an LP theorem or proof.

## Prospective proof-route boundary

After a source-approved proposition is selected, common proof routes might use polyhedral
geometry and extreme points, Farkas separation and dual certificates, or a source-specific
algorithm invariant. These are possible obligation-tree seeds only. No obligation registry,
alternate encoding, proof route, or closure credit is frozen during intake.
