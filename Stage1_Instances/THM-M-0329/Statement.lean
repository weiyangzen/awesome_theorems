import Mathlib.Analysis.InnerProductSpace.Dual

/-!
# THM-M-0329: exact Lax-Milgram statement

This module freezes the standard real-Hilbert-space variational statement. It
contains no proof of Lax-Milgram.
-/

noncomputable section

namespace Stage1Instances.THM_M_0329

open InnerProductSpace

universe u

/-- Canonical Lax-Milgram target. The unknown occupies the first argument of
the bounded bilinear form; the datum is an arbitrary continuous functional. -/
def LaxMilgramTarget : Prop :=
  forall (V : Type u) [NormedAddCommGroup V] [InnerProductSpace Real V]
    [CompleteSpace V] (B : V →L[Real] V →L[Real] Real),
      IsCoercive B ->
        forall F : V →L[Real] Real,
          ∃! u : V, forall v : V, B u v = F v

/-- The same claim with the Riesz representative of the datum exposed. -/
def RieszRepresentativeShape : Prop :=
  forall (V : Type u) [NormedAddCommGroup V] [InnerProductSpace Real V]
    [CompleteSpace V] (B : V →L[Real] V →L[Real] Real),
      IsCoercive B ->
        forall f : V,
          ∃! u : V, forall v : V, B u v = @inner Real V _ f v

/-- Riesz representation supplies a checked transport between the functional
and representing-vector encodings; this uses no Lax-Milgram result. -/
theorem target_iff_rieszRepresentativeShape :
    LaxMilgramTarget.{u} ↔ RieszRepresentativeShape.{u} := by
  constructor
  · intro h V _ _ _ B hB f
    simpa only [toDual_apply_apply] using h V B hB (toDual Real V f)
  · intro h V _ _ _ B hB F
    simpa only [toDual_symm_apply] using h V B hB ((toDual Real V).symm F)

-- Structural mutations elaborated separately and rejected by the checker.
def mutationRemovedCoercivity : Prop :=
  forall (V : Type u) [NormedAddCommGroup V] [InnerProductSpace Real V]
    [CompleteSpace V] (B : V →L[Real] V →L[Real] Real)
    (F : V →L[Real] Real),
      ∃! u : V, forall v : V, B u v = F v

def mutationChangedDomainToReal : Prop :=
  forall B : Real →L[Real] Real →L[Real] Real,
    IsCoercive B ->
      forall F : Real →L[Real] Real,
        ∃! u : Real, forall v : Real, B u v = F v

def mutationChangedBinderScope : Prop :=
  forall (V : Type u) [NormedAddCommGroup V] [InnerProductSpace Real V]
    [CompleteSpace V] (B : V →L[Real] V →L[Real] Real)
    (F : V →L[Real] Real),
      ∃! u : V, IsCoercive B -> forall v : V, B u v = F v

def mutationExcludesZeroDatum : Prop :=
  forall (V : Type u) [NormedAddCommGroup V] [InnerProductSpace Real V]
    [CompleteSpace V] (B : V →L[Real] V →L[Real] Real),
      IsCoercive B ->
        forall F : V →L[Real] Real, F ≠ 0 ->
          ∃! u : V, forall v : V, B u v = F v

end Stage1Instances.THM_M_0329

set_option pp.explicit true in
#print Stage1Instances.THM_M_0329.LaxMilgramTarget
