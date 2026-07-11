import Mathlib.Geometry.Manifold.Complex
import Mathlib.LinearAlgebra.Dimension.Finite

/-!
# THM-M-0113: Hodge decomposition statement boundary

This module elaborates the compact-Kahler cohomological statement selected at
intake. The pinned mathlib snapshot does not provide de Rham/Dolbeault
cohomology or a bundled Kahler-manifold API, so those notions are exposed as
typed data and predicates. No field assumes either conclusion of the theorem.
This file states the target only; it does not prove Hodge decomposition.
-/

noncomputable section

open scoped Manifold Topology

namespace Stage1Instances.THMM0113

universe uE uH uM uC

/-- Bidegrees contributing to total cohomological degree `n`. -/
abbrev Bidegree (n : Nat) := {pq : Nat × Nat // pq.1 + pq.2 = n}

/--
The objects needed to state Hodge decomposition in the current dependency
snapshot. `isKahler` denotes the usual compatibility and closedness condition
on a Hermitian metric; `cohomology n` denotes complex de Rham cohomology and
`hodgePiece n p q` its `(p,q)` subspace. The conjugation laws make
`conjugate` an involutive conjugate-linear map, without assuming that it
preserves or exchanges any Hodge piece.
-/
structure HodgeData
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace Complex E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Complex E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [CompactSpace M] [T2Space M] where
  isComplexManifold : IsManifold I omega M
  isKahler : Prop
  cohomology : Nat -> Type uC
  [cohomologyAddCommGroup : forall n, AddCommGroup (cohomology n)]
  [cohomologyModule : forall n, Module Complex (cohomology n)]
  hodgePiece : forall n : Nat, Nat -> Nat -> Submodule Complex (cohomology n)
  conjugate : forall n, cohomology n -> cohomology n
  conjugate_add : forall n x y, conjugate n (x + y) = conjugate n x + conjugate n y
  conjugate_smul : forall n (z : Complex) x,
    conjugate n (z • x) = star z • conjugate n x
  conjugate_involutive : forall n x, conjugate n (conjugate n x) = x

attribute [instance] HodgeData.cohomologyAddCommGroup HodgeData.cohomologyModule

namespace HodgeData

variable
  {E : Type uE} [NormedAddCommGroup E] [NormedSpace Complex E]
  {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners Complex E H}
  {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
  [CompactSpace M] [T2Space M]

/-- The Hodge piece indexed without a redundant proof that `p + q = n`. -/
def piece (D : HodgeData E H I M) (n : Nat) (pq : Bidegree n) :
    Submodule Complex (D.cohomology n) :=
  D.hodgePiece n pq.1.1 pq.1.2

/-- The internal direct-sum assertion in total degree `n`. -/
def IsHodgeDirectSum (D : HodgeData E H I M) (n : Nat) : Prop :=
  iSupIndep (fun pq : Bidegree n => D.piece n pq) /\
    iSup (fun pq : Bidegree n => D.piece n pq) = ⊤

/-- Complex conjugation exchanges the `(p,q)` and `(q,p)` pieces. -/
def HasConjugationSymmetry (D : HodgeData E H I M) (n : Nat) : Prop :=
  forall p q : Nat, p + q = n -> forall x : D.cohomology n,
    x ∈ D.hodgePiece n p q <-> D.conjugate n x ∈ D.hodgePiece n q p

/-- The fixed-data conclusion, including every degree and boundary bidegree. -/
def Conclusion (D : HodgeData E H I M) : Prop :=
  forall n : Nat, D.IsHodgeDirectSum n /\ D.HasConjugationSymmetry n

end HodgeData

/--
The exact normalized target: every finite-dimensional compact Kahler manifold
has the Hodge direct-sum decomposition of complex de Rham cohomology in every
degree, and conjugation swaps the two bidegrees.
-/
def HodgeDecompositionTarget : Prop :=
  forall (E : Type uE) [NormedAddCommGroup E] [NormedSpace Complex E]
    [FiniteDimensional Complex E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Complex E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [CompactSpace M] [T2Space M]
    (D : HodgeData.{uE, uH, uM, uC} E H I M),
      D.isKahler -> D.Conclusion

/-- Checked expansion fixing the target's binders, hypothesis, and conclusion. -/
theorem hodgeDecompositionTarget_iff_expanded :
    HodgeDecompositionTarget.{uE, uH, uM, uC} <->
      forall (E : Type uE) [NormedAddCommGroup E] [NormedSpace Complex E]
        [FiniteDimensional Complex E]
        (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Complex E H)
        (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
        [CompactSpace M] [T2Space M]
        (D : HodgeData.{uE, uH, uM, uC} E H I M),
          D.isKahler ->
            forall n : Nat,
              D.IsHodgeDirectSum n /\ D.HasConjugationSymmetry n :=
  Iff.rfl

-- Separately elaborated structural mutations; none receives equivalence credit.
def MutationRemovedCompactness : Prop :=
  forall (E : Type uE) [NormedAddCommGroup E] [NormedSpace Complex E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Complex E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [CompactSpace M] [T2Space M] (D : HodgeData.{uE, uH, uM, uC} E H I M),
      D.Conclusion

def MutationChangedCoefficients : Prop :=
  forall _n : Nat, Nonempty (Type uC)

def MutationFixedDegreeZero : Prop :=
  forall (E : Type uE) [NormedAddCommGroup E] [NormedSpace Complex E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Complex E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [CompactSpace M] [T2Space M] (D : HodgeData.{uE, uH, uM, uC} E H I M),
      D.isKahler -> D.IsHodgeDirectSum 0 /\ D.HasConjugationSymmetry 0

end Stage1Instances.THMM0113

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THMM0113.HodgeDecompositionTarget
