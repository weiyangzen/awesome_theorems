import Mathlib.CategoryTheory.Abelian.FreydMitchell

/-!
# THM-M-0086 canonical Lean statement

This module freezes the three claim branches identified by the accepted intake.  The generator
results require no second import: `FreydMitchell` already exposes their declarations through its
pinned transitive import closure.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits
open CategoryTheory.Abelian

universe v u

namespace Stage1Instances.THM_M_0086

/-- Full, faithful, and exact (finite-limit/finite-colimit preserving) module embedding. -/
def EmbeddingBranch (C : Type u) [Category.{v} C] [Abelian C] : Prop :=
  ∃ (R : Type (max u v)) (_ : Ring R) (F : C ⥤ ModuleCat.{max u v} R),
    F.Full ∧ F.Faithful ∧ PreservesFiniteLimits F ∧ PreservesFiniteColimits F

/-- Freyd's injective-cogenerator existence result, with all auxiliary hypotheses explicit. -/
def InjectiveBranch (C : Type u) [Category.{v} C] [Abelian C] : Prop :=
  ∀ [HasLimits C] [EnoughInjectives C] (G : C),
    IsSeparator G → ∃ I : C, Injective I ∧ IsCoseparator I

/-- The dual projective-generator existence result. -/
def ProjectiveBranch (C : Type u) [Category.{v} C] [Abelian C] : Prop :=
  ∀ [HasColimits C] [EnoughProjectives C] (G : C),
    IsCoseparator G → ∃ P : C, Projective P ∧ IsSeparator P

/--
The exact formal target for the repository's three-branch "Freyd theorem" package.

There is deliberately no nonemptiness or nontriviality hypothesis: the empty/degenerate boundary
is covered by the universal quantifier and the `Abelian` typeclass.
-/
def CanonicalStatement : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C],
    EmbeddingBranch C ∧ InjectiveBranch C ∧ ProjectiveBranch C

/-- Unfolded alternate encoding, checked definitionally equivalent to the named target. -/
theorem canonicalStatement_iff_unfolded :
    CanonicalStatement.{v, u} ↔
      ∀ (C : Type u) [Category.{v} C] [Abelian C],
        (∃ (R : Type (max u v)) (_ : Ring R) (F : C ⥤ ModuleCat.{max u v} R),
            F.Full ∧ F.Faithful ∧ PreservesFiniteLimits F ∧ PreservesFiniteColimits F) ∧
        (∀ [HasLimits C] [EnoughInjectives C] (G : C),
            IsSeparator G → ∃ I : C, Injective I ∧ IsCoseparator I) ∧
        (∀ [HasColimits C] [EnoughProjectives C] (G : C),
            IsCoseparator G → ∃ P : C, Projective P ∧ IsSeparator P) := by
  simp only [CanonicalStatement, EmbeddingBranch, InjectiveBranch, ProjectiveBranch]

/-! Mutation probes compare proof terms, rather than merely checking that mutated Props parse. -/

def RemovedHypothesisMutation : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C],
    EmbeddingBranch C ∧
      (∀ [HasLimits C] (G : C), IsSeparator G → ∃ I : C, Injective I ∧ IsCoseparator I) ∧
      ProjectiveBranch C

def ChangedDomainMutation : Prop :=
  ∀ (C : Type (u + 1)) [Category.{v} C] [Abelian C],
    EmbeddingBranch C ∧ InjectiveBranch C ∧ ProjectiveBranch C

def ChangedBinderScopeMutation : Prop :=
  ∃ (R : Type (max u v)) (_ : Ring R), ∀ (C : Type u) [Category.{v} C] [Abelian C],
    (∃ F : C ⥤ ModuleCat.{max u v} R,
      F.Full ∧ F.Faithful ∧ PreservesFiniteLimits F ∧ PreservesFiniteColimits F) ∧
    InjectiveBranch C ∧ ProjectiveBranch C

def ExcludedBoundaryMutation : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C] [Nonempty C],
    EmbeddingBranch C ∧ InjectiveBranch C ∧ ProjectiveBranch C

variable
  (hRemoved : RemovedHypothesisMutation.{v, u})
  (hDomain : ChangedDomainMutation.{v, u})
  (hScope : ChangedBinderScopeMutation.{v, u})
  (hBoundary : ExcludedBoundaryMutation.{v, u})

#check_failure (show CanonicalStatement.{v, u} from hRemoved)
#check_failure (show CanonicalStatement.{v, u} from hDomain)
#check_failure (show CanonicalStatement.{v, u} from hScope)
#check_failure (show CanonicalStatement.{v, u} from hBoundary)

set_option pp.universes true in
set_option pp.explicit true in
#print CanonicalStatement

#check canonicalStatement_iff_unfolded
#print axioms canonicalStatement_iff_unfolded

end Stage1Instances.THM_M_0086
