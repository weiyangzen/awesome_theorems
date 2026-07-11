import Mathlib.CategoryTheory.Abelian.LeftDerived
import Mathlib.CategoryTheory.Abelian.RightDerived

/-!
An elaborated candidate normalization for THM-M-0006.

This is deliberately not named `CanonicalStatement`: the repository's one-line source does not
determine the hypotheses or whether "derived functor" means the degreewise resolution construction
or a total derived functor. The statement phase therefore may validate this candidate without
freezing it as the exact source claim.
-/

noncomputable section

open CategoryTheory

universe uC vC uD vD

namespace Stage1Instances.THM_M_0006

/--
The degreewise abelian-resolution reading of "left/right derived functors exist" discovered in the
legacy module. All universes, domains, typeclass assumptions, binders, and the conclusion are
explicit here so that the candidate can be compared against a future source-authorized target.
-/
def AbelianResolutionCandidate : Prop :=
  ∀ {C : Type uC} [Category.{vC} C] [Abelian C]
    [HasProjectiveResolutions C] [HasInjectiveResolutions C]
    {D : Type uD} [Category.{vD} D] [Abelian D]
    (F : CategoryTheory.Functor C D) [F.Additive],
      (∀ n : Nat, Nonempty {G : CategoryTheory.Functor C D // G = F.leftDerived n}) ∧
        (∀ n : Nat, Nonempty {G : CategoryTheory.Functor C D // G = F.rightDerived n})

#check AbelianResolutionCandidate
#print AbelianResolutionCandidate

end Stage1Instances.THM_M_0006
