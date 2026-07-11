import Mathlib.CategoryTheory.Abelian.RightDerived
import Mathlib.Algebra.Homology.SpectralSequence.Basic

/-!
Kernel-checked infrastructure probe for the THM-M-0007 statement gate.

The repository intake does not yet freeze a source-exact convergence convention, and pinned
mathlib supplies spectral-sequence pages but no abutment or convergence predicate. Accordingly,
this file declares no canonical theorem and no proxy convergence proposition. It checks only the
typed objects common to the possible source-faithful formulations.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits

namespace Stage1Instances.THM_M_0007.StatementInfrastructure

universe uC vC uD vD uE vE

variable {C : Type uC} [Category.{vC} C] [Abelian C] [HasInjectiveResolutions C]
variable {D : Type uD} [Category.{vD} D] [Abelian D] [HasInjectiveResolutions D]
variable {E : Type uE} [Category.{vE} E] [Abelian E]

/-- The expected object on the `(p,q)` position of the second page. -/
abbrev ExpectedE2Term (F : Functor C D) (G : Functor D E) [F.Additive] [G.Additive]
    (X : C) (p q : ℕ) : E :=
  (G.rightDerived p).obj ((F.rightDerived q).obj X)

/-- The expected degree-`n` abutment object. This does not assert convergence to it. -/
abbrev ExpectedAbutment (F : Functor C D) (G : Functor D E) [F.Additive] [G.Additive]
    (X : C) (n : ℕ) : E :=
  ((F ⋙ G).rightDerived n).obj X

/-- Pinned mathlib's typed first-quadrant cohomological spectral-sequence carrier. -/
abbrev FirstQuadrantE2SpectralSequence : Type _ :=
  E₂CohomologicalSpectralSequenceNat E

#check ExpectedE2Term
#check ExpectedAbutment
#check FirstQuadrantE2SpectralSequence
#check SpectralSequence.page

end Stage1Instances.THM_M_0007.StatementInfrastructure
