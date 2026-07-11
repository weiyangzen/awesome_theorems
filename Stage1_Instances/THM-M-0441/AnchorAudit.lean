import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Set.Card
import Mathlib.ModelTheory.Algebra.Field.Basic
import Mathlib.ModelTheory.Definability
import Mathlib.Topology.Closure
import Mathlib.Topology.Separation.Connected

/-!
# THM-M-0441 anchor audit

This file checks the pinned mathlib surfaces used by the exact statement.  It
does not provide a proof of Pila-Wilkie.
-/

open FirstOrder Set

namespace Stage1Instances.THM_M_0441.AnchorAudit

noncomputable section

local instance : FirstOrder.Ring.CompatibleRing Real :=
  FirstOrder.Ring.compatibleRingOfRing Real

/-- Mathlib supplies parameter-definability for sets in finite Cartesian powers. -/
example (L : Language.{0, 0}) [L.Structure Real]
    (X : Set (Fin n -> Real)) : Prop :=
  (Set.univ : Set Real).Definable L X

/-- The ring-language specialization needed to encode semialgebraic sets elaborates. -/
example (X : Set (Fin n -> Real)) : Prop :=
  (Set.univ : Set Real).Definable Language.ring X

/-- Topological connectedness and nontriviality support the statement's algebraic-part boundary. -/
example (A : Set (Fin n -> Real)) : Prop :=
  IsPreconnected A /\ A.Nontrivial

/-- `Set.ncard` and its explicit finiteness premise support the counting conclusion. -/
example (S : Set (Fin n -> Rat)) : Prop :=
  S.Finite /\ (S.ncard : Real) <= 1

/-- Real exponentiation supports the source exponent `epsilon : Real`. -/
example (T : Nat) (epsilon : Real) : Real :=
  (T : Real) ^ epsilon

#check Set.Definable
#check Set.ncard
#check Set.toFinite
#check IsPreconnected
#check Set.Nontrivial
#check Real.rpow

end

end Stage1Instances.THM_M_0441.AnchorAudit
