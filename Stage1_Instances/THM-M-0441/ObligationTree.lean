import Statement

/-!
# THM-M-0441 obligation composition

This module gives typed interfaces for the frozen Pila-Wilkie architecture and
checks only their binder-preserving composition. It deliberately supplies no
parameterization, determinant, block-counting, or dimension-induction proof.
-/

open FirstOrder Set

namespace Stage1Instances.THM_M_0441.ObligationTree

open Stage1Instances.THM_M_0441

/-- The quantitative conclusion after the language, set, and exponent have
been fixed. This is definitionally the corresponding tail of `PilaWilkie`. -/
def CountingConclusion (X : Set (Fin n -> Real)) (epsilon : Real) : Prop :=
  exists c : Real, 0 < c /\ forall T : Nat, 1 <= T ->
    (transcendentalRationalPoints X T).Finite /\
    ((transcendentalRationalPoints X T).ncard : Real) <=
      c * (T : Real) ^ epsilon

/-- A typed boundary for the combined geometric proof engine. Its fields are
premises for future proof work, not declarations of Pila-Wilkie facts. -/
structure CountingEngine where
  parameterization : Prop
  determinantEstimate : Prop
  blockDecomposition : Prop
  dimensionInduction : Prop
  deriveCounting :
    parameterization -> determinantEstimate -> blockDecomposition ->
      dimensionInduction ->
      forall (L : Language.{0, 0}) [L.Structure Real],
        IsOMinimalExpansion L ->
        forall (n : Nat) (X : Set (Fin n -> Real)),
          (Set.univ : Set Real).Definable L X ->
          forall epsilon : Real, 0 < epsilon -> CountingConclusion X epsilon

/-- Checked composition from the four explicitly named mathematical engines
to the exact canonical target. No field is inhabited in this phase. -/
theorem engine_compose (E : CountingEngine)
    (hParam : E.parameterization)
    (hDet : E.determinantEstimate)
    (hBlocks : E.blockDecomposition)
    (hDim : E.dimensionInduction) : PilaWilkie := by
  intro L _ hOM n X hDef epsilon hEpsilon
  exact E.deriveCounting hParam hDet hBlocks hDim L hOM n X hDef epsilon hEpsilon

/-- The local quantitative interface expands to the exact statement tail. -/
theorem countingConclusion_iff (X : Set (Fin n -> Real)) (epsilon : Real) :
    CountingConclusion X epsilon <->
      exists c : Real, 0 < c /\ forall T : Nat, 1 <= T ->
        (transcendentalRationalPoints X T).Finite /\
        ((transcendentalRationalPoints X T).ncard : Real) <=
          c * (T : Real) ^ epsilon := by
  rfl

#check engine_compose
#print axioms engine_compose

end Stage1Instances.THM_M_0441.ObligationTree
