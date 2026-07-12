import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Set.Card
import Mathlib.ModelTheory.Algebra.Field.Basic
import Mathlib.ModelTheory.Definability
import Mathlib.Topology.Closure
import Mathlib.Topology.Separation.Connected

/-!
# THM-M-0665 anchor audit

This module checks the pinned mathlib surfaces available to the frozen target.
They are statement ingredients only; this file does not prove Pila-Wilkie.
-/

open FirstOrder Set

namespace Stage1Instances.THM_M_0665.AnchorAudit

noncomputable section

local instance : FirstOrder.Ring.CompatibleRing Real :=
  FirstOrder.Ring.compatibleRingOfRing Real

/-- Mathlib supplies parameter-definability for finite Cartesian powers. -/
example (L : Language.{0, 0}) [L.Structure Real]
    (X : Set (Fin n -> Real)) : Prop :=
  (Set.univ : Set Real).Definable L X

/-- Ring-language definability supports the local semialgebraic boundary. -/
example (X : Set (Fin n -> Real)) : Prop :=
  (Set.univ : Set Real).Definable Language.ring X

/-- Connectedness and nontriviality support the algebraic-part definition. -/
example (A : Set (Fin n -> Real)) : Prop :=
  IsPreconnected A /\ A.Nontrivial

/-- Finiteness and cardinality support the quantitative conclusion. -/
example (S : Set (Fin n -> Rat)) : Prop :=
  S.Finite /\ (S.ncard : Real) <= 1

/-- Real exponentiation supports the real exponent in the source theorem. -/
example (T : Nat) (epsilon : Real) : Real :=
  (T : Real) ^ epsilon

#check Set.Definable
#check Set.ncard
#check Set.toFinite
#check IsPreconnected
#check Set.Nontrivial
#check Real.rpow

end

end Stage1Instances.THM_M_0665.AnchorAudit
