import «Statement»

/-!
Negative elaboration test input.  This file must fail: each `rfl` tries to
identify the frozen target with a semantically altered statement.
-/

namespace Stage1.THM_M_0423.Mutations

universe u v

open Stage1.THM_M_0423

private def RemovedNondegeneracy : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (V : Type v) [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    (Q : QuadraticForm K V),
      IsIsotropic Q ↔
        IsIsotropicAtEveryFinitePlace Q ∧ IsIsotropicAtEveryInfinitePlace Q

example : HasseMinkowskiStatement.{u, v} = RemovedNondegeneracy.{u, v} := rfl

private def RationalDomainOnly : Prop :=
  ∀ (V : Type v) [AddCommGroup V] [Module ℚ V] [FiniteDimensional ℚ V]
    (Q : QuadraticForm ℚ V),
    Q.Nondegenerate → IsIsotropic Q

example : HasseMinkowskiStatement.{u, v} = RationalDomainOnly.{v} := rfl

private def ChangedBinderScope : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (V : Type v) [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    (Q : QuadraticForm K V),
      (Q.Nondegenerate → IsIsotropic Q) ↔
        IsIsotropicAtEveryFinitePlace Q ∧ IsIsotropicAtEveryInfinitePlace Q

example : HasseMinkowskiStatement.{u, v} = ChangedBinderScope.{u, v} := rfl

private def AllowsZeroVector
    {K : Type u} {V : Type v} [CommRing K] [AddCommGroup V] [Module K V]
    (Q : QuadraticForm K V) : Prop :=
  ∃ x : V, Q x = 0

example {K : Type u} {V : Type v} [CommRing K] [AddCommGroup V] [Module K V]
    (Q : QuadraticForm K V) : IsIsotropic Q = AllowsZeroVector Q := rfl

end Stage1.THM_M_0423.Mutations
