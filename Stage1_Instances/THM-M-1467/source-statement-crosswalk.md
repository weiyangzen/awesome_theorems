# THM-M-1467 source-statement crosswalk

## Repository record

The source inventory at `Docs/researches/math_theorems.md:10707-10712` contains exactly:

- title: `谱元法` (spectral element method);
- proposer: `Anthony Patera`;
- time: `1984`;
- statement gloss: `谱方法与有限元的结合` (combination of spectral methods and finite
  elements);
- importance: high; and
- formalization status: `已验证` (verified).

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, formula, domain,
mesh, spaces, assumptions, conclusion, proof, formal declaration, or validation link. The Stage0
projection at `Docs/Stage0_Blueprint.md:39892-39917` repeats the gloss while explicitly leaving
definitions and premises, proof route, dependencies, equivalent forms, axioms, machine status, and
artifact links open. Rev-5.6 treats the verified label as untrusted metadata.

## Literal crosswalk

| Repository phrase | Material ambiguity | Required exact component | Intake status |
|---|---|---|---|
| `谱元法` | a method family, not a conclusion | equation/problem, discretization, result | open |
| `谱方法` | modal/nodal basis, approximation, Galerkin, collocation, or quadrature | basis, nodes, degree, residual formulation | open |
| `有限元` | mesh, element maps, local spaces, conformity, assembly | geometry, spaces, degrees of freedom, interfaces | open |
| `结合` | many inequivalent hybrids and no logical connective | exact construction and theorem relating its components | open |
| `Anthony Patera` / `1984` | historical metadata without a cited work or locator | immutable source identity, statement, proof, corrections | open |
| `已验证` | catalog inventory label only | no human or machine evidence | explicitly untrusted |

These rows do not determine ordered binders, hypotheses, or one conclusion. The canonical human
statement and Lean expression therefore remain null.

## Bibliographic lead, not an admitted proposition

Crossref metadata was inspected for Anthony T. Patera, “A spectral element method for fluid
dynamics: Laminar flow in a channel expansion,” *Journal of Computational Physics* 54(3), June
1984, pages 468-488, DOI `10.1016/0021-9991(84)90128-1`. This aligns with the catalog's author,
date, and topic. The inspected metadata contains no abstract or theorem text. The article body,
exact equations and algorithms, theorem or formula locator, assumptions, proof boundary,
corrections, intended catalog-root selection, and independent review were not admitted. The paper
is therefore a source-family lead only, not `H0`, a canonical statement, or proof evidence.

## Candidate source-to-statement rows

| Candidate family | Source components that must be fixed | Lean obligations if selected | Current boundary |
|---|---|---|---|
| discrete well-posedness | PDE, spaces, form, mesh, degree, quadrature, coercivity or inf-sup | finite-dimensional space/operator and exact existence/uniqueness bridge | no source proposition |
| best approximation | energy form, conforming subspace, exact/discrete solutions, constants | orthogonality and composition to a norm estimate | overlaps Galerkin/FEM neighbors |
| interpolation error | reference element, nodes, maps, regularity, norm, `h`/`p` scaling | polynomial operator, transport, local-to-global estimate | no selected estimate |
| spectral convergence | analytic or Sobolev class, mesh family, degree regime, constants | quantified approximation and discretization-error composition | no selected rate |
| quadrature stability/error | nodes, weights, exactness, positivity, aliasing, modified form | exact quadrature model and perturbation bound | Chebyshev API is only substrate |
| solver correctness | assembly, representation, arithmetic, solver, tolerance | executable semantics, certificates, rounding/stability composition | no computation contract |

These are resolution rows for a later source and statement review, not inherited clauses.

## Pinned formal substrate, not a root anchor

The bounded intake search used pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Relevant checked declarations include
`IsCoercive.continuousLinearEquivOfBilin`, `Submodule.starProjection_minimal`,
`Polynomial.Chebyshev.integral_eval_T_real_mul_eval_T_real_measureT_of_ne`, and
`Polynomial.Chebyshev.integral_eq_sumZeroes`. They respectively expose coercive variational,
best-projection, polynomial-orthogonality, and exact-quadrature substrate. None supplies element
geometry, local polynomial spaces, assembly, interface conditions, a discrete PDE, or a
source-identical spectral-element conclusion. `IntakeProbe.lean` elaborates interfaces only and
adds no theorem or proof body. No root machine status is credited.

## Gate result

Human status is provisionally `H5`: the received target is a method-family gloss rather than one
stable proposition. Machine status is `M4`: no usable source-identical formal root has been located;
adjacent checked interfaces are not the target. Readability status is `R4`: this boundary record is
not a readable proof of an exact theorem. Retry requires an accountable immutable source selection
and independent review fixing every proposition-changing row before exact statement elaboration.
