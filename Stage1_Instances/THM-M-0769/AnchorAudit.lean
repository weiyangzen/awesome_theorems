import Mathlib.Logic.Nonempty

/-!
# THM-M-0769 anchor audit

These declarations check three pinned candidates against the frozen target's
literal dependent-family type. They are audit witnesses, not the target's
downstream proof artifact.
-/

universe u v

namespace Stage1Instances.THM_M_0769.AnchorAudit

theorem viaPiInstNonempty :
    ∀ (ι : Sort u) (A : ι → Sort v),
      (∀ i, Nonempty (A i)) → Nonempty (∀ i, A i) :=
  fun _ _ h => @Pi.instNonempty _ _ h

theorem viaClassicalNonemptyPi :
    ∀ (ι : Sort u) (A : ι → Sort v),
      (∀ i, Nonempty (A i)) → Nonempty (∀ i, A i) :=
  fun _ _ h => Classical.nonempty_pi.mpr h

theorem viaClassicalChoice :
    ∀ (ι : Sort u) (A : ι → Sort v),
      (∀ i, Nonempty (A i)) → Nonempty (∀ i, A i) :=
  fun _ _ h => ⟨fun i => Classical.choice (h i)⟩

#check @Pi.instNonempty
#check @Classical.nonempty_pi
#check @Classical.axiomOfChoice
#print axioms viaPiInstNonempty
#print axioms viaClassicalNonemptyPi
#print axioms viaClassicalChoice

end Stage1Instances.THM_M_0769.AnchorAudit
