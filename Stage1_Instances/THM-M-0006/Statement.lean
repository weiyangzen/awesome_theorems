import Mathlib.CategoryTheory.Abelian.LeftDerived
import Mathlib.CategoryTheory.Abelian.RightDerived

/-!
# THM-M-0006 statement boundary probe

The repository record says only "existence of left/right derived functors". It does not select
the ambient categories, variance, exactness or additivity assumptions, resolution hypotheses, or
whether "derived functor" means the degreewise abelian construction or a total Kan extension.
This module therefore checks only the pinned interfaces of the narrow degreewise candidate. It
deliberately declares no canonical target, checked alternate transport, or mutation fixture.
-/

noncomputable section

open CategoryTheory

universe uC vC uD vD

namespace Stage1Instances.THM_M_0006

section DegreewiseBoundary

variable {C : Type uC} [Category.{vC} C] [Abelian C]
variable {D : Type uD} [Category.{vD} D] [Abelian D]

#check HasProjectiveResolutions
#check HasInjectiveResolutions
#check Functor.leftDerived
#check Functor.rightDerived

end DegreewiseBoundary

end Stage1Instances.THM_M_0006
