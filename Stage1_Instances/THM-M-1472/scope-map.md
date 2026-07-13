# Scope map

## Preserved theorem-family scope

The repository preserves a recognizable numerical-analysis theorem family, not a binder-complete
claim. The standard Lax-Richtmyer setting concerns a properly posed linear initial-value problem
and a linear finite-difference approximation. Modern generalizations instead use abstract normed
solution and data spaces, continuous and discrete solution operators, restriction maps, and a
refinement family. Those formulations are related, but they are not definitionally interchangeable.

The catalog slogan also compresses directionality. A common sufficiency statement is
`consistent and stable implies convergent`; the classical word "equivalence" may instead express
that, for a consistent approximation to a well-posed linear problem, stability is necessary and
sufficient for convergence. Encoding the typography as the propositional tautology
`(Stable ∧ Consistent) ↔ Convergent`, or using arbitrary `Prop` parameters, would discard all
numerical content and is excluded.

## Decisions required at statement freeze

1. Select an immutable source edition and exact result: the 1956 Lax-Richtmyer theorem, a
   source-approved restatement, or a later general equivalence theorem.
2. Fix the continuous problem: scalar field, solution and data spaces, operator domain and range,
   linearity, well-posedness, solution operator, initial and boundary data, forcing, and time span.
3. Fix the approximation family: admissible step sizes or directed refinement filter, discrete
   spaces, difference operator, solvability, inverse/solution operator, restriction or prolongation
   maps, and their uniform bounds.
4. Define consistency exactly: pointwise or uniform, operator or truncation error, dense core,
   order/rate if any, norm, filter, and quantifier order.
5. Define stability exactly: inverse/operator/propagation stability, norm, time horizon, uniformity
   in step and time indices, and permitted dependence of the stability constant.
6. Define convergence exactly: data class, solution comparison map, norm or topology, pointwise or
   uniform mode, finite- or infinite-time scope, and whether a rate is concluded.
7. Settle whether the target proves sufficiency only, necessity only, or a checked equivalence, and
   which consistency and well-posedness assumptions are shared by the directions.
8. Freeze ordered binders, hypotheses, boundary cases, foundation/TCB/computation profiles,
   minimal imports, expression/environment fingerprints, checked transports, and mutations.

## Boundary cases

The statement phase must decide zero and nonpositive step sizes, whether zero is excluded from the
step set and is its unique accumulation point, empty or singleton refinement sets, zero-dimensional
spaces, trivial operators, singular discrete systems, exact and zero solutions, zero time horizon,
one-step versus multistep initialization, non-dense consistency cores, unbounded restriction maps,
nonuniform constants, infinite-time growth, incompatible initial/boundary data, and exact versus
floating-point arithmetic. No case is excluded at intake.

Assuming the desired convergence or stability conclusion as a structure field is circular. A
scheme-specific residual, plot, convergence table, or finite computation cannot replace the
quantified theorem.

## Neighbor and substitution exclusions

- `THM-M-1465` owns the broad finite-difference-method label. A particular stencil or method
  theorem cannot silently become this equivalence result.
- `THM-M-1471` a priori error estimates, `THM-M-1473` the CFL condition, and `THM-M-1474` von
  Neumann stability analysis are distinct targets and provide no inherited proof credit.
- `THM-M-0329` Lax-Milgram, `THM-M-1201`/`THM-M-1202` Lax entropy results, and
  `THM-M-1550`/`THM-M-1551` Lax-pair results share a name only.
- The 1985 Sanz-Serna-Palencia generalized discretization theorem and the 2021 Coq statement
  cannot replace the 1956 formulation without an accepted source decision and checked transport.
- Banach-Steinhaus, operator-norm inequalities, generic limit lemmas, and squeeze arguments are
  substrate, not a finite-difference equivalence theorem.

## Formal and execution boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`ContinuousLinearMap.le_opNorm`, `banach_steinhaus`, and standard limit/squeeze APIs are available.
A bounded topic search found no exact Lax-Richtmyer or Lax equivalence declaration in pinned
mathlib or the repository-local Lean sources. This is intake discovery, not the required exhaustive
anchor audit and not a global absence proof.

The public Coq artifact at `mohittkr/Lax_equivalence` is a credible external formal lead, but its
source mapping, exact theorem type, dependency closure, axioms, placeholders, build, and relation to
the eventual Lean target belong to downstream audits. It is not a pinned Lean dependency and earns
no `M0` or `M1` classification at this intake. Statement selection must occur before obligation-tree
or proof work.
