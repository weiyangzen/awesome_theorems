import Mathlib.Analysis.Calculus.VectorField

/-!
# THM-M-1258 obligation composition harness

This checks the pointwise-to-condition composition and two boundary cases. It intentionally does
not assert that arbitrary vector fields meet the condition.
-/

noncomputable section

namespace Stage1Instances.THM_M_1258_Obligations

abbrev Euclidean (n : Nat) := Fin n -> Real
abbrev RealVectorField (n : Nat) := Euclidean n -> Euclidean n
abbrev Coefficients (n : Nat) := Fin n -> Euclidean n -> Real

def asVectorField {n : Nat} (a : Coefficients n) : RealVectorField n := fun x i => a i x

inductive GeneratedBracket {n r : Nat}
    (X0 : Coefficients n) (X : Fin r -> Coefficients n) : RealVectorField n -> Prop where
  | drift : GeneratedBracket X0 X (asVectorField X0)
  | square (j : Fin r) : GeneratedBracket X0 X (asVectorField (X j))
  | bracket {V W : RealVectorField n} :
      GeneratedBracket X0 X V -> GeneratedBracket X0 X W ->
      GeneratedBracket X0 X (VectorField.lieBracket Real V W)

def condition {n r : Nat} (Omega : TopologicalSpace.Opens (Euclidean n))
    (X0 : Coefficients n) (X : Fin r -> Coefficients n) : Prop :=
  forall x, x ∈ (Omega : Set (Euclidean n)) ->
    Submodule.span Real
      ((fun V : RealVectorField n => V x) '' {V | GeneratedBracket X0 X V}) = ⊤

/-- Exact child-to-parent composition: the open pointwise span family is consumed explicitly. -/
theorem compose_condition {n r : Nat} (Omega : TopologicalSpace.Opens (Euclidean n))
    (X0 : Coefficients n) (X : Fin r -> Coefficients n)
    (span_at : forall x, x ∈ (Omega : Set (Euclidean n)) ->
      Submodule.span Real
        ((fun V : RealVectorField n => V x) '' {V | GeneratedBracket X0 X V}) = ⊤) :
    condition Omega X0 X := span_at

theorem empty_domain {n r : Nat} (X0 : Coefficients n) (X : Fin r -> Coefficients n) :
    condition (⊥ : TopologicalSpace.Opens (Euclidean n)) X0 X := by
  intro x hx
  exfalso
  simpa using hx

theorem zero_dimension {r : Nat} (Omega : TopologicalSpace.Opens (Euclidean 0))
    (X0 : Coefficients 0) (X : Fin r -> Coefficients 0) : condition Omega X0 X := by
  intro x hx
  exact Subsingleton.elim _ _

#check compose_condition
#print axioms compose_condition
#print axioms empty_domain
#print axioms zero_dimension

end Stage1Instances.THM_M_1258_Obligations
