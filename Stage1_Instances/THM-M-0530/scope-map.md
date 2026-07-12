# Scope map

## Provisional included family

- A topological space `X` and an as-yet unselected coefficient object, provisionally an abelian
  group `G`.
- Ordinary singular cochains formed contravariantly from singular chains, with cohomology groups
  `H^n(X; G)` obtained from cocycles modulo coboundaries.
- Maps on cohomology induced contravariantly by continuous maps.
- Invariance under homeomorphism as the weakest direct reading of "topological invariant".
- Homotopy invariance as a separate candidate root only if the selected primary source shows that
  the repository phrase was intended to assert it.

## Decisions required at statement freeze

The statement phase must select and inspect an exact primary theorem, then freeze ordinary versus
reduced, relative, compact-support, Cech, cellular, sheaf, or generalized cohomology; coefficients
and their algebraic structure; `Nat` versus `Int` grading; variance and binder order; based versus
unbased spaces; the map class; and whether the conclusion is equality, an induced isomorphism, or
a naturally isomorphic functor. It must also settle the empty space, degree zero, negative degrees,
the one-point space, non-Hausdorff spaces, and coefficient-zero cases.

## Explicit exclusions

- Treating the definition of a cohomology group as though it were itself a theorem.
- Substituting the universal coefficient theorem (`THM-M-0531`), a Kunneth theorem, Poincare or
  Alexander duality, de Rham's theorem, or a sheaf-cohomology theorem.
- Replacing topological singular cohomology with group, Galois, Lie-algebra, or derived-functor
  cohomology merely because a Lean API exists.
- Assuming an abstract `Cohomology : Nat -> Type` or an isomorphism field and then projecting the
  desired conclusion.
- Crediting the repository label `已验证` as either human-source evidence or kernel evidence.

No Lean target is frozen at intake. The later statement must expose a concrete cochain complex,
cohomology object, induced map, and selected invariance relation, or record a precise missing-API
blocker without weakening or broadening the claim.
