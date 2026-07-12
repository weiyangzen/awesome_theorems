import Mathlib.Analysis.Calculus.VectorField

/-!
# THM-M-1258: Hormander bracket condition

This file elaborates the condition named by the repository metadata. It defines a predicate; it
does not assert the separate regularity theorem recorded as THM-M-1259.
-/

noncomputable section

namespace Stage1Instances.THM_M_1258

abbrev Euclidean (n : Nat) := Fin n -> Real

abbrev RealVectorField (n : Nat) := Euclidean n -> Euclidean n

/-- Coordinate coefficients of a real vector field on `Real^n`. -/
abbrev Coefficients (n : Nat) := Fin n -> Euclidean n -> Real

def asVectorField {n : Nat} (a : Coefficients n) : RealVectorField n :=
  fun x i => a i x

/-- The family obtained from the drift and square fields by iterated Lie brackets. -/
inductive GeneratedBracket {n r : Nat}
    (X0 : Coefficients n) (X : Fin r -> Coefficients n) : RealVectorField n -> Prop where
  | drift : GeneratedBracket X0 X (asVectorField X0)
  | square (j : Fin r) : GeneratedBracket X0 X (asVectorField (X j))
  | bracket {V W : RealVectorField n} :
      GeneratedBracket X0 X V ->
      GeneratedBracket X0 X W ->
      GeneratedBracket X0 X (VectorField.lieBracket Real V W)

/--
Hormander's bracket-generating condition: at each point of the open domain, values of the drift,
square fields, and all their iterated Lie brackets span the full tangent space `Real^n`.
-/
def hormanderCondition {n r : Nat}
    (Omega : TopologicalSpace.Opens (Euclidean n))
    (X0 : Coefficients n) (X : Fin r -> Coefficients n) : Prop :=
  forall x : Euclidean n, x ∈ (Omega : Set (Euclidean n)) ->
    Submodule.span Real
      ((fun V : RealVectorField n => V x) '' {V | GeneratedBracket X0 X V}) = ⊤

#check hormanderCondition
#check @hormanderCondition

end Stage1Instances.THM_M_1258
