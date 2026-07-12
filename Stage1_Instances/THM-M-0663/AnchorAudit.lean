import Mathlib.ModelTheory.Definability
import Mathlib.ModelTheory.Order
import Mathlib.Topology.Order.Basic
import Mathlib.Topology.Order.MonotoneContinuity

/-!
# THM-M-0663 pinned-mathlib anchor audit

This module checks the pinned library interfaces relevant to the frozen target. It deliberately
does not state or prove o-minimal monotonicity.
-/

open FirstOrder Set

namespace Stage1Instances.THM_M_0663.AnchorAudit

universe u v w

variable {L : Language.{u, v}} {M : Type w}

/-- Pinned mathlib supplies parameter-definable unary sets. -/
example [L.Structure M] (A : Set M) : Prop :=
  (Set.univ : Set M).Definable₁ L A

/-- It also supplies compatibility between a language order and the carrier order. -/
example [L.IsOrdered] [L.Structure M] [LinearOrder M] [L.OrderedStructure M] :
    FirstOrder.Language.OrderedStructure L M := inferInstance

/-- The conclusion vocabulary is available independently of an o-minimal proof. -/
example [LinearOrder M] [TopologicalSpace M] (f : M -> M) (p : Set M) : Prop :=
  ContinuousOn f p /\ (StrictMonoOn f p \/ StrictAntiOn f p)

#check Set.Definable₁
#check FirstOrder.Language.OrderedStructure
#check Set.OrdConnected
#check ContinuousOn
#check StrictMonoOn
#check StrictAntiOn

end Stage1Instances.THM_M_0663.AnchorAudit
