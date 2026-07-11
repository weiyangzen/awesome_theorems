import Mathlib.CategoryTheory.Yoneda

/-! Exact-type checks for the immutable mathlib anchor audited for THM-M-0088. -/

open CategoryTheory

universe v u

namespace Stage1Instances.THM_M_0088.AnchorAudit

/-- The pinned mathlib candidate has exactly the frozen data-valued target type. -/
def exactMathlibAnchor (C : Type u) [Category.{v} C] :
    (yoneda (C := C)).FullyFaithful :=
  Yoneda.fullyFaithful

/-- The terminal candidate is definitionally the selected mathlib declaration. -/
theorem exactMathlibAnchor_eq (C : Type u) [Category.{v} C] :
    exactMathlibAnchor C = Yoneda.fullyFaithful :=
  rfl

end Stage1Instances.THM_M_0088.AnchorAudit

#check @CategoryTheory.Yoneda.fullyFaithful
#print axioms CategoryTheory.Yoneda.fullyFaithful
#print CategoryTheory.Yoneda.fullyFaithful
#print axioms Stage1Instances.THM_M_0088.AnchorAudit.exactMathlibAnchor
