import Mathlib.Algebra.Group.Defs

/-!
# THM-M-0118: Nakano vanishing statement

This file freezes the positive-vector-bundle form selected by the intake. The
pinned library does not yet bundle the required analytic Kahler, holomorphic
vector-bundle, curvature-positivity, and Dolbeault-cohomology interfaces, so
they are exposed as typed input data. No field contains a vanishing result.

This module elaborates the statement only; it does not prove it.
-/

namespace Stage1Instances.THMM0118

universe uX uE uH

/-- Typed inputs for the Nakano-positive vector-bundle vanishing statement.
`Cohomology p q` denotes `H^q(X, Omega^p_X tensor E)`. The three propositions
retain their standard analytic meanings and will require checked transports
when native mathlib interfaces become available. -/
structure NakanoVanishingData where
  X : Type uX
  E : Type uE
  complexDimension : Nat
  Cohomology : Nat -> Nat -> Type uH
  cohomologyAddCommGroup : forall p q, AddCommGroup (Cohomology p q)
  compactKahler : Prop
  holomorphicVectorBundle : Prop
  nakanoPositive : Prop

namespace NakanoVanishingData

variable (D : NakanoVanishingData.{uX, uE, uH})

/-- Vanishing means that the indicated cohomology group has exactly one
element. This is the type-level form of equality to the zero group. -/
def Vanishes (p q : Nat) : Prop :=
  Subsingleton (D.Cohomology p q)

end NakanoVanishingData

/-- Exact selected root: on a compact Kahler manifold of complex dimension
`n`, a Nakano-positive holomorphic vector bundle has
`H^q(X, Omega^p_X tensor E) = 0` whenever `p + q > n`. -/
def NakanoVanishingTarget : Prop :=
  forall (D : NakanoVanishingData.{uX, uE, uH}) (p q : Nat),
    D.compactKahler ->
    D.holomorphicVectorBundle ->
    D.nakanoPositive ->
    D.complexDimension < p + q ->
    D.Vanishes p q

/-- Checked expansion fixing all binders, hypotheses, the strict range, and
the type-level zero-group conclusion. -/
theorem nakanoVanishingTarget_iff_expanded :
    NakanoVanishingTarget.{uX, uE, uH} <->
      forall (D : NakanoVanishingData.{uX, uE, uH}) (p q : Nat),
        D.compactKahler ->
        D.holomorphicVectorBundle ->
        D.nakanoPositive ->
        D.complexDimension < p + q ->
        Subsingleton (D.Cohomology p q) :=
  Iff.rfl

-- Separately elaborated mutations; none receives equivalence credit.
def MutationRemovedPositivity : Prop :=
  forall (D : NakanoVanishingData.{uX, uE, uH}) (p q : Nat),
    D.compactKahler -> D.holomorphicVectorBundle ->
    D.complexDimension < p + q -> D.Vanishes p q

def MutationChangedDegreeDomain : Prop :=
  forall (D : NakanoVanishingData.{uX, uE, uH}) (p q : Int),
    D.compactKahler -> D.holomorphicVectorBundle -> D.nakanoPositive ->
    (D.complexDimension : Int) < p + q ->
    Subsingleton (D.Cohomology p.natAbs q.natAbs)

def MutationChangedBinderScope : Prop :=
  forall p q : Nat,
    p + q > 0 ->
    forall D : NakanoVanishingData.{uX, uE, uH},
      D.compactKahler -> D.holomorphicVectorBundle -> D.nakanoPositive ->
      D.Vanishes p q

def MutationIncludesBoundary : Prop :=
  forall (D : NakanoVanishingData.{uX, uE, uH}) (p q : Nat),
    D.compactKahler -> D.holomorphicVectorBundle -> D.nakanoPositive ->
    D.complexDimension <= p + q -> D.Vanishes p q

end Stage1Instances.THMM0118

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THMM0118.NakanoVanishingTarget
